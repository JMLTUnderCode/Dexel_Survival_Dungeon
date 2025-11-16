"""
Condiciones para el HSM

Descripción
    MÓDULO: Registro de condiciones usadas por la HSM. Cada condición tiene la
    firma: fn(hinst, entity) -> bool. Las condiciones deben ser ligeras y usar
    el blackboard para datos compartidos.

Convenciones
    - Las condiciones se registran mediante el decorador `@condition`.
    - El HSM expone `_spec_params` en el blackboard con los parámetros del spec.
    - Las condiciones pueden leer y escribir claves en el blackboard (p.ej.
      `last_player_visible_at`, `last_known_player_pos`, `player_visible`).
    - Las funciones deben ser defensivas: nunca lanzar excepción no manejada.
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
        CONDICIÓN: True si la vida actual del entity es menor que el umbral.

    Lógica (pasos)
    1. Resolver 'flee_threshold' desde spec con get_spec_param.
    2. Leer hp y max_hp de la entidad.
    3. Calcular fraction = hp / max_hp y comparar.
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
        CONDICIÓN: True si la vida actual del entity es mayor o igual al umbral.

    Lógica (pasos)
    1. Resolver 'restore_threshold' desde spec.
    2. Leer hp / max_hp y comparar fraction >= threshold.
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
        CONDICIÓN: True si el jugador está dentro de rango y en el cono de visión.

    Lógica (pasos)
    1. Leer parámetros de vision desde _spec_params (vision_range, vision_fov_deg, memory).
    2. Obtener referencia al player vía get_player().
    3. Calcular distancia y, si dentro de vision_range, chequear ángulo (FOV).
    4. Si visible: actualizar timestamps y last_known en blackboard.
    5. Si no visible pero estuvo recientemente visible (memory) -> considerar visible.
    6. En caso contrario marcar player_visible=False y devolver False.
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
        CONDICIÓN: True si el jugador NO ha sido visible por más de `timeout` segundos.

    Lógica (pasos)
    1. Resolver timeout desde spec (player_lost_timeout).
    2. Leer last_player_visible_at del blackboard.
    3. Si no hay registro -> True (no visto nunca).
    4. Si tiempo transcurrido >= timeout -> True.
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
def PlayerFarAndNoThreat(hinst: HSMInstance, entity: Any) -> bool:
    """
    Descripción
        CONDICIÓN: True si el jugador está suficientemente lejos (>= safe_distance),
        y no es visible dentro del cono. Además escribe `safe_anchor` en blackboard.

    Lógica (pasos)
    1. Resolver safe_distance desde spec.
    2. Si no hay player -> True (no hay amenaza).
    3. Calcular distancia entidad->player; si < safe_distance -> False.
    4. Hacer FOV/vision strict check: si player dentro de vision y FOV -> False.
    5. Calcular safe_anchor en dirección opuesta al player y guardarlo.
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
        path protegido (guardian_original_path o entity.path) es mayor que
        `protection_margin`.

    Lógica (pasos)
    1. Resolver protection margin desde spec (protection_margin).
    2. Obtener el path original (guardian_original_path o entity.path).
    3. Usar last_param cache ('guardian_last_param') para búsqueda local en path.get_param.
    4. Actualizar guardian_last_param en blackboard para futuras consultas.
    5. Calcular posición en el param y medir distancia euclidiana.
    6. Devolver True si dist > margin, False en caso contrario.
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
        Implementación: negación de IsFarFromProtectionZone para mantener semántica clara.
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
    """
    try:
        if not PlayerNotVisibleFor(hinst, entity):
            return False
        return IsAtProtectionZone(hinst, entity)
    except Exception:
        return False