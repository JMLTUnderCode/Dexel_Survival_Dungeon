"""
Condition registry. Each condition signature: fn(hsm_instance, entity) -> bool

Utilities to access spec params or blackboard values are provided here.
"""
import math
import time

CONDITIONS = {}

def condition(fn):
    CONDITIONS[fn.__name__] = fn
    return fn

def _get_spec_param(hinst, key: str, default=None):
    """
    Resolve parameter key: if key is string and exists in _spec_params use it,
    else try parse numeric literal.
    """
    spec = hinst.blackboard.get("_spec_params", {})
    if key is None:
        return default
    if isinstance(key, (int, float)):
        return key
    # allow keys that refer to spec params
    if isinstance(key, str):
        if key in spec:
            return spec[key]
        try:
            return float(key)
        except Exception:
            return default
    return default

@condition
def HealthBelow(hinst, entity):
    params = hinst.blackboard.get("_spec_params", {})
    threshold = params.get("flee_threshold", 0.3)
    # allow override per-transition via cond_params
    cond_p = hinst.blackboard.get("_last_transition_cond_params", {}) or {}
    if "threshold" in cond_p:
        threshold = _get_spec_param(hinst, cond_p["threshold"], threshold)
    hp = getattr(entity, "health", 0.0)
    max_hp = getattr(entity, "max_health", hp)
    if max_hp <= 0:
        return False
    return (hp / max_hp) < threshold

@condition
def HealthAbove(hinst, entity):
    params = hinst.blackboard.get("_spec_params", {})
    threshold = params.get("restore_threshold", 0.7)
    cond_p = hinst.blackboard.get("_last_transition_cond_params", {}) or {}
    if "threshold" in cond_p:
        threshold = _get_spec_param(hinst, cond_p["threshold"], threshold)
    hp = getattr(entity, "health", 0.0)
    max_hp = getattr(entity, "max_health", hp)
    if max_hp <= 0:
        return False
    return (hp / max_hp) >= threshold

@condition
def PlayerVisible(hinst, entity):
    """
    True if player is within distance AND inside entity's FOV (based on entity.orientation).
    Also honors short memory (player_seen_memory) so we do not oscillate on throttled checks.
    """
    params = hinst.blackboard.get("_spec_params", {})
    max_dist = float(params.get("vision_range", 300.0))
    fov_deg = float(params.get("vision_fov_deg", 120.0))
    memory = float(params.get("player_seen_memory", 0.5))

    manager = hinst.blackboard.get("manager")
    player = None
    if manager:
        player = getattr(manager, "player", None)
    if not player:
        return False

    ex, ez = entity.get_pos()
    px, pz = player.get_pos()
    dx, dz = px - ex, pz - ez
    dist = math.hypot(dx, dz)
    if dist <= max_dist:
        # angle check
        try:
            angle_to_player = math.atan2(dz, dx)
            facing = float(getattr(entity, "orientation", 0.0))
            half_fov = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
            diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) <= half_fov:
                hinst.set_blackboard("last_player_visible_at", time.time())
                hinst.set_blackboard("last_known_player_pos", (px, pz))
                hinst.set_blackboard("player_visible", True)
                return True
        except Exception:
            pass

    # short memory fallback
    last_seen = hinst.blackboard.get("last_player_visible_at", 0)
    if last_seen and (time.time() - last_seen) <= memory:
        return True

    hinst.set_blackboard("player_visible", False)
    return False

@condition
def PlayerNotVisibleFor(hinst, entity):
    """
    True if player has NOT been visible for more than timeout (seconds).
    Expects timeout_key in cond_params or uses spec 'player_lost_timeout'.
    """
    cond_p = hinst.blackboard.get("_last_transition_cond_params", {}) or {}
    spec = hinst.blackboard.get("_spec_params", {})
    timeout = spec.get("player_lost_timeout", 2.0)
    if "timeout_key" in cond_p:
        timeout = _get_spec_param(hinst, cond_p["timeout_key"], timeout)
    last_seen = hinst.blackboard.get("last_player_visible_at", 0)
    if not last_seen:
        # never seen -> consider not visible for long time
        return True
    return (time.time() - last_seen) >= float(timeout)

@condition
def PlayerFarAndNoThreat(hinst, entity):
    """
    True if the player is far enough (dist >= safe_distance), not strictly visible
    (distance + FOV), and there are no other enemies close to this entity.
    Also sets a safe_anchor on the HSM blackboard (point away from player at safe_distance).
    cond_params:
      - safe_distance_key: key or numeric to resolve safe_distance
      - no_enemies_radius: radius to check for nearby enemies (default 300.0)
    """
    params = hinst.blackboard.get("_spec_params", {})
    cond_p = hinst.blackboard.get("_last_transition_cond_params", {}) or {}

    # Resolve safe_distance (cond param overrides spec)
    safe_distance = _get_spec_param(hinst, cond_p.get("safe_distance_key", None),
                                   params.get("safe_distance", 400.0))
    try:
        safe_distance = float(safe_distance)
    except Exception:
        safe_distance = float(params.get("safe_distance", 400.0))

    no_enemies_radius = float(cond_p.get("no_enemies_radius", 300.0))

    manager = hinst.blackboard.get("manager")
    player = getattr(manager, "player", None) if manager else None
    if not player:
        return True

    ex, ez = entity.get_pos()
    px, pz = player.get_pos()
    dx, dz = ex - px, ez - pz
    dist = math.hypot(dx, dz)

    # 1) Distance check: require player to be beyond safe_distance
    if dist < safe_distance:
        return False

    # 2) Strict visibility check (distance + FOV). If player is visible -> threat
    vision = float(params.get("vision_range", 300.0))
    fov_deg = float(params.get("vision_fov_deg", 120.0))
    try:
        # angle to player
        angle_to_player = math.atan2(pz - ez, px - ex)
        facing = float(getattr(entity, "orientation", 0.0))
        half_fov = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
        diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
        if dist <= vision and abs(diff) <= half_fov:
            # player is within strict vision cone => threat
            return False
    except Exception:
        # if computing FOV fails, be conservative and treat as threat if within vision
        if dist <= vision:
            return False

    # 3) No other enemies close (threat via nearby allies)
    if manager:
        for e in getattr(manager, "enemies", []):
            if e is entity:
                continue
            edx = e.position[0] - ex
            edz = e.position[1] - ez
            if math.hypot(edx, edz) < no_enemies_radius:
                return False

    # 4) Compute and store a safe_anchor (point away from player at safe_distance)
    d = max(1e-5, dist)
    sx = ex + (dx / d) * safe_distance
    sz = ez + (dz / d) * safe_distance
    hinst.set_blackboard("safe_anchor", (sx, sz))

    return True