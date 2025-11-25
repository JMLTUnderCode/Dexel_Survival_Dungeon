"""
Acciones para el HSM

Descripción
-------------------
    MÓDULO: Colección y registro de acciones (ACTIONS) invocables por la HSM.
    Cada acción implementa un efecto sobre el mundo y/o el blackboard y tiene la
    firma: fn(hinst, entity) -> None, donde:
        - hinst: instancia runtime de la HSM (HSMInstance) que expone el blackboard
                 y utilitarios de spec/manager.
        - entity: la entidad (Enemy / Boss / etc.) sobre la que opera la acción.

    Propósito:
        - Encapsular comportamientos atómicos (iniciar patrol, spawn, curación, cambiar
          algoritmo, asignar FollowPath, actualizar bookkeeping, etc.).
        - Mantener efectos locales y documentados en el blackboard para que las
          condiciones y transiciones puedan leerlos/consumirlos.

Convenciones
-------------------
    - Documentación: todos los docstrings de acciones deben estar en español y
      documentar: Descripción, Argumentos, Blackboard utilizado/modificado y
      Parámetros esperados. Si no hay entradas para Blackboard o Parámetros, indicar
      explícitamente "- Ninguno".
    - Firma: fn(hinst, entity) -> None (no return útil). Acciones no deben devolver valores.
    - Registro: usar el decorador @_register("nombre_accion") para exponer la acción.
    - Efectos en blackboard: preferir set_blackboard/get_blackboard (hinst.* helpers)
      para sincronizar datos entre condiciones/acciones/estado.
    - Seguridad: capturar excepciones internamente y usar exception_print para logging;
      no propagar excepciones al bucle principal del juego.
    - Determinismo y peso: las acciones deben ser rápidas y deterministas; evitar operaciones
      bloqueantes o cálculos pesados (offload a systems/manager si es necesario).
    - Acceso a servicios: usar get_spec_param, get_manager, get_player desde ai.utils
      para leer parámetros del spec y acceder a servicios/globales.
    - Manipulación de entidad: modificar campos de la entidad (algorithm, follow_path,
      velocity, face.target, etc.), pero documentar los cambios en el docstring.
    - Atomicidad: intentar que cada acción sea atómica y recuperable; mantener bookkeeping
      coherente en caso de fallo.
    - Tamaño: preferir funciones pequeñas; extraer lógica compleja a helpers privados
      dentro del módulo (prefijo _).
    - Nombres de claves: documentar claves de blackboard que la acción lee/escribe y
      eliminar o limpiar claves cuando sea apropiado en stop_* actions.
"""
import random
import math
import time
from typing import Dict, Callable, Any, List, Optional

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.path_following import FollowPath
from characters.animation import set_animation_state
from helper.paths import PolylinePath
from configs.package import CONF

from ai.utils import get_spec_param, get_manager, get_player, exception_print

# ACTIONS: mapping string -> callable(hinst, entity)
ACTIONS: Dict[str, Callable[[Any, Any], None]] = {}

# --------------------
# Registro de acciones
# --------------------
def _register(name: str):
    """Decorador para registrar acciones en ACTIONS."""
    def _decor(fn: Callable[[Any, Any], None]):
        ACTIONS[name] = fn
        return fn
    return _decor

# --------------------
# Helpers locales
# --------------------
def _find_best_patrol_path(pathfinder, start_pos, desired_nodes: int, max_attempts: int = 12) -> Optional[List]:
    """
    Intentar encontrar una ruta (lista de puntos) con al menos desired_nodes.
    Retorna None si no hay navmesh o no se encuentra ruta adecuada.
    """
    if not getattr(pathfinder, "navmesh", None):
        return None
    nodes_list = list(getattr(pathfinder.navmesh, "nodes", {}).values())
    if not nodes_list:
        return None
    attempts = 0
    best = None
    while attempts < max_attempts:
        target_node = random.choice(nodes_list)
        try:
            pts = pathfinder.find_path(start_pos, target_node.center)
        except Exception:
            pts = None
        if pts and len(pts) >= desired_nodes:
            return pts
        if pts and (best is None or len(pts) > len(best)):
            best = pts
        attempts += 1
    return best

# --------------------
# Bookkeeping general
# --------------------
@_register("record_last_state_start")
def record_last_state_start(hinst, entity):
    """Guardar snapshot de la pila activa al iniciar un estado (para debugging / restore)."""
    try:
        hinst.set_blackboard("last_state_stack", list(hinst.get_active_stack()))
    except Exception as e:
        exception_print("RECORD LAST STATE START", entity, str(e))

# --------------------
# Patrol / FollowPath
# --------------------
@_register("start_random_patrol")
def start_random_patrol(hinst, entity):
    """
    Descripción
        FUNCIÓN: Inicia una patrulla aleatoria usando el navmesh/pathfinder.
        - No sobreescribe la ruta guardian si `is_on_guardian_path` está a True.
        - Si no hay navmesh o no se consigue ruta válida, cambia a comportamiento WANDER.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad (Enemy) sobre la que se crea la patrulla.

    Blackboard utilizado/modificado
        - is_on_guardian_path (read/update): si está en ruta guardian.
        - patrol_target (update): punto final de la patrulla.
        - patrol_requested_at (update): timestamp de última solicitud de patrulla.
        - 

    Parámetros esperados
        - patrol_path_nodes (int): número deseado de nodos en la ruta (default 20).
    """
    try:
        # 1) Si estamos siguiendo la ruta guardian, no crear ruta aleatoria.
        if hinst.get_blackboard("is_on_guardian_path", False):
            return

        # 2) Obtener pathfinder desde el manager; si no existe -> fallback a wander.
        manager = get_manager(hinst)
        pathfinder = getattr(manager, "pathfinder", None)
        if pathfinder is None or getattr(pathfinder, "navmesh", None) is None:
            # 2.a) No hay navmesh: dejar entidad en wander y actualizar timestamp
            entity.follow_path = None
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return

        # 3) Limpiar cualquier follow_path previo para forzar reconstrucción
        entity.follow_path = None

        # 4) Obtener parámetros y buscar ruta en navmesh
        desired_nodes = int(get_spec_param(hinst, "patrol_path_nodes", 20))
        pts = _find_best_patrol_path(pathfinder, entity.get_pos(), desired_nodes)

        # 5) Si no hay puntos adecuados -> fallback a wander
        if not pts:
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return

        # 6) Construir PolylinePath y FollowPath de forma segura
        poly = PolylinePath(pts, closed=False)
        try:
            entity.follow_path = FollowPath(
                character=entity,
                path=poly,
                path_offset=getattr(entity, "path_offset", 1.0),
                current_param=0.0,
                max_acceleration=getattr(entity, "max_acceleration", 300.0)
            )
            entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
            hinst.set_blackboard("patrol_target", pts[-1])
            hinst.set_blackboard("patrol_requested_at", time.time())
            hinst.set_blackboard("is_on_guardian_path", False)
        except Exception as e:
            # 7) Si Falló la asignación del FollowPath -> fallback y log
            exception_print("START RANDOM PATROL", entity, f"Could not assign FollowPath: {e}")
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
            hinst.set_blackboard("patrol_requested_at", time.time())
    except Exception as e:
        exception_print("START RANDOM PATROL", entity, str(e))

@_register("patrol_tick")
def patrol_tick(hinst, entity):
    """
    Descripción
        FUNCIÓN: Tick periódico que mantiene o solicita una nueva patrulla aleatoria.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que ejecuta la patrulla.

    Blackboard utilizado/modificado
        - is_on_guardian_path (read): si está en ruta guardian.
        - patrol_requested_at (read/update): timestamp de última solicitud de patrulla.

    Parámetros esperados
        - patrol_tick_throttle (float): segundos entre posibles nuevas solicitudes (default 3.0).
    """
    try:
        # 1) No interferir si estamos en la ruta guardian
        if hinst.get_blackboard("is_on_guardian_path", False):
            return

        # 2) Obtener throttling y timestamps para no recalcular cada frame
        throttle = float(get_spec_param(hinst, "patrol_tick_throttle", 3.0))
        last = float(hinst.get_blackboard("patrol_requested_at", 0.0))
        now = time.time()

        poly_follow = getattr(entity, "follow_path", None)
        need_new = False

        # 3) Si no hay ruta activa y pasó el throttle -> pedir nueva
        if poly_follow is None:
            if now - last > throttle:
                need_new = True
        else:
            # 4) Si existe ruta, comprobar si está en el último segmento (ruta terminada)
            path_obj = getattr(poly_follow, "path", None)
            curp = float(getattr(poly_follow, "current_param", 0.0))
            seg_count = int(getattr(path_obj, "segment_count", 0))
            if seg_count and curp >= max(0, seg_count - 1):
                need_new = True

            # 5) Si el algoritmo cambió (no está en PATH_FOLLOWING) y pasó throttle -> re-request
            if getattr(entity, "algorithm", None) != CONF.ALG.ALGORITHM.PATH_FOLLOWING and (now - last) > throttle:
                need_new = True

        # 6) Si se decide pedir nueva ruta, delegar a start_random_patrol
        if need_new:
            start_random_patrol(hinst, entity)
    except Exception as e:
        exception_print("PATROL TICK", entity, str(e))

@_register("stop_patrol")
def stop_patrol(hinst, entity):
    """
    Descripción
        ACCIÓN: Detener la patrulla activa y seleccionar algoritmo fallback.

    Argumentos
        - hinst (HSMInstance) : instancia de la HSM.
        - entity (Any) : entidad cuya patrulla se detiene.

    Blackboard utilizado/modificado
        - is_on_guardian_path (read) : si está en ruta guardian.
    
    Parámetros esperados
        - Ninguno
    """
    try:
        # 1) Eliminar referencia a follow_path para detener seguimiento
        entity.follow_path = None

        # 2) Seleccionar algoritmo fallback según bandera is_on_guardian_path
        if not hinst.get_blackboard("is_on_guardian_path", False):
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
        else:
            # Mantener PATH_FOLLOWING si estamos conceptualmente sobre la ruta guardian
            entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
    except Exception as e:
        exception_print("STOP PATROL", entity, str(e))

# --------------------
# Visibility / bookkeeping
# --------------------
@_register("throttle_check_player_visibility")
def throttle_check_player_visibility(hinst, entity):
    """
    Descripción
        ACCIÓN: Acción que verifica la visibilidad del jugador con throttling y actualiza
        el blackboard con información útil para la HSM.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad cuya patrulla se detiene.

    Blackboard utilizado/modificado
        - last_los_check (read/update): timestamp throttle
        - last_known_player_pos (update): última posición conocida del jugador
        - last_player_visible_at (update): timestamp de última visibilidad
        - player_visible (update): si el jugador es visible actualmente

    Parámetros esperados
        - check_los_throttle (float): segundos entre comprobaciones (default 0.25)
        - vision_range (float): distancia máxima de visión (px)
        - vision_fov_deg (float): ángulo de visión en grados (0..180)
    """
    try:
        # 1) Obtener player; si no existe no hay visibilidad que comprobar
        player = get_player(hinst)
        if not player:
            return

        # 2) Throttling: evitar comprobaciones costosas cada frame
        throttle = float(get_spec_param(hinst, "check_los_throttle", 0.25))
        last = float(hinst.get_blackboard("last_los_check", 0.0))
        now = time.time()
        if now - last < throttle:
            return
        # actualizar timestamp del último chequeo
        hinst.set_blackboard("last_los_check", now)

        # 3) Distancia entre entidad y jugador
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dx, dz = px - ex, pz - ez
        dist = math.hypot(dx, dz)
        vision = float(get_spec_param(hinst, "vision_range", 300.0))

        # 3.a) Si fuera de rango, marcar no visible y salir
        if dist > vision:
            hinst.set_blackboard("player_visible", False)
            return

        # 4) Comprobar FOV (cono de visión)
        fov_deg = float(get_spec_param(hinst, "vision_fov_deg", 120.0))
        half_fov_rad = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
        try:
            # calcular ángulo hacia el jugador y diferencia relativa con la orientación de la entidad
            angle_to_player = math.atan2(dz, dx)
            facing = float(getattr(entity, "orientation", 0.0))
            diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
            # si está dentro del cono, actualizar blackboard como visible
            if abs(diff) <= half_fov_rad:
                hinst.set_blackboard("last_known_player_pos", (float(px), float(pz)))
                hinst.set_blackboard("player_visible", True)
                hinst.set_blackboard("last_player_visible_at", now)
                return
        except Exception as e:
            # Fallo en cálculo angular: log y seguir a fallback (marcar no visible)
            exception_print("THROTTLE CHECK PLAYER VISIBILITY", entity, f"FOV error: {e}")

        # 5) Si no cumple FOV -> marcar no visible (la memoria/timeout se maneja en condiciones)
        hinst.set_blackboard("player_visible", False)
    except Exception as e:
        # Defender: no dejar que una excepción rompa el loop del juego
        exception_print("THROTTLE CHECK PLAYER VISIBILITY", entity, str(e))

# --------------------
# Pursue / Attack
# --------------------
@_register("start_pursue_target")
def start_pursue_target(hinst, entity):
    """
    Descripción
        ACCIÓN: Activar persecución hacia el jugador usando el algoritmo de pursue.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad (Enemy) que iniciará la persecución.

    Blackboard utilizado/modificado
        - pursuing (update): flag indicando que la entidad está persiguiendo.
        - last_known_player_pos (update): última posición conocida del jugador.
        - player_visible_since (update): timestamp desde que el jugador fue visto.

    Parámetros esperados
        - Ninguno
    """
    try:
        # 1) Obtener jugador; si no existe no hay nada que perseguir
        player = get_player(hinst)
        if not player:
            return

        # 2) Limpiar residuos cinemáticos que pueden provocar saltos de orientación
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
        entity.rotation = 0.0
        # quitar objetivo face si lo hubiera
        if getattr(entity, "face", None):
            entity.face.target = None

        # 3) Configurar algoritmo de la entidad para persecución y apuntar al player
        entity.algorithm = CONF.ALG.ALGORITHM.PURSUE
        entity.pursue.target = player
        
        # 4) Actualizar blackboard con metadata de persecución
        hinst.set_blackboard("pursuing", True)
        hinst.set_blackboard("last_known_player_pos", (float(player.get_pos()[0]), float(player.get_pos()[1])))
        hinst.set_blackboard("player_visible_since", time.time())
    except Exception as e:
        exception_print("START PURSUE TARGET", entity, str(e))

@_register("pursue_tick")
def pursue_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Tick ligero durante persecución. Mantiene y refresca información de visibilidad
        mediante throttle_check_player_visibility.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad en persecución.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - Ninguno
    """
    try:
        throttle_check_player_visibility(hinst, entity)
    except Exception as e:
        exception_print("PURSUE TICK", entity, str(e))


@_register("stop_pursue")
def stop_pursue(hinst, entity):
    """
    Descripción
        ACCIÓN: Detener la persecución y restablecer comportamiento de patrulla o caminar.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que detiene la persecución.

    Blackboard utilizado/modificado
        - pursuing (update): se limpia la marca de persecución.

    Parámetros esperados
        - Ninguno
    """
    try:
        hinst.set_blackboard("pursuing", False)
        stop_patrol(hinst, entity)
    except Exception as e:
        exception_print("STOP PURSUE", entity, str(e))


@_register("try_melee_attack")
def try_melee_attack(hinst, entity):
    """
    Descripción
        ACCIÓN: Intento de ataque cuerpo a cuerpo. Dispara la animación si el jugador está en rango.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que realiza el ataque.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - attack_range (float): distancia en px considerada para ejecutar el ataque.
    """
    try:
        player = get_player(hinst)
        if not player:
            return

        # 1) Calcular distancia entre entity y player
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)

        # 2) Obtener rango de ataque desde el spec (fallback 48)
        attack_r = float(get_spec_param(hinst, "attack_range", 48.0))

        # 3) Si está en rango, intentar disparar animación de ataque
        if dist <= attack_r:
            try:
                set_animation_state(entity, CONF.ENEMY.ACTIONS.ATTACK)
            except Exception as e:
                exception_print("TRY MELEE ATTACK", entity, f"Anim error: {e}")
    except Exception as e:
        exception_print("TRY MELEE ATTACK", entity, str(e))

# --------------------
# Evade / Flee
# --------------------
@_register("start_evade_from_player")
def start_evade_from_player(hinst, entity):
    """
    Descripción
        ACCIÓN: Poner a la entidad en modo huida frente al jugador.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): la entidad (Enemy) que ejecuta la huida.

    Blackboard usado/modificado
        - prev_algorithm (update): algoritmo previo guardado para restauración.
        - is_fleeing (update): flag que indica que la entidad está huyendo.

    Parámetros esperados
        - Ninguno
    """
    try:
        player = get_player(hinst)
        if not player:
            return

        # 1) Guardar algoritmo previo para restauración posterior
        prev_alg = getattr(entity, "algorithm", None)
        hinst.set_blackboard("prev_algorithm", prev_alg)

        # 2) Intentar que la entidad mire hacia el jugador mientras huye
        try:
            entity.look_where.target = player
        except Exception:
            # No todas las entidades exponen look_where; no es crítico.
            pass

        # 3) Cambiar algoritmo y marcar huida
        entity.algorithm = CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING
        hinst.set_blackboard("is_fleeing", True)
    except Exception as e:
        exception_print("START EVADE FROM PLAYER", entity, str(e))

@_register("evade_tick")
def evade_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Tick de huida — actualizar métricas y bookkeeping útiles durante huida.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad en huida.

    Blackboard usado/modificado
        - distance_to_player (update): distancia Euclidiana actual a player (px).

    Parámetros esperados
        - Ninguno
    """
    try:
        player = get_player(hinst)
        if not player:
            return

        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)
        hinst.set_blackboard("distance_to_player", float(dist))
    except Exception as e:
        exception_print("EVADE TICK", entity, str(e))

@_register("stop_evade")
def stop_evade(hinst, entity):
    """
    Descripción
        ACCIÓN: Finalizar el estado de huida y restaurar comportamiento.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que termina la huida.

    Blackboard usado/modificado
        - is_fleeing (update): se limpia la bandera de huida.
        - prev_algorithm (read): si existe, se usa para restaurar entity.algorithm.

    Parámetros esperados
        - Ninguno.
    """
    try:
        hinst.set_blackboard("is_fleeing", False)
        prev = hinst.get_blackboard("prev_algorithm", None)
        if prev:
            entity.algorithm = prev
        else:
            stop_patrol(hinst, entity)
    except Exception as e:
        exception_print("STOP EVADE", entity, str(e))

# --------------------------------------
# Face / Safe Anchor / Movement Helpers
# --------------------------------------
@_register("face_towards_safe_anchor")
def face_towards_safe_anchor(hinst, entity):
    """
    Descripción
        ACCIÓN: Orientar la entidad hacia un anchor seguro o hacia el jugador si este
        se encuentra dentro de un rango extendido de interés.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad (Enemy) que ejecuta la acción.

    Blackboard utilizado/modificado
        - last_known_player_pos (read): última posición conocida del jugador.
        - safe_anchor (read/update): punto seguro calculado y almacenado.
        - curing_face_target (update): objetivo actual que la entidad está mirando.

    Parámetros esperados
        - safe_distance (float): distancia a usar para calcular anchor seguro.
        - vision_range (float): rango de visión para considerar al jugador.
        - vision_fov_deg (float): ángulo de visión (grados).
        - face_range_multiplier (float): multiplicador para ampliar rango de facing.
    """
    # 1) Preparar parámetros y referencias (player, thresholds, fov)
    try:
        player = get_player(hinst)
        safe_distance = float(get_spec_param(hinst, "safe_distance", 200.0))
        vision = float(get_spec_param(hinst, "vision_range", 300.0))
        fov_deg = float(get_spec_param(hinst, "vision_fov_deg", 120.0))
        face_mult = float(get_spec_param(hinst, "face_range_multiplier", 1.5))
        face_range = vision * face_mult
        half_fov = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)

        # 2) Leer blackboard: posición conocida del jugador y anchor seguro (si existe)
        last_known = hinst.get_blackboard("last_known_player_pos", None)
        safe = hinst.get_blackboard("safe_anchor", None)

        # 3) Si no existe safe_anchor, calcularlo:
        #    - si hay player: punto en dirección opuesta al player a distancia safe_distance
        #    - si no hay player: generar punto aleatorio próximo (fallback)
        if not safe:
            ex, ez = entity.get_pos()
            if player:
                px, pz = player.get_pos()
                dx = ex - px
                dz = ez - pz
                d = math.hypot(dx, dz) or 1.0
                sx = ex + (dx / d) * safe_distance
                sz = ez + (dz / d) * safe_distance
            else:
                ang = random.random() * (2 * math.pi)
                r = 80.0
                sx = ex + math.cos(ang) * r
                sz = ez + math.sin(ang) * r
            safe = (float(sx), float(sz))
            hinst.set_blackboard("safe_anchor", safe)

        # 4) Si existe player, comprobar si está en el rango extendido y en FOV:
        #    - si es así, fijar entity.face.target al player y setear algoritmo FACE.
        if player:
            ex, ez = entity.get_pos()
            px, pz = player.get_pos()
            dx, dz = px - ex, pz - ez
            dist = math.hypot(dx, dz)
            try:
                angle_to_player = math.atan2(dz, dx)
                facing = float(getattr(entity, "orientation", 0.0))
                diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
                if dist <= face_range and abs(diff) <= half_fov:
                    # 4.a) Mirar directamente al player
                    entity.face.target = player
                    entity.algorithm = CONF.ALG.ALGORITHM.FACE
                    hinst.set_blackboard("curing_face_target", player.get_pos())
                    return
            except Exception as e:
                exception_print("FACE TOWARDS SAFE ANCHOR", entity, f"FOV calc error: {e}")

        # 5) Fallback: si no se mira al player, mirar al last_known o al safe_anchor
        target_pos = last_known if last_known is not None else safe
        try:
            tgt = Kinematic(position=target_pos, orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
            entity.face.target = tgt
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
            hinst.set_blackboard("curing_face_target", target_pos)
        except Exception as e:
            exception_print("FACE TOWARDS SAFE ANCHOR", entity, f"Set face target error: {e}")
    except Exception as e:
        exception_print("FACE TOWARDS SAFE ANCHOR", entity, str(e))

@_register("clear_safe_anchor")
def clear_safe_anchor(hinst, entity):
    """
    Descripción
        ACCIÓN: Limpiar el safe_anchor y restaurar el objetivo de facing al jugador (si existe).

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que ejecuta la acción.

    Blackboard utilizado/modificado
        - safe_anchor (update/remove): se elimina el anchor seguro.
        - curing_face_target (update/remove): se limpia el objetivo de facing de curación.

    Parámetros esperados
        - Ninguno
    """
    # 1) Eliminar claves relacionadas con anchor/target de curación del blackboard
    try:
        if "safe_anchor" in hinst.blackboard:
            del hinst.blackboard["safe_anchor"]
        if "curing_face_target" in hinst.blackboard:
            del hinst.blackboard["curing_face_target"]

        # 2) Restablecer objetivo de face al player si existe, ignorando fallos no críticos
        player = get_player(hinst)
        try:
            if player:
                entity.face.target = player
        except Exception as e:
            exception_print("CLEAR SAFE ANCHOR", entity, f"Restore face error: {e}")
    except Exception as e:
        exception_print("CLEAR SAFE ANCHOR", entity, str(e))

@_register("stop_movement")
def stop_movement(hinst, entity):
    """
    Descripción
        ACCIÓN: Frenar el movimiento de la entidad y neutralizar la salida de steering.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad cuyos movimientos se detienen.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - Ninguno
    """
    # 1) Poner velocidad lineal a cero y limpiar steering pendiente
    try:
        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
    except Exception as e:
        exception_print("STOP MOVEMENT", entity, str(e))

# ...existing code...
# --------------------
# Healing
# --------------------
@_register("start_heal_tick")
def start_heal_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Inicializar el proceso de curación del enemigo.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad (Enemy) que iniciará la curación.

    Blackboard utilizado/modificado
        - healing (update): bool que indica que la entidad está en proceso de curación.
        - heal_accum (update): acumulador de curación aplicado (px o HP).
        - last_heal_at (update): timestamp del último tick de curación.
        - heal_started_at (update): timestamp en que se inició la curación.

    Parámetros esperados
        - heal_rate_per_sec (float): fracción de max_health curada por segundo (p.ej. 0.05 = 5%/s).
    """
    try:
        # 1) Marcar que la entidad está curándose y guardar timestamps/contadores
        hinst.set_blackboard("healing", True)
        hinst.set_blackboard("heal_accum", 0.0)
        now = time.time()
        hinst.set_blackboard("last_heal_at", now)
        hinst.set_blackboard("heal_started_at", now)
    except Exception as e:
        exception_print("START HEAL TICK", entity, str(e))

@_register("heal_tick")
def heal_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Aplicar curación incremental por tick.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad que recibe la curación.

    Blackboard utilizado/modificado
        - healing (read)        : si no está activo, la acción no hace nada.
        - _dt (read)            : delta time del frame (segundos).
        - heal_accum (update)   : acumula la cantidad total curada desde start_heal_tick.
        - last_heal_at (update) : actualiza timestamp del último tick de curación.

    Parámetros esperados
        - heal_rate_per_sec (float): fracción de max_health a aplicar por segundo.
    """
    try:
        # 1) Solo operar si la curación está activa
        if not hinst.get_blackboard("healing", False):
            return

        # 2) Obtener delta time y parámetros de curación
        dt = float(hinst.get_blackboard("_dt", 0.0))
        if dt <= 0.0:
            return
        rate = float(get_spec_param(hinst, "heal_rate_per_sec", 0.05))

        # 3) Calcular incremento en HP
        max_hp = float(getattr(entity, "max_health", 100.0))
        current_hp = float(getattr(entity, "health", 0.0))
        inc = rate * max_hp * dt

        # 4) Aplicar curación y no superar max_health
        new_hp = min(max_hp, current_hp + inc)
        entity.health = float(new_hp)

        # 5) Actualizar bookkeeping en blackboard
        prev_acc = float(hinst.get_blackboard("heal_accum", 0.0))
        hinst.set_blackboard("heal_accum", prev_acc + inc)
        hinst.set_blackboard("last_heal_at", time.time())
    except Exception as e:
        exception_print("HEAL TICK", entity, str(e))


@_register("stop_heal_tick")
def stop_heal_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Terminar el proceso de curación y limpiar contadores.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad que finaliza la curación.

    Blackboard utilizado/modificado
        - healing (update)      : se pone a False.
        - heal_accum (update)   : se resetea a 0.0.
        - last_heal_at (update) : opcionalmente se puede mantener o limpiar.
        - heal_started_at (remove): opcional limpiar registro de inicio.
        
    Parámetros esperados
        - Ninguno
    """
    try:
        # 1) Limpiar banderas y acumuladores relacionados a la curación
        hinst.set_blackboard("healing", False)
        hinst.set_blackboard("heal_accum", 0.0)
        if "heal_started_at" in hinst.blackboard:
            del hinst.blackboard["heal_started_at"]
        # conservar last_heal_at para diagnósticos, pero es opcional quitarlo
    except Exception as e:
        exception_print("STOP HEAL TICK", entity, str(e))

# -------------------------
# Guardian patrol / Return
# -------------------------
@_register("start_guardian_patrol")
def start_guardian_patrol(hinst, entity):
    """
    Descripción
        ACCIÓN: (Re)asignar el FollowPath basado en el path original de la entidad
        (ruta que protege). Si no existe path original, delega a start_random_patrol.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM con su blackboard.
        - entity (Any): entidad (Enemy) que iniciará/retomará la patrulla guardian.

    Blackboard usado / modificado
        - guardian_original_path (update): referencia al PolylinePath protegido.
        - is_on_guardian_path (update): marca que indica que la entidad sigue la ruta guardian.
        - is_returning_to_zone (update): limpia la marca de retorno si procede.
        - is_at_protection_zone (update): marcado inicial (False hasta verificar llegada).
        - guardian_last_param (update): hint/cache del param más cercano (optimización).

    Parámetros esperados
        - path_offset (float): offset al asignar FollowPath (fallback en entity).
    """
    try:
        original = getattr(entity, "path", None)
        if original is None:
            # No hay ruta definida: crear patrulla aleatoria
            start_random_patrol(hinst, entity)
            return

        # Registrar referencia al path protegido
        hinst.set_blackboard("guardian_original_path", original)

        # Calcular parámetro inicial cercano a la posición actual
        hint = float(hinst.get_blackboard("guardian_last_param", 0.0))
        try:
            start_param = original.get_param(entity.get_pos(), hint)
        except Exception:
            start_param = 0.0

        # Construir FollowPath y asignar
        try:
            entity.follow_path = FollowPath(
                character=entity,
                path=original,
                path_offset=float(get_spec_param(hinst, "path_offset", getattr(entity, "path_offset", 1.0))),
                current_param=float(start_param),
                max_acceleration=getattr(entity, "max_acceleration", 300.0)
            )
            entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING

            # Flags de comportamiento
            hinst.set_blackboard("is_on_guardian_path", True)
            hinst.set_blackboard("is_returning_to_zone", False)
            hinst.set_blackboard("is_at_protection_zone", False)
            # cache del param para optimizaciones posteriores
            hinst.set_blackboard("guardian_last_param", float(start_param))
            # limpiar temp path si existía
            entity.temp_follow_path = None
        except Exception as e:
            exception_print("START GUARDIAN PATROL", entity, f"FollowPath error: {e}")
            # fallback: si no tenemos follow_path válido, usar comportamiento wander
            if getattr(entity, "follow_path", None) is None:
                entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
    except Exception as e:
        exception_print("START GUARDIAN PATROL", entity, str(e))

@_register("return_to_protection_zone")
def return_to_protection_zone(hinst, entity):
    """
    Descripción
        ACCIÓN: Construir y asignar una ruta temporal (temp_follow_path) desde la
        posición actual hacia el punto más cercano del path guardian para volver a la ruta.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): entidad que debe regresar.

    Blackboard usado / modificado
        - guardian_original_path (read): path protegido de referencia.
        - return_target_pos (update): punto objetivo en el path guardian al que regresar.
        - is_returning_to_zone (update): marca que indica que estamos en fase de retorno.
        - is_on_guardian_path (update): se pone False.
        - is_at_protection_zone (update): False hasta llegada.
        - guardian_last_param (update): hint del param cercano al target.

    Parámetros esperados
        - arrival_threshold (float): umbral de llegada (px) usado por check_return_path_finished.
    """
    try:
        manager = get_manager(hinst)
        pathfinder = getattr(manager, "pathfinder", None)

        original = hinst.get_blackboard("guardian_original_path", None) or getattr(entity, "path", None)
        if original is None or pathfinder is None:
            # si no hay referencia a path o pathfinder: considerar ya en zona
            hinst.set_blackboard("is_at_protection_zone", True)
            return

        # 1) calcular punto objetivo sobre el path guardian más cercano a la entidad
        try:
            closest_param = original.get_param(entity.get_pos(), float(hinst.get_blackboard("guardian_last_param", 0.0)))
        except Exception:
            closest_param = 0.0
        target_pos = original.get_position(closest_param)
        hinst.set_blackboard("return_target_pos", (float(target_pos[0]), float(target_pos[1])))
        # actualizar hint cache
        hinst.set_blackboard("guardian_last_param", float(closest_param))

        # 2) pedir ruta desde la posición actual al punto objetivo
        try:
            pts = pathfinder.find_path(entity.get_pos(), target_pos)
        except Exception:
            pts = None

        # 3) si no hay path válido, no forzamos retorno (evitar bloquear)
        if not pts or len(pts) < 2:
            hinst.set_blackboard("is_at_protection_zone", True)
            return

        # 4) crear PolylinePath y FollowPath temporal
        poly = PolylinePath(pts, closed=False)
        try:
            # asegurar primer punto igual a la posición actual para continuidad
            if getattr(poly, "points", None):
                poly.points[0] = tuple(entity.get_pos())
        except Exception:
            # Si no podemos establecer el primer punto en la posición de la entidad, continuar sin generar una excepción.
            pass

        try:
            start_param = poly.get_param(entity.get_pos(), 0.0)
        except Exception:
            start_param = 0.0

        # limpiar follow_path regular para priorizar temp_follow_path
        entity.follow_path = None
        temp_offset = min(float(get_spec_param(hinst, "path_offset", getattr(entity, "path_offset", 1.0))), 1.0)
        entity.temp_follow_path = FollowPath(
            character=entity,
            path=poly,
            path_offset=temp_offset,
            current_param=start_param,
            max_acceleration=getattr(entity, "max_acceleration", 300.0)
        )

        # 5) configurar algoritmo temporal y flags
        entity.algorithm = CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING
        hinst.set_blackboard("is_returning_to_zone", True)
        hinst.set_blackboard("is_on_guardian_path", False)
        hinst.set_blackboard("is_at_protection_zone", False)
    except Exception as e:
        exception_print("RETURN TO PROTECTION ZONE", entity, str(e))
        # en caso de fallo, no dejar al NPC en estado inconsistente
        hinst.set_blackboard("is_at_protection_zone", True)
        hinst.set_blackboard("is_returning_to_zone", False)

@_register("check_return_path_finished")
def check_return_path_finished(hinst, entity):
    """
    Descripción
        ACCIÓN: Comprobar si la ruta de retorno temporal ha finalizado o si la entidad
        ha llegado al punto objetivo en el path guardian. Si llegó, limpiar temp_follow_path
        y restaurar PATH_FOLLOWING sobre el path guardian.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que está ejecutando temp_follow_path.

    Blackboard usado / modificado
        - return_target_pos (read): punto objetivo en el path guardian.
        - is_at_protection_zone (update): se marca True al llegar.
        - is_returning_to_zone (update): se marca False al completar retorno.

    Parámetros esperados
        - arrival_threshold (float): umbral de llegada en px (default 24.0).
    """
    try:
        temp = getattr(entity, "temp_follow_path", None)
        target = hinst.get_blackboard("return_target_pos", None)
        arrival_thresh = float(get_spec_param(hinst, "arrival_threshold", 24.0))

        if temp and target:
            ex, ez = entity.get_pos()
            tx, tz = float(target[0]), float(target[1])
            # 1) llegada por proximidad al objetivo
            if math.hypot(ex - tx, ez - tz) <= arrival_thresh:
                entity.temp_follow_path = None
                entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
                hinst.set_blackboard("is_at_protection_zone", True)
                hinst.set_blackboard("is_returning_to_zone", False)
                return

            # 2) llegada por fin del temp path
            path_obj = getattr(temp, "path", None)
            curp = float(getattr(temp, "current_param", 0.0))
            seg_count = int(getattr(path_obj, "segment_count", 1))
            if path_obj and curp >= (seg_count - 1):
                entity.temp_follow_path = None
                entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
                hinst.set_blackboard("is_at_protection_zone", True)
                hinst.set_blackboard("is_returning_to_zone", False)
                return
        else:
            # no hay temp path: asumimos que estamos en la zona o no hay necesidad de retorno
            hinst.set_blackboard("is_at_protection_zone", True)
            hinst.set_blackboard("is_returning_to_zone", False)
    except Exception as e:
        exception_print("CHECK RETURN PATH FINISHED", entity, str(e))
        # mantener estado conservador: marcar en zona
        hinst.set_blackboard("is_at_protection_zone", True)
        hinst.set_blackboard("is_returning_to_zone", False)

# --------------------
# Boss: return / invocation / regen / ranged helpers
# --------------------
@_register("start_return_to_boss_position")
def start_return_to_boss_position(hinst, entity):
    """
    Descripción
        ACCIÓN: Construir y asignar un temp_follow_path desde la posición actual hasta boss_position.
    
    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard y spec.
        - entity (Any): entidad (Boss) sobre la que opera la acción.

    Blackboard utilizado/modificado
        - return_target_pos (update): destino calculado en boss_position.
        - return_path_requested_at (update): timestamp de la petición de ruta.
        - entity.temp_follow_path (update): FollowPath temporal asignado.
    
    Parámetros esperados
        - boss_position (tuple): posición objetivo (x,z) donde debe reposicionarse el boss.
        - path_offset (float): offset usado al construir FollowPath (opcional).
    """
    # 1) Obtener servicios y parámetros necesarios
    try:
        manager = get_manager(hinst)
        pathfinder = getattr(manager, "pathfinder", None)
        boss_pos = get_spec_param(hinst, "boss_position", None)
        if not boss_pos:
            # 2) Si no hay boss_position, usar posición actual como target seguro
            hinst.set_blackboard("return_target_pos", tuple(entity.get_pos()))
            return

        # 3) Normalizar target y solicitar ruta al pathfinder si está disponible
        target_pos = (float(boss_pos[0]), float(boss_pos[1]))
        hinst.set_blackboard("return_target_pos", target_pos)

        pts = None
        if pathfinder is not None:
            try:
                pts = pathfinder.find_path(entity.get_pos(), target_pos)
            except Exception:
                pts = None

        # 4) Si no hay path válido, crear lista directa start->target
        if not pts or len(pts) < 2:
            pts = [tuple(entity.get_pos()), target_pos]

        # 5) Construir PolylinePath y FollowPath temporal y asignarlo a la entidad
        poly = PolylinePath(pts, closed=False)
        start_param = poly.get_param(entity.get_pos(), 0.0)
        temp_offset = float(get_spec_param(hinst, "path_offset", getattr(entity, "path_offset", 1.0)))
        entity.follow_path = None
        entity.temp_follow_path = FollowPath(
            character=entity,
            path=poly,
            path_offset=temp_offset,
            current_param=start_param,
            max_acceleration=getattr(entity, "max_acceleration", 300.0)
        )
        # 6) Marcar algoritmo temporal y guardar timestamp de la petición
        entity.algorithm = CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING
        hinst.set_blackboard("return_path_requested_at", time.time())
    except Exception as e:
        exception_print("START RETURN TO BOSS POSITION", entity, str(e))

@_register("return_to_boss_tick")
def return_to_boss_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Tick que supervisa el progreso del temp_follow_path hacia boss_position.
        Marca llegada y limpia rutas/algoritmos cuando se alcanza el destino.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad (Boss) que sigue temp_follow_path.

    Blackboard utilizado/modificado
        - return_target_pos (read): posición objetivo establecida en start_return_to_boss_position.
        - return_arrived_at (update): timestamp cuando se detecta la llegada.
        - entity.temp_follow_path / entity.follow_path (update): limpieza al llegar.

    Parámetros esperados
        - arrival_threshold (float): umbral en px para considerar llegada (default: arrival_threshold spec).
    """
    try:
        # 1) Reusar lógica de check: si estamos cerca del target, detener temp path
        temp = getattr(entity, "temp_follow_path", None)
        target = hinst.get_blackboard("return_target_pos", None)
        arrival_thresh = float(get_spec_param(hinst, "arrival_threshold", 24.0))

        if temp and target:
            ex, ez = entity.get_pos()
            tx, tz = float(target[0]), float(target[1])
            if math.hypot(ex - tx, ez - tz) <= arrival_thresh:
                # 2) Llegada: limpiar temp path y fijar algoritmo de parada
                entity.temp_follow_path = None
                entity.follow_path = None
                entity.algorithm = CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC
                hinst.set_blackboard("return_arrived_at", time.time())
                return
        else:
            # 3) Si no hay temp path o target, marcar como arrived por seguridad
            hinst.set_blackboard("return_arrived_at", time.time())
    except Exception as e:
        exception_print("RETURN TO BOSS TICK", entity, str(e))

@_register("stop_return_to_boss_position")
def stop_return_to_boss_position(hinst, entity):
    """
    Descripción
        ACCIÓN: Limpiar temp_follow_path y restaurar algoritmo base al salir del estado Reposicionar.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad (Boss) que termina de reposicionarse.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - Ninguno
    """
    try:
        # 1) Eliminar temp path y seleccionar algoritmo fallback
        entity.temp_follow_path = None
        entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
    except Exception as e:
        exception_print("STOP RETURN TO BOSS POSITION", entity, str(e))

@_register("start_invocation")
def start_invocation(hinst, entity):
    """
    Descripción
        ACCIÓN: Inicializar el proceso de invocación.
        - Prepara bookkeeping y pone al boss en FACE mirando al player mientras spawnan aliados.

    Argumentos
        - hinst (HSMInstance): instancia HSM que contiene el blackboard y spec.
        - entity (Any): entidad (Boss) que inicia la invocación.

    Blackboard utilizado/modificado
        - invocation_started_at (update): timestamp de inicio de invocación.
        - invocation_spawned_count (update): contador de aliados spawnados.
        - invocation_entities (update): lista de referencias a aliados spawnados.
        - invocation_prev_algorithm (update): algoritmo previo guardado para restaurar al salir.

    Parámetros esperados
        - allies_for_invocation (int): número total de aliados a generar.
        - time_for_invocation (float): duración total de la fase de invocación en segundos.
        - timeout_invocations (float): lifetime en segundos para cada aliado invocado.
    """
    try:
        # 1) Inicial bookkeeping para la invocación
        hinst.set_blackboard("invocation_started_at", time.time())
        hinst.set_blackboard("invocation_spawned_count", 0)
        hinst.set_blackboard("invocation_entities", [])
        hinst.set_blackboard("invocation_prev_algorithm", getattr(entity, "algorithm", None))

        # 2) Asegurar que el boss quede estático y cara al player (FACE)
        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        player = get_player(hinst)
        try:
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
            if player:
                entity.face.target = player
            else:
                last = hinst.get_blackboard("last_known_player_pos", None)
                if last:
                    tgt = Kinematic(position=tuple(last), orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
                    entity.face.target = tgt
        except Exception as e:
            exception_print("START INVOCATION", entity, f"Setting face target: {e}")
    except Exception as e:
        exception_print("START INVOCATION", entity, str(e))

@_register("invocation_tick")
def invocation_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Durante la invocación spawnear aliados gradualmente según time_for_invocation.
        - Usar manager.spawn_enemy cuando esté disponible.
        - Registrar cada spawn en invocation_entities y mantener contador.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que ejecuta la invocación.

    Blackboard utilizado/modificado
        - invocation_started_at (read): timestamp de inicio de invocación.
        - invocation_spawned_count (read/update): contador de aliados spawnados.
        - invocation_entities (read/update): lista acumulada de referencias a invocados.
        - invocation_last_spawn_at (update): timestamp del último spawn (diagnóstico).

    Parámetros esperados
        - allies_for_invocation (int): total de aliados a crear.
        - time_for_invocation (float): duración en segundos para distribuir los spawns.
        - timeout_invocations (float): lifetime de cada aliado en segundos.
    """
    try:
        mgr = get_manager(hinst)
        total = int(get_spec_param(hinst, "allies_for_invocation", 3))
        duration = float(get_spec_param(hinst, "time_for_invocation", 6.0))
        timeout = float(get_spec_param(hinst, "timeout_invocations", 14.0))
        start = hinst.get_blackboard("invocation_started_at", None)
        spawned = int(hinst.get_blackboard("invocation_spawned_count", 0))
        if not start:
            return

        # 1) Calcular interval determinista y spawnear cuando corresponda
        if spawned < total:
            interval = max(1e-6, float(duration) / float(total))
            next_spawn_time = float(start) + (spawned + 1) * interval
            if time.time() >= next_spawn_time:
                spawned_spec = {
                    "type": "gargant-soldier",
                    "algorithm": CONF.ALG.ALGORITHM.PURSUE,
                    "behavior": None,
                    "lifetime": timeout
                }
                spawned_ref = None
                try:
                    if mgr and getattr(mgr, "spawn_enemy", None):
                        spawned_ref = mgr.spawn_enemy(spawned_spec, entity)
                    else:
                        spawned_ref = spawned_spec
                except Exception as e:
                    exception_print("INVOCATION SPAWN", entity, f"spawn error: {e}")
                    spawned_ref = spawned_spec

                arr = hinst.get_blackboard("invocation_entities", []) or []
                arr.append(spawned_ref)
                hinst.set_blackboard("invocation_entities", arr)
                hinst.set_blackboard("invocation_spawned_count", spawned + 1)
                hinst.set_blackboard("invocation_last_spawn_at", time.time())
    except Exception as e:
        exception_print("INVOCATION TICK", entity, str(e))

@_register("stop_invocation")
def stop_invocation(hinst, entity):
    """
    Descripción
        ACCIÓN: Finalizar el proceso de invocación y limpiar bookkeeping.
        - Restaurar algoritmo previo y limpiar face target.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que termina la invocación.

    Blackboard utilizado/modificado
        - invocation_prev_algorithm (read/remove): algoritmo previo restaurado.
        - invocation_started_at / invocation_spawned_count / invocation_last_spawn_at (remove): limpieza.
        - invocation_entities (read): lista de entidades creadas (no se elimina aquí).

    Parámetros esperados
        - Ninguno
    """
    try:
        prev = hinst.get_blackboard("invocation_prev_algorithm", None)
        if prev:
            try:
                entity.algorithm = prev
            except Exception:
                entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC
            try:
                del hinst.blackboard["invocation_prev_algorithm"]
            except Exception as e:
                exception_print("STOP INVOCATION", entity, str(e))

        entity.face.target = None
        
        for k in ("invocation_started_at", "invocation_spawned_count", "invocation_last_spawn_at"):
            if k in hinst.blackboard:
                del hinst.blackboard[k]
    except Exception as e:
        exception_print("STOP INVOCATION", entity, str(e))

@_register("start_regeneration")
def start_regeneration(hinst, entity):
    """
    Descripción
        ACCIÓN: Iniciar regeneración en boss_position; asegurar que el boss quede estático
        y mirando al jugador (FACE). Preparar bookkeeping para regen.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que iniciará regeneración.

    Blackboard utilizado/modificado
        - regen_started_at (update): timestamp de inicio de regeneración.
        - regen_total_amount (update): cantidad total de HP a recuperar.
        - regen_accum (update): acumulado actual de HP recuperado.

    Parámetros esperados
        - perc_regenerate (float): fracción de max_health a recuperar durante la fase.
        - time_for_regeneration (float): duración en segundos de la regeneración.
        - boss_position (tuple): posición absoluta donde debe ocurrir la regeneración.
    """
    try:
        perc = float(get_spec_param(hinst, "perc_regenerate", 0.18))
        max_hp = float(getattr(entity, "max_health", 100.0))
        total = perc * max_hp
        hinst.set_blackboard("regen_started_at", time.time())
        hinst.set_blackboard("regen_total_amount", float(total))
        hinst.set_blackboard("regen_accum", 0.0)

        # 1) Normalizar cinemática y limpiar rutas residuales para evitar micro-desplazamientos
        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
        entity.follow_path = None
        entity.temp_follow_path = None

        # 2) Poner algoritmo FACE y fijar target al player o a boss_position como fallback
        try:
            player = get_player(hinst)
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
            if player:
                entity.face.target = player
            else:
                boss_pos = get_spec_param(hinst, "boss_position", None)
                if boss_pos:
                    tgt = Kinematic(position=(float(boss_pos[0]), float(boss_pos[1])), orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
                    entity.face.target = tgt
        except Exception as e:
            exception_print("START REGENERATION", entity, f"Setting face target: {e}")

    except Exception as e:
        exception_print("START REGENERATION", entity, str(e))

@_register("regen_tick")
def regen_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Aplicar curación incremental durante la fase de regeneración.
        - Usa _dt del blackboard para calcular la cantidad a aplicar por tick.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que recibe la regeneración.

    Blackboard utilizado/modificado
        - regen_started_at (read): indica si la regeneración está activa.
        - regen_total_amount (read): total de HP a recuperar.
        - regen_accum (update): acumulador de HP aplicado.
        - regen_finished_at (update): timestamp marcado cuando termina la regeneración.

    Parámetros esperados
        - time_for_regeneration (float): duración total de la regeneración (s).
        - perc_regenerate (float): porcentaje de max_health a recuperar.
        - _dt (float): delta time del frame (debe estar en blackboard).
    """
    try:
        if not hinst.get_blackboard("regen_started_at", None):
            return
        total = float(hinst.get_blackboard("regen_total_amount", 0.0) or 0.0)
        if total <= 0.0:
            return
        dt = float(hinst.get_blackboard("_dt", 0.0) or 0.0)
        if dt <= 0.0:
            return
        duration = float(get_spec_param(hinst, "time_for_regeneration", 8.0))
        per_sec = total / max(1e-6, duration)
        inc = per_sec * dt
        prev = float(hinst.get_blackboard("regen_accum", 0.0) or 0.0)
        to_apply = min(inc, total - prev)
        if to_apply <= 0.0:
            return
        # 1) Aplicar curación a la entidad y actualizar bookkeeping
        max_hp = float(getattr(entity, "max_health", 100.0) or 100.0)
        entity.health = min(max_hp, float(getattr(entity, "health", 0.0)) + to_apply)
        hinst.set_blackboard("regen_accum", prev + to_apply)
        if (hinst.get_blackboard("regen_accum", 0.0) or 0.0) >= total:
            hinst.set_blackboard("regen_finished_at", time.time())
    except Exception as e:
        exception_print("REGEN TICK", entity, str(e))

@_register("stop_regeneration")
def stop_regeneration(hinst, entity):
    """
    Descripción
        ACCIÓN: Finalizar la fase de regeneración y limpiar claves del blackboard.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que finaliza regeneración.

    Blackboard utilizado/modificado
        - regen_started_at / regen_total_amount / regen_accum (remove): se eliminan las claves relacionadas.

    Parámetros esperados
        - Ninguno
    """
    try:
        if "regen_started_at" in hinst.blackboard:
            del hinst.blackboard["regen_started_at"]
        if "regen_total_amount" in hinst.blackboard:
            del hinst.blackboard["regen_total_amount"]
        if "regen_accum" in hinst.blackboard:
            del hinst.blackboard["regen_accum"]
    except Exception as e:
        exception_print("STOP REGENERATION", entity, str(e))

@_register("reset_lost_health_accum")
def reset_lost_health_accum(hinst, entity):
    """
    Descripción
        ACCIÓN: Resetea la referencia de vida al final de una restauración o regeneración.
        - Guarda health_at_last_restore = current health en el blackboard.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): entidad cuyo snapshot de vida se resetea.

    Blackboard utilizado/modificado
        - health_at_last_restore (update): vida actual registrada como referencia de restauración.

    Parámetros esperados
        - Ninguno
    """
    try:
        hp = float(getattr(entity, "health", 0.0))
        hinst.set_blackboard("health_at_last_restore", float(hp))
    except Exception as e:
        exception_print("RESET LOST HEALTH ACCUM", entity, str(e))

@_register("record_health_tick")
def record_health_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Mantener dos snapshots de vida para detectar daños recientes.
        - last_health_snapshot_prev : vida al inicio del tick anterior.
        - last_health_snapshot      : vida actual (snapshot de este tick).

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): entidad cuya vida se registra.

    Blackboard utilizado/modificado
        - last_health_snapshot_prev (update): vida del tick previo.
        - last_health_snapshot (update): vida actual.

    Parámetros esperados
        - Ninguno
    """
    try:
        prev_snapshot = hinst.get_blackboard("last_health_snapshot", None)
        if prev_snapshot is None:
            prev_snapshot = float(getattr(entity, "health", 0.0) or 0.0)
        hinst.set_blackboard("last_health_snapshot_prev", float(prev_snapshot))

        current_hp = float(getattr(entity, "health", 0.0) or 0.0)
        hinst.set_blackboard("last_health_snapshot", float(current_hp))
    except Exception as e:
        exception_print("RECORD HEALTH TICK", entity, str(e))

# --------------------
# Attention / Atento helpers
# --------------------
@_register("start_attention_facing")
def start_attention_facing(hinst, entity):
    """
    Descripción
        ACCIÓN: Inicializar el objetivo de facing para el estado 'Atento'.
        - Crea y asigna un target Kinematic en la dirección especificada y activa FACE.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): entidad que entra en estado Atento.

    Blackboard utilizado/modificado
        - attention_face_target (update): Kinematic objetivo almacenado para facing.

    Parámetros esperados
        - attention_direction (str): "N"|"S"|"E"|"W" (opcional).
        - attention_distance (float): distancia en px para colocar el target (default 10.0).
    """
    try:
        dir_param = get_spec_param(hinst, "attention_direction", "N")
        distance = float(get_spec_param(hinst, "attention_distance", 10.0))
    
        dd = dir_param.strip().upper()
        card_map = {"E": 0.0, "N": math.pi/2, "W": math.pi, "S": -math.pi/2}
        angle_rad = card_map.get(dd, None)
        if angle_rad is None:
            angle_rad = float(getattr(entity, "orientation", 0.0))

        ex, ez = entity.get_pos()
        tx = ex + math.cos(angle_rad) * distance
        tz = ez + math.sin(angle_rad) * distance

        # 1) Normalizar estado cinemático para evitar giros bruscos residuales
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
        entity.rotation = 0.0

        # 2) Crear Kinematic target y asignarlo como objetivo de face
        try:
            tgt = Kinematic(position=(float(tx), float(tz)), orientation=angle_rad, velocity=(0.0, 0.0), rotation=0.0)
            hinst.set_blackboard("attention_face_target", tgt)
            entity.face.target = tgt
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
        except Exception as e:
            exception_print("START ATTENTION FACING", entity, f"Setting face target: {e}")
    except Exception as e:
        exception_print("START ATTENTION FACING", entity, str(e))

# --------------------
# Boss ranged attack
# --------------------
@_register("start_boss_range_attack_mode")
def start_boss_range_attack_mode(hinst, entity):
    """
    Descripción
        ACCIÓN: Inicializar modo de ataque a distancia.
        - Pone al boss estático, guarda algoritmo previo y activa FACE mirando al player.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que cambia a modo ranged.

    Blackboard utilizado/modificado
        - boss_range_last_at (update): timestamp del último ataque (inicializado a 0).
        - boss_range_cooldown (update): cooldown del ataque (se establece desde spec).
        - boss_prev_algorithm (update): algoritmo previo guardado.

    Parámetros esperados
        - stomp_cooldown (float): cooldown entre ataques a distancia.
        - ranged_attack_range (float): radio del efecto AOE a usar en boss_range_attack_tick.
    """
    try:
        hinst.set_blackboard("boss_range_last_at", 0.0)
        hinst.set_blackboard("boss_range_cooldown", float(get_spec_param(hinst, "stomp_cooldown", 6.0)))

        prev_alg = getattr(entity, "algorithm", None)
        hinst.set_blackboard("boss_prev_algorithm", prev_alg)

        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
        entity.rotation = 0.0

        try:
            player = get_player(hinst)
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
            if player:
                entity.face.target = player
            else:
                last = hinst.get_blackboard("last_known_player_pos", None)
                if last:
                    tgt = Kinematic(position=tuple(last), orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
                    entity.face.target = tgt
        except Exception as e:
            exception_print("START BOSS RANGE ATTACK MODE", entity, f"Setting face target: {e}")
    except Exception as e:
        exception_print("START BOSS RANGE ATTACK MODE", entity, str(e))

@_register("boss_range_attack_tick")
def boss_range_attack_tick(hinst, entity):
    """
    Descripción
        ACCIÓN: Ejecutar ataque de rango AOE simple manteniendo FACE y sin movimiento.
        - Cuando el cooldown expira, genera un efecto mediante manager.spawn_attack_effect
          o registra en blackboard si el manager no está presente.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss en modo ranged.

    Blackboard utilizado/modificado
        - boss_range_last_at (read/update): timestamp del último ataque.
        - boss_range_cooldown (read): cooldown entre ataques.
        - last_boss_range_effect (update): fallback si no se pudo usar manager.

    Parámetros esperados
        - ranged_attack_range (float): radio del AOE a aplicar.
        - stomp_cooldown (float): cooldown entre ataques.
    """
    try:
        player = get_player(hinst)
        if not player:
            return

        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        try:
            entity.face.target = player
        except Exception:
            entity.face.target = Kinematic(position=player.get_pos(), orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)

        last = float(hinst.get_blackboard("boss_range_last_at", 0.0))
        cd = float(hinst.get_blackboard("boss_range_cooldown", get_spec_param(hinst, "stomp_cooldown", 6.0)))
        now = time.time()
        if now - last < cd:
            return

        mgr = get_manager(hinst)
        pos = player.get_pos()
        try:
            if mgr and getattr(mgr, "spawn_attack_effect", None):
                mgr.spawn_attack_effect("boss_aoe_circle", position=pos, radius=float(get_spec_param(hinst, "ranged_attack_range", 220.0)))
            else:
                hinst.set_blackboard("last_boss_range_effect", (pos, float(get_spec_param(hinst, "ranged_attack_range", 220.0))))
        except Exception as e:
            exception_print("BOSS RANGE ATTACK TICK", entity, f"effect spawn error: {e}")

        hinst.set_blackboard("boss_range_last_at", now)
    except Exception as e:
        exception_print("BOSS RANGE ATTACK TICK", entity, str(e))

@_register("stop_boss_range_attack_mode")
def stop_boss_range_attack_mode(hinst, entity):
    """
    Descripción
        ACCIÓN: Limpiar el modo de ataque a distancia y restaurar algoritmo previo.
        - Limpia face target y borra claves relacionadas del blackboard.

    Argumentos
        - hinst (HSMInstance): instancia HSM.
        - entity (Any): boss que sale del modo ranged.

    Blackboard utilizado/modificado
        - boss_prev_algorithm (read/remove): algoritmo previo restaurado.
        - boss_range_last_at / boss_range_cooldown / last_boss_range_effect (remove): limpieza.

    Parámetros esperados
        - Ninguno
    """
    try:
        prev = hinst.get_blackboard("boss_prev_algorithm", None)
        if prev:
            entity.algorithm = prev
        else:
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_DYNAMIC

        entity.face.target = None
        
        for k in ("boss_range_last_at", "boss_range_cooldown", "boss_prev_algorithm", "last_boss_range_effect"):
            if k in hinst.blackboard:
                del hinst.blackboard[k]
    except Exception as e:
        exception_print("STOP BOSS RANGE ATTACK MODE", entity, str(e))
        
# ----------------------------
# Behavior flags / monitoring
# ----------------------------
@_register("set_behavior_flag_fleeing")
def set_behavior_flag_fleeing(hinst, entity):
    """
    Descripción
        ACCIÓN: Marcar en el blackboard que la entidad está en estado de huida.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard.
        - entity (Any): entidad (Enemy) sobre la que se aplica la marca.

    Blackboard utilizado/modificado
        - is_fleeing (update): flag booleana que indica que la entidad está huyendo.

    Parámetros esperados
        - Ninguno
    """
    # 1) Establecer la bandera is_fleeing en el blackboard
    try:
        hinst.set_blackboard("is_fleeing", True)
    except Exception as e:
        exception_print("SET BEHAVIOR FLAG FLEEING", entity, str(e))

@_register("clear_behavior_flag_fleeing")
def clear_behavior_flag_fleeing(hinst, entity):
    """
    Descripción
        ACCIÓN: Quitar la marca de huida del blackboard.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad sobre la que se quita la marca.

    Blackboard utilizado/modificado
        - is_fleeing (update): se pone a False.

    Parámetros esperados
        - Ninguno
    """
    # 1) Limpiar la bandera is_fleeing
    try:
        hinst.set_blackboard("is_fleeing", False)
    except Exception as e:
        exception_print("CLEAR BEHAVIOR FLAG FLEEING", entity, str(e))

@_register("monitor_player_presence")
def monitor_player_presence(hinst, entity):
    """
    Descripción
        ACCIÓN: Verificar periódicamente la presencia del jugador y actualizar métricas
        en el blackboard para uso de condiciones y debugging.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que ejecuta la monitorización.

    Blackboard utilizado/modificado
        - last_player_visible_at (read): timestamp de la última vez que se vio al jugador.
        - time_since_player_seen (update): tiempo transcurrido desde la última visibilidad.

    Parámetros esperados
        - Ninguno
    """
    # 1) Ejecutar la comprobación throttled de visibilidad para mantener blackboard actualizado
    try:
        throttle_check_player_visibility(hinst, entity)

        # 2) Calcular y almacenar tiempo desde la última vez que se vio al jugador
        last_seen = hinst.get_blackboard("last_player_visible_at", None)
        if last_seen:
            hinst.set_blackboard("time_since_player_seen", time.time() - float(last_seen))
        else:
            # explícito: no se ha visto al jugador recientemente
            hinst.set_blackboard("time_since_player_seen", None)
    except Exception as e:
        exception_print("MONITOR PLAYER PRESENCE", entity, str(e))