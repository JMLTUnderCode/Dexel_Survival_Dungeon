"""
Condiciones para el HSM

Descripción
-------------------
    MÓDULO: Registro de condiciones booleanas usadas por la HSM para evaluar
    transiciones. Cada condición tiene la firma: fn(hinst, entity) -> bool.
    Las condiciones deben ser ligeras, rápidas y, en general, puramente lectoras del
    estado (blackboard y atributos de la entidad). Excepciones:
      - Actualizaciones pequeñas y explícitas del blackboard para bookkeeping temporal
        (timestamps, last_seen, last_known_pos) están permitidas y deben documentarse.

    Propósito:
        - Proveer predicados simples y compuestos que definen las reglas de transición
          entre estados de la HSM (visibilidad, salud, proximidad, finishing timers, etc.).
        - Mantener coherencia de lectura con las acciones: keys usadas deben estar
          documentadas en ambos lados.

Convenciones
-------------------
    - Documentación: todos los docstrings de condiciones deben estar en español y
      documentar: Descripción, Argumentos, Blackboard utilizado/modificado y
      Parámetros esperados. Si no hay entradas para Blackboard o Parámetros, indicar
      explícitamente "- Ninguno".
    - Firma: fn(hinst: HSMInstance, entity: Any) -> bool.
    - Registro: usar el decorador @condition para añadir la función al registro global.
    - Performance: deben ser muy rápidas; evitar cálculos trigonométricos innecesarios
      o búsquedas costosas cada vez (usar throttling o cached hints en el blackboard).
    - Robustez: no deben propagar excepciones; capturar errores y devolver False
      en casos indeterminados para no romper el ciclo del HSM.
    - Lectura vs Escritura: preferir lectura del blackboard; los únicos writes permitidos
      son metadata de observación (p.ej. last_player_visible_at, last_known_player_pos,
      last_health_snapshot_prev) y siempre documentados.
    - Uso de utilitarios: usar get_spec_param y get_player desde ai.utils para acceder
      a parámetros del spec y al jugador respectivamente.
    - Determinismo: evitar efectos secundarios que cambien el mundo; las condiciones
      deben ser puramente predictivas o idempotentes en su escritura.
    - Composición: crear funciones simples y combinarlas para condiciones compuestas
      (ej. PlayerNotVisibleAndAtProtectionZone) en lugar de duplicar lógica.
    - Nombres: preferir PascalCase o nombres descriptivos (ej. PlayerVisible,
      HealthBelow, RecentlyDamaged) para facilitar mapeo desde el HSM.
    - Testing: las condiciones deben ser fácilmente testeables inyectando un HSMInstance
      con blackboard controlado y un stub de entidad.
"""
import math
import time
from typing import Any, Dict
from ai.hsm import HSMInstance
from ai.utils import get_spec_param, get_player

# Registro global de condiciones
CONDITIONS: Dict[str, callable] = {}

def condition(fn):
    """
    Decorador
        REGISTRA: Añade la función al registro global CONDITIONS bajo su nombre.
        - Uso: aplicar @condition antes de la definición de la función.
        - Resultado: la función queda disponible para el builder/hsm.
    """
    CONDITIONS[fn.__name__] = fn
    return fn

# --------------------
# Salud (health) checks
# --------------------
@condition
def HealthBelow(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si la vida actual del entity es menor que el umbral de huida.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM que contiene el blackboard y spec.
        - entity (Any): entidad cuyo estado de vida se evalúa.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - flee_threshold (float): fracción (0..1) que define el umbral para huir.
    """
    try:
        # 1) Obtener umbral
        flee_threshold = get_spec_param(hinst, "flee_threshold", 0.30)

        # 2) Leer vida actual y máxima
        hp = float(getattr(entity, "health", 0.0))
        max_hp = float(getattr(entity, "max_health", hp))

        # 3) Validaciones y comparación
        if max_hp <= 0:
            return False
        return (hp / max_hp) < float(flee_threshold)
    except Exception:
        # Defensive: cualquier error -> condición falsa
        return False

@condition
def HealthAbove(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si la vida actual del entity es mayor o igual al umbral de restauración.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad cuya vida se evalúa.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - restore_threshold (float): fracción (0..1) que define el umbral para considerar restaurado.
    """
    try:
        restore_threshold = get_spec_param(hinst, "restore_threshold", 0.70)
        hp = float(getattr(entity, "health", 0.0))
        max_hp = float(getattr(entity, "max_health", hp))
        if max_hp <= 0:
            return False
        return (hp / max_hp) >= float(restore_threshold)
    except Exception:
        return False

# --------------------
# Visibilidad del jugador
# --------------------
@condition
def PlayerVisible(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el jugador está dentro de rango y dentro del cono de visión.
        - Actualiza timestamps y última posición conocida cuando se detecta visibilidad.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que realiza la comprobación de visión.

    Blackboard utilizado/modificado
        - last_player_visible_at (update): timestamp de la última vez que se vio al jugador.
        - last_known_player_pos (update): posición (x,z) del último avistamiento.
        - player_visible (update): flag booleano de visibilidad.

    Parámetros esperados
        - vision_range (float): distancia máxima de detección en píxeles.
        - vision_fov_deg (float): apertura del cono de visión en grados.
        - player_seen_memory (float): tiempo en segundos para considerar visible por memoria.
    """
    try:
        # 1) Parámetros
        params = hinst.blackboard.get("_spec_params", {})
        max_dist = float(params.get("vision_range", 300.0))
        fov_deg = float(params.get("vision_fov_deg", 120.0))
        memory = float(params.get("player_seen_memory", 0.5))

        # 2) Obtener jugador
        player = get_player(hinst)
        if not player:
            return False

        # 3) Posiciones y distancia
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dx, dz = px - ex, pz - ez
        dist = math.hypot(dx, dz)

        # 4) Range check + FOV check
        if dist <= max_dist:
            try:
                angle_to_player = math.atan2(dz, dx)
                facing = float(getattr(entity, "orientation", 0.0))
                half_fov = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
                # normalizar diferencia angular a [-pi, pi]
                diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
                if abs(diff) <= half_fov:
                    # 5) Visible: actualizar memoria en blackboard
                    hinst.set_blackboard("last_player_visible_at", time.time())
                    hinst.set_blackboard("last_known_player_pos", (float(px), float(pz)))
                    hinst.set_blackboard("player_visible", True)
                    return True
            except Exception:
                # Fallo en cálculo angular -> ignorar y permitir fallback de memoria
                pass

        # 6) Fallback por memoria: si fue visto recientemente, considerarlo visible
        last_seen = hinst.blackboard.get("last_player_visible_at", 0)
        if last_seen and (time.time() - float(last_seen)) <= memory:
            return True

        # 7) No visible: actualizar flag y devolver False
        hinst.set_blackboard("player_visible", False)
        return False
    except Exception:
        return False

@condition
def PlayerNotVisibleFor(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el jugador NO ha sido visible por más de `player_lost_timeout` segundos.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que consulta el tiempo desde el último avistamiento.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - player_lost_timeout (float): tiempo en segundos tras el cual se considera perdido.
    """
    try:
        timeout = get_spec_param(hinst, "player_lost_timeout", 2.0)
        last_seen = hinst.blackboard.get("last_player_visible_at", 0)
        if not last_seen:
            return True
        return (time.time() - float(last_seen)) >= float(timeout)
    except Exception:
        return False

# --------------------
# Safe anchor / curado
# --------------------
@condition
def PlayerFar(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el jugador está suficientemente lejos (>= safe_distance),
        y no es visible dentro del cono. Además escribe `safe_anchor` en el blackboard.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa si puede curarse en seguridad.

    Blackboard utilizado/modificado
        - safe_anchor (update): punto seguro calculado en la dirección opuesta al jugador.

    Parámetros esperados
        - safe_distance (float): distancia mínima requerida para considerar seguro.
        - vision_range (float): usado para comprobar visibilidad estricta.
        - vision_fov_deg (float): usado para comprobación de FOV estricta.
    """
    try:
        safe_distance = float(get_spec_param(hinst, "safe_distance", 450.0))
        player = get_player(hinst)
        if not player:
            return True

        # posiciones y distancia
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dx, dz = ex - px, ez - pz
        dist = math.hypot(dx, dz)

        # 1) distancia mínima requerida
        if dist < safe_distance:
            return False

        # 2) comprobar visibilidad estricta (si está dentro de vision y FOV -> no es seguro)
        vision = float(get_spec_param(hinst, "vision_range", 300.0))
        fov_deg = float(get_spec_param(hinst, "vision_fov_deg", 120.0))
        try:
            angle_to_player = math.atan2(pz - ez, px - ex)
            facing = float(getattr(entity, "orientation", 0.0))
            half_fov = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
            diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
            if dist <= vision and abs(diff) <= half_fov:
                return False
        except Exception:
            if dist <= vision:
                return False

        # 3) calcular safe_anchor (punto en la dirección opuesta al player a distancia safe_distance)
        d = max(1e-5, dist)
        sx = ex + (dx / d) * safe_distance
        sz = ez + (dz / d) * safe_distance
        hinst.set_blackboard("safe_anchor", (float(sx), float(sz)))
        return True
    except Exception:
        return False

# --------------------
# Protección / path checks (protection margin sobre path)
# --------------------
@condition
def IsFarFromProtectionZone(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si la distancia desde la entidad al punto MÁS CERCANO del
        path protegido (guardian_original_path o entity.path) es mayor que `protection_margin`.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa su proximidad al path protegido.

    Blackboard utilizado/modificado
        - guardian_last_param (update): cache del parámetro de path para optimizar búsquedas.
        - Ninguno (lectura): guardian_original_path (si existe) es leído desde el blackboard.

    Parámetros esperados
        - protection_margin (float): margen en píxeles que define la zona de protección.
    """
    try:
        # 1) margin (px) que define estar "sobre" el path
        margin = float(get_spec_param(hinst, "protection_margin", 40.0))

        # 2) obtener referencia al path protegido
        original = hinst.blackboard.get("guardian_original_path", None) or getattr(entity, "path", None)
        if original is None:
            # si no hay path definido, no consideramos 'far'
            return False

        # 3) usar hint/historial para acelerar get_param (locality optimization)
        hint = float(hinst.blackboard.get("guardian_last_param", 0.0))
        param = original.get_param(entity.get_pos(), hint)

        # 4) cache del param para la siguiente evaluación (ventana local)
        hinst.set_blackboard("guardian_last_param", float(param))

        # 5) obtener la posición (x, z) correspondiente al param y calcular distancia
        px, pz = original.get_position(param)
        ex, ez = entity.get_pos()
        dist = math.hypot(ex - px, ez - pz)

        # 6) comparar con margin
        return dist > margin
    except Exception:
        return False

@condition
def IsAtProtectionZone(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si la entidad está dentro de la protección del path.
        - Implementación: negación de IsFarFromProtectionZone para mantener semántica clara.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa si está en la zona protegida.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - Ninguno
    """
    try:
        return not IsFarFromProtectionZone(hinst, entity)
    except Exception:
        return False

# --------------------
# Condiciones compuestas para transiciones explícitas
# --------------------
@condition
def PlayerNotVisibleAndFarFromProtectionZone(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        COMBINADA: True si el jugador NO es visible (PlayerNotVisibleFor) y la entidad
        está FUERA del path protegido (IsFarFromProtectionZone).
        Uso típico: Atacar -> RegresarAZona.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa la condición compuesta.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - Ninguno
    """
    try:
        if not PlayerNotVisibleFor(hinst, entity):
            return False
        return IsFarFromProtectionZone(hinst, entity)
    except Exception:
        return False

@condition
def PlayerNotVisibleAndAtProtectionZone(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        COMBINADA: True si el jugador NO es visible y la entidad está EN la zona protegida.
        Uso típico: Atacar -> Vigilar.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa la condición compuesta.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - Ninguno
    """
    try:
        if not PlayerNotVisibleFor(hinst, entity):
            return False
        return IsAtProtectionZone(hinst, entity)
    except Exception:
        return False

@condition
def PlayerBeyondMelee(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el jugador está visible y su distancia es mayor que dist_for_mele.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa distancia relativa al jugador.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - dist_for_mele (float): umbral de distancia para preferir ataques melee.
    """
    try:
        player = get_player(hinst)
        if not player:
            return False
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)
        thresh = float(get_spec_param(hinst, "dist_for_mele", 120.0))
        # además requiere que PlayerVisible sea True para coherencia con la HSM
        if not CONDITIONS.get("PlayerVisible")(hinst, entity):
            return False
        return dist > thresh
    except Exception:
        return False

@condition
def PlayerWithinMelee(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el jugador está visible y su distancia es menor o igual que dist_for_mele.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que evalúa distancia relativa al jugador.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - dist_for_mele (float): umbral de distancia para considerar melee.
    """
    try:
        player = get_player(hinst)
        if not player:
            return False
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)
        thresh = float(get_spec_param(hinst, "dist_for_mele", 120.0))
        if not CONDITIONS.get("PlayerVisible")(hinst, entity):
            return False
        return dist <= thresh
    except Exception:
        return False

@condition
def LostHealthSinceLastRestoreAtLeast(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True cuando la fracción de vida perdida desde la última restauración
        es >= lost_health_trigger_pct. Si no existe health_at_last_restore se inicializa.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad cuyo historial de vida se compara.

    Blackboard utilizado/modificado
        - health_at_last_restore (read/update): referencia de vida usada como punto de comparación.

    Parámetros esperados
        - lost_health_trigger_pct (float): fracción (0..1) de vida perdida que dispara la condición.
    """
    try:
        pct = float(get_spec_param(hinst, "lost_health_trigger_pct", 0.25))
        hp = float(getattr(entity, "health", 0.0))
        max_hp = float(getattr(entity, "max_health", hp))
        if max_hp <= 0:
            return False
        health_at_restore = hinst.get_blackboard("health_at_last_restore", None)
        if health_at_restore is None:
            # inicializar para evitar disparos inmediatos
            hinst.set_blackboard("health_at_last_restore", float(hp))
            return False
        lost = max(0.0, float(health_at_restore) - hp)
        return (lost / max_hp) >= pct
    except Exception:
        return False

@condition
def IsAtBossPosition(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si la entidad está suficientemente cerca de boss_position.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que verifica su posición relativa a boss_position.

    Blackboard utilizado/modificado
        - Ninguno

    Parámetros esperados
        - boss_position (tuple): posición objetivo (x,z) del boss (si no existe se considera True).
        - arrival_threshold (float): umbral en píxeles para considerar llegada.
    """
    try:
        boss_pos = hinst.blackboard.get("_spec_params", {}).get("boss_position", None) \
                   or get_spec_param(hinst, "boss_position", None)
        if not boss_pos:
            return True
        ex, ez = entity.get_pos()
        tx, tz = float(boss_pos[0]), float(boss_pos[1])
        thresh = float(get_spec_param(hinst, "arrival_threshold", 24.0))
        return math.hypot(ex - tx, ez - tz) <= thresh
    except Exception:
        return False

@condition
def InvocationFinished(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el tiempo de invocación ha concluido (time_for_invocation).

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad asociada a la invocación.

    Blackboard utilizado/modificado
        - invocation_started_at (read): timestamp usado para calcular duración.

    Parámetros esperados
        - time_for_invocation (float): duración total de la fase de invocación en segundos.
    """
    try:
        start = hinst.get_blackboard("invocation_started_at", None)
        if not start:
            return False
        duration = float(get_spec_param(hinst, "time_for_invocation", 6.0))
        return (time.time() - float(start)) >= duration
    except Exception:
        return False

@condition
def RegenerationFinished(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si la regeneración ha finalizado (time_for_regeneration).

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad que está regenerando.

    Blackboard utilizado/modificado
        - regen_started_at (read): timestamp usado para calcular duración.

    Parámetros esperados
        - time_for_regeneration (float): duración total de la regeneración en segundos.
    """
    try:
        start = hinst.get_blackboard("regen_started_at", None)
        if not start:
            return False
        duration = float(get_spec_param(hinst, "time_for_regeneration", 8.0))
        return (time.time() - float(start)) >= duration
    except Exception:
        return False

@condition
def RecentlyDamaged(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: Detecta si la entidad sufrió daño recientemente comparando la vida
        actual con una snapshot previa y manteniendo una ventana temporal.

    Argumentos
        - hinst (HSMInstance): instancia de la HSM.
        - entity (Any): entidad cuyo daño reciente se detecta.

    Blackboard utilizado/modificado
        - last_health_snapshot_prev (read/update): snapshot de vida del tick previo.
        - recently_damaged_at (update): timestamp del último daño detectado.

    Parámetros esperados
        - recent_damage_threshold (float): umbral mínimo de HP perdido para considerar daño.
        - recent_damage_window (float): ventana temporal (s) durante la cual se mantiene el flag.
    """
    try:
        threshold = float(get_spec_param(hinst, "recent_damage_threshold", 1.0))
        window = float(get_spec_param(hinst, "recent_damage_window", 1.0))

        current_hp = float(getattr(entity, "health", 0.0) or 0.0)
        prev_hp = hinst.get_blackboard("last_health_snapshot_prev", None)
        now = time.time()

        # Si no existe prev_hp: inicializar y no disparar
        if prev_hp is None:
            hinst.set_blackboard("last_health_snapshot_prev", float(current_hp))
            return False

        # Detectar daño comparando con la snapshot previa
        if current_hp < float(prev_hp) - float(threshold):
            hinst.set_blackboard("recently_damaged_at", now)
            # actualizar prev snapshot para evitar múltiples disparos en el mismo tick
            hinst.set_blackboard("last_health_snapshot_prev", float(current_hp))
            return True

        # Si hubo daño recientemente dentro de la ventana temporal, seguir devolviendo True
        recent_at = float(hinst.get_blackboard("recently_damaged_at", 0.0) or 0.0)
        if recent_at and (now - recent_at) <= window:
            return True

        # No daño: actualizar prev para siguiente frame (defensivo)
        hinst.set_blackboard("last_health_snapshot_prev", float(current_hp))
        return False
    except Exception:
        return False