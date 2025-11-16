"""
Acciones HSM (src/ai/actions.py) — documentación y refactorización (en español)

Descripción general
-------------------
Este módulo expone un registro de acciones (ACTIONS) utilizadas por las HSM.
Cada acción tiene la firma: fn(hinst, entity) donde:
 - hinst: instancia runtime de la HSM (HSMInstance).
 - entity: la entidad (Enemy) sobre la que opera la acción.

Objetivos y convenciones
- Código en inglés; documentación y docstrings en español (AGENTS.md).
- Las acciones deben ser pequeñas, deterministas y delegar lógica de dominio a utilitarios.
- Uso de `ai.utils.get_spec_param/get_manager/get_player` para acceder a parámetros y servicios.
- Manejo robusto de excepciones: no propagar errores al bucle principal del juego.
- Nombres de parámetros en spec: usar `heal_rate_per_sec`, `patrol_path_nodes`, etc.

Estructura
- ACTIONS: dict mapping string -> callable
- Decorador @_register(name) para registrar acciones
- Acciones agrupadas por responsabilidad:
  - patrol / follow path
  - visibility / bookkeeping
  - pursue / attack
  - evade / flee
  - face / healing
  - flags / monitoring

Notas de mantenimiento
- Preferir mover helpers reutilizables a ai.utils y mantener aquí sólo acciones.
- Si introduces nuevas acciones, documentarlas con su comportamiento esperado y keys de blackboard que usan/modifican.
"""
import random
import math
import time
from typing import Dict, Callable, Any, List, Optional

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.path_following import FollowPath
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
        - hinst (HSMInstance) : instancia de la HSM que contiene el blackboard.
        - entity (Any) : entidad (Enemy) sobre la que se crea la patrulla.
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
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return

        # 3) Limpiar cualquier follow_path previo para forzar reconstrucción
        entity.follow_path = None

        # 4) Obtener parámetros y buscar ruta en navmesh
        desired_nodes = int(get_spec_param(hinst, "patrol_path_nodes", 20))
        pts = _find_best_patrol_path(pathfinder, entity.get_pos(), desired_nodes)

        # 5) Si no hay puntos adecuados -> fallback a wander
        if not pts:
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return

        # 6) Construir PolylinePath y FollowPath de forma segura
        poly = PolylinePath(pts, closed=False)
        try:
            entity.follow_path = FollowPath(
                character=entity,
                path=poly,
                path_offset=get_spec_param(hinst, "path_offset", getattr(entity, "path_offset", 1.0)),
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
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
    except Exception as e:
        exception_print("START RANDOM PATROL", entity, str(e))

@_register("patrol_tick")
def patrol_tick(hinst, entity):
    """
    Descripción
        FUNCIÓN: Tick periódico que mantiene o solicita una nueva patrulla aleatoria.

    Argumentos
        - hinst (HSMInstance) : instancia de la HSM.
        - entity (Any) : entidad que ejecuta la patrulla.
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
            seg_count = int(getattr(path_obj, "segment_count", 0) or 0)
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
        FUNCIÓN: Detener la patrulla activa y seleccionar algoritmo fallback.

    Argumentos
        - hinst (HSMInstance) : instancia de la HSM.
        - entity (Any) : entidad cuya patrulla se detiene.
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
    Revisa visibilidad del jugador con throttling.
    Actualiza en blackboard: last_known_player_pos, player_visible, last_player_visible_at.
    """
    try:
        player = get_player(hinst)
        if not player:
            return
        throttle = float(get_spec_param(hinst, "check_los_throttle", 0.25))
        last = float(hinst.get_blackboard("last_los_check", 0.0))
        now = time.time()
        if now - last < throttle:
            return
        hinst.set_blackboard("last_los_check", now)

        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dx, dz = px - ex, pz - ez
        dist = math.hypot(dx, dz)
        vision = float(get_spec_param(hinst, "vision_range", 300.0))

        if dist > vision:
            hinst.set_blackboard("player_visible", False)
            return

        fov_deg = float(get_spec_param(hinst, "vision_fov_deg", 120.0))
        half_fov_rad = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
        try:
            angle_to_player = math.atan2(dz, dx)
            facing = float(getattr(entity, "orientation", 0.0))
            diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) <= half_fov_rad:
                hinst.set_blackboard("last_known_player_pos", (float(px), float(pz)))
                hinst.set_blackboard("player_visible", True)
                hinst.set_blackboard("last_player_visible_at", now)
                return
        except Exception as e:
            exception_print("THROTTLE CHECK PLAYER VISIBILITY", entity, f"FOV error: {e}")

        hinst.set_blackboard("player_visible", False)
    except Exception as e:
        exception_print("THROTTLE CHECK PLAYER VISIBILITY", entity, str(e))

# --------------------
# Pursue / Attack
# --------------------
@_register("start_pursue_target")
def start_pursue_target(hinst, entity):
    """
    Activar algoritmo de persecución hacia el jugador.
    Blackboard modificado: pursuing, last_known_player_pos, player_visible_since
    """
    try:
        player = get_player(hinst)
        if not player:
            return
        entity.algorithm = CONF.ALG.ALGORITHM.PURSUE
        try:
            entity.pursue.target = player
        except Exception:
            # algunos objetos pueden no exponer .pursue asignable
            pass
        hinst.set_blackboard("pursuing", True)
        hinst.set_blackboard("last_known_player_pos", player.get_pos())
        hinst.set_blackboard("player_visible_since", time.time())
    except Exception as e:
        exception_print("START PURSUE TARGET", entity, str(e))

@_register("pursue_tick")
def pursue_tick(hinst, entity):
    """Tick de persecución: refresca visibilidad y mantiene last_known. Muy ligero."""
    try:
        throttle_check_player_visibility(hinst, entity)
    except Exception as e:
        exception_print("PURSUE TICK", entity, str(e))

@_register("stop_pursue")
def stop_pursue(hinst, entity):
    """Detener persecución: limpiar flag y volver a patrullar/andar."""
    try:
        hinst.set_blackboard("pursuing", False)
        stop_patrol(hinst, entity)
    except Exception as e:
        exception_print("STOP PURSUE", entity, str(e))

@_register("try_melee_attack")
def try_melee_attack(hinst, entity):
    """
    Intento de ataque cuerpo a cuerpo.
    - Comprueba distancia respecto a attack_range y dispara animación.
    - Aplicación de daño manejada por Enemy.update.
    """
    try:
        player = get_player(hinst)
        if not player:
            return
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)
        spec = hinst.get_blackboard("_spec_params", {}) or {}
        attack_r = float(get_spec_param(hinst, "attack_range", spec.get("attack_range", 48.0)))
        if dist <= attack_r:
            try:
                from characters.animation import set_animation_state
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
    Iniciar huida: guardar algoritmo previo, cambiar a LOOK_WHERE_YOURE_GOING y
    marcar is_fleeing en blackboard.
    """
    try:
        player = get_player(hinst)
        if not player:
            return
        prev_alg = getattr(entity, "algorithm", None)
        hinst.set_blackboard("prev_algorithm", prev_alg)
        try:
            entity.look_where.target = player
        except Exception:
            pass
        entity.algorithm = CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING
        hinst.set_blackboard("is_fleeing", True)
    except Exception as e:
        exception_print("START EVADE FROM PLAYER", entity, str(e))

@_register("evade_tick")
def evade_tick(hinst, entity):
    """Tick de huida: mantener distancia al jugador en blackboard."""
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
    """Finalizar huida: restaurar algoritmo previo o fallback a patrulla."""
    try:
        hinst.set_blackboard("is_fleeing", False)
        prev = hinst.get_blackboard("prev_algorithm", None)
        if prev:
            entity.algorithm = prev
        else:
            stop_patrol(hinst, entity)
    except Exception as e:
        exception_print("STOP EVADE", entity, str(e))

# --------------------
# Face / Safe anchor / movement helpers
# --------------------
@_register("face_towards_safe_anchor")
def face_towards_safe_anchor(hinst, entity):
    """
    Orientar la entidad hacia anchor seguro o hacia jugador si está dentro de un rango extendido.
    - Actualiza curing_face_target en blackboard.
    - Usa last_known_player_pos y safe_anchor en blackboard.
    """
    try:
        player = get_player(hinst)
        sd = float(get_spec_param(hinst, "safe_distance", 200.0))
        vision = float(get_spec_param(hinst, "vision_range", 300.0))
        fov_deg = float(get_spec_param(hinst, "vision_fov_deg", 120.0))
        face_mult = float(get_spec_param(hinst, "face_range_multiplier", 1.5))
        face_range = vision * face_mult
        half_fov_rad = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)

        last_known = hinst.get_blackboard("last_known_player_pos", None)
        safe = hinst.get_blackboard("safe_anchor", None)

        if not safe:
            ex, ez = entity.get_pos()
            if player:
                px, pz = player.get_pos()
                dx = ex - px
                dz = ez - pz
                dist = math.hypot(dx, dz) or 1.0
                sx = ex + dx / dist * sd
                sz = ez + dz / dist * sd
            else:
                ang = random.random() * (2 * math.pi)
                r = 80.0
                sx = ex + math.cos(ang) * r
                sz = ez + math.sin(ang) * r
            safe = (float(sx), float(sz))
            hinst.set_blackboard("safe_anchor", safe)

        if player:
            ex, ez = entity.get_pos()
            px, pz = player.get_pos()
            dx, dz = px - ex, pz - ez
            dist = math.hypot(dx, dz)
            try:
                angle_to_player = math.atan2(dz, dx)
                facing = float(getattr(entity, "orientation", 0.0))
                diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
                if dist <= face_range and abs(diff) <= half_fov_rad:
                    entity.face.target = player
                    entity.algorithm = CONF.ALG.ALGORITHM.FACE
                    hinst.set_blackboard("curing_face_target", player.get_pos())
                    return
            except Exception as e:
                exception_print("FACE TOWARDS SAFE ANCHOR", entity, f"FOV error: {e}")

        target_pos = last_known if last_known is not None else safe
        try:
            tgt = Kinematic(position=target_pos, orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
            entity.face.target = tgt
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
            hinst.set_blackboard("curing_face_target", target_pos)
        except Exception as e:
            exception_print("FACE TOWARDS SAFE ANCHOR", entity, f"Setting face target error: {e}")
    except Exception as e:
        exception_print("FACE TOWARDS SAFE ANCHOR", entity, str(e))

@_register("clear_safe_anchor")
def clear_safe_anchor(hinst, entity):
    """Limpiar safe_anchor y restaurar objetivo de face (player si existe)."""
    try:
        if "safe_anchor" in hinst.blackboard:
            del hinst.blackboard["safe_anchor"]
        if "curing_face_target" in hinst.blackboard:
            del hinst.blackboard["curing_face_target"]
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
    """Frenar movimiento: poner velocidad a cero y steering pending a neutral."""
    try:
        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
    except Exception as e:
        exception_print("STOP MOVEMENT", entity, str(e))

# --------------------
# Healing
# --------------------
@_register("start_heal_tick")
def start_heal_tick(hinst, entity):
    """Inicializar curación (bandera y timestamps/contadores)."""
    try:
        hinst.set_blackboard("healing", True)
        hinst.set_blackboard("heal_accum", 0.0)
        hinst.set_blackboard("last_heal_at", time.time())
    except Exception as e:
        exception_print("START HEAL TICK", entity, str(e))

@_register("heal_tick")
def heal_tick(hinst, entity):
    """
    Aplicar curación por tick.
    - Usa spec param 'heal_rate_per_sec' (fracción de max_health por segundo).
    """
    try:
        if not hinst.get_blackboard("healing", False):
            return
        dt = float(hinst.get_blackboard("_dt", 0.0))
        rate = float(get_spec_param(hinst, "heal_rate_per_sec", 0.10))
        max_hp = float(getattr(entity, "max_health", 100.0) or 100.0)
        if max_hp <= 0 or dt <= 0.0:
            return
        inc = rate * max_hp * dt
        entity.health = min(max_hp, float(getattr(entity, "health", 0.0) + inc))
    except Exception as e:
        exception_print("HEAL TICK", entity, str(e))

@_register("stop_heal_tick")
def stop_heal_tick(hinst, entity):
    """Detener curación y limpiar acumuladores."""
    try:
        hinst.set_blackboard("healing", False)
        hinst.set_blackboard("heal_accum", 0.0)
    except Exception as e:
        exception_print("STOP HEAL TICK", entity, str(e))

# --------------------
# Guardian patrol / Return
# --------------------
@_register("start_guardian_patrol")
def start_guardian_patrol(hinst, entity):
    """
    Reasignar FollowPath basado en entity.path (ruta protegida).
    Si no existe, fallback a start_random_patrol.
    Blackboard modificado: guardian_original_path, is_on_guardian_path, ...
    """
    try:
        original = getattr(entity, "path", None)
        if original is None:
            start_random_patrol(hinst, entity)
            return
        hinst.set_blackboard("guardian_original_path", original)
        try:
            start_param = original.get_param(entity.get_pos(), 0.0)
        except Exception:
            start_param = 0.0
        try:
            entity.follow_path = FollowPath(
                character=entity,
                path=original,
                path_offset=get_spec_param(hinst, "path_offset", getattr(entity, "path_offset", 1.0)),
                current_param=start_param,
                max_acceleration=getattr(entity, "max_acceleration", 300.0)
            )
            entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
            hinst.set_blackboard("is_on_guardian_path", True)
            hinst.set_blackboard("is_returning_to_zone", False)
            hinst.set_blackboard("is_at_protection_zone", False)
            entity.temp_follow_path = None
        except Exception as e:
            exception_print("START GUARDIAN PATROL", entity, f"FollowPath error: {e}")
            if getattr(entity, "follow_path", None) is None:
                entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
    except Exception as e:
        exception_print("START GUARDIAN PATROL", entity, str(e))

@_register("return_to_protection_zone")
def return_to_protection_zone(hinst, entity):
    """
    Construir ruta temporal hacia el punto más cercano en la ruta protegida.
    No escribe flags de cooldown; solo:
      - asigna entity.temp_follow_path,
      - setea is_returning_to_zone/is_on_guardian_path/is_at_protection_zone.
    """
    try:
        manager = get_manager(hinst)
        pathfinder = getattr(manager, "pathfinder", None)

        original = hinst.get_blackboard("guardian_original_path", None) or getattr(entity, "path", None)
        if original is None or pathfinder is None:
            hinst.set_blackboard("is_at_protection_zone", True)
            return

        closest_param = original.get_param(entity.get_pos(), 0.0)
        target_pos = original.get_position(closest_param)
        hinst.set_blackboard("return_target_pos", (float(target_pos[0]), float(target_pos[1])))

        pts = pathfinder.find_path(entity.get_pos(), target_pos)
        if not pts or len(pts) < 2:
            hinst.set_blackboard("is_at_protection_zone", True)
            return

        poly = PolylinePath(pts, closed=False)
        try:
            if poly.points:
                poly.points[0] = tuple(entity.get_pos())
        except Exception:
            pass

        try:
            start_param = poly.get_param(entity.get_pos(), 0.0)
        except Exception:
            start_param = 0.0

        entity.follow_path = None
        temp_offset = min(float(getattr(entity, "path_offset", 1.0)), 1.0)
        entity.temp_follow_path = FollowPath(
            character=entity,
            path=poly,
            path_offset=temp_offset,
            current_param=start_param,
            max_acceleration=getattr(entity, "max_acceleration", 300.0)
        )
        entity.algorithm = "TEMP_PATH_FOLLOWING"
        hinst.set_blackboard("is_returning_to_zone", True)
        hinst.set_blackboard("is_on_guardian_path", False)
        hinst.set_blackboard("is_at_protection_zone", False)
    except Exception as e:
        exception_print("RETURN TO PROTECTION ZONE", entity, str(e))
        hinst.set_blackboard("is_at_protection_zone", True)

@_register("check_return_path_finished")
def check_return_path_finished(hinst, entity):
    """
    Comprueba llegada y limpia flags. No escribe cooldowns.
    Llegada se determina por cercanía al return_target_pos o fin del temp path.
    """
    try:
        temp = getattr(entity, "temp_follow_path", None)
        target = hinst.get_blackboard("return_target_pos", None)
        arrival_thresh = float(get_spec_param(hinst, "arrival_threshold", 24.0))

        if temp and target:
            ex, ez = entity.get_pos()
            tx, tz = float(target[0]), float(target[1])
            if math.hypot(ex - tx, ez - tz) <= arrival_thresh:
                entity.temp_follow_path = None
                entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
                hinst.set_blackboard("is_at_protection_zone", True)
                hinst.set_blackboard("is_returning_to_zone", False)
                return

            path_obj = getattr(temp, "path", None)
            curp = float(getattr(temp, "current_param", 0.0))
            if path_obj and curp >= (int(getattr(path_obj, "segment_count", 1)) - 1):
                entity.temp_follow_path = None
                entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
                hinst.set_blackboard("is_at_protection_zone", True)
                hinst.set_blackboard("is_returning_to_zone", False)
                return
        else:
            hinst.set_blackboard("is_at_protection_zone", True)
    except Exception as e:
        exception_print("CHECK RETURN PATH FINISHED", entity, str(e))
        hinst.set_blackboard("is_at_protection_zone", True)

# --------------------
# Behavior flags / monitoring
# --------------------
@_register("set_behavior_flag_fleeing")
def set_behavior_flag_fleeing(hinst, entity):
    """
    Marcar huida (flags).
    """
    try:
        hinst.set_blackboard("is_fleeing", True)
    except Exception as e:
        exception_print("SET BEHAVIOR FLAG FLEEING", entity, str(e))

@_register("clear_behavior_flag_fleeing")
def clear_behavior_flag_fleeing(hinst, entity):
    """Quitar flag de huida."""
    try:
        hinst.set_blackboard("is_fleeing", False)
    except Exception as e:
        exception_print("CLEAR BEHAVIOR FLAG FLEEING", entity, str(e))

@_register("monitor_player_presence")
def monitor_player_presence(hinst, entity):
    """
    Acción de actualización periódica: comprobar visibilidad del jugador y almacenar tiempo desde último visto.
    """
    try:
        throttle_check_player_visibility(hinst, entity)
        last_seen = hinst.get_blackboard("last_player_visible_at", None)
        if last_seen:
            hinst.set_blackboard("time_since_player_seen", time.time() - float(last_seen))
    except Exception as e:
        exception_print("MONITOR PLAYER PRESENCE", entity, str(e))