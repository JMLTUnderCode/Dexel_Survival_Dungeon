import random
import math
import time
from typing import Any, Dict

from kinematics.kinematic import SteeringOutput
from kinematics.path_following import FollowPath
from helper.paths import PolylinePath
from configs.package import CONF

# ACTIONS: mapping string -> callable(hinst, entity)
# Each action receives (hinst, entity) where hinst is HSMInstance (see src/ai/hsm.py)
# and entity is the Enemy instance.
ACTIONS: Dict[str, callable] = {}

# --- Helpers ------------------------------------------------------------
def _get_manager(hinst) -> Any:
    return hinst.blackboard.get("manager") or hinst.blackboard.get("entity_manager")

def _spec_param(hinst, key, default=None):
    spec = hinst.blackboard.get("_spec_params", {}) or {}
    if key is None:
        return default
    if isinstance(key, (int, float)):
        return key
    if isinstance(key, str) and key in spec:
        return spec[key]
    try:
        return float(key)
    except Exception:
        return default

def _register(name):
    def _decor(fn):
        ACTIONS[name] = fn
        return fn
    return _decor

# --- No-op / bookkeeping -----------------------------------------------
@_register("hsm_noop")
def hsm_noop(hinst, entity):
    return

@_register("record_last_state_start")
def record_last_state_start(hinst, entity):
    try:
        hinst.set_blackboard("last_state_stack", list(hinst.get_active_stack()))
    except Exception:
        pass

# --- Patrol (FollowPath) -----------------------------------------------
@_register("start_random_patrol")
def start_random_patrol(hinst, entity):
    try:
        manager = _get_manager(hinst)
        pathfinder = getattr(manager, "pathfinder", None)
        if pathfinder is None or getattr(pathfinder, "navmesh", None) is None:
            # fallback to wander if no navmesh available
            entity.follow_path = None
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return

        # Force clear old follow_path so entry always resets routing
        try:
            entity.follow_path = None
        except Exception:
            pass

        params = hinst.blackboard.get("_spec_params", {})
        desired_nodes = int(params.get("patrol_path_nodes", 20))
        attempts = 0
        best_pts = None
        nodes_list = list(getattr(pathfinder.navmesh, "nodes", {}).values())
        if not nodes_list:
            # no navmesh nodes -> fallback
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return
        # Try random target nodes until we find a path with enough nodes
        while attempts < 12:
            target_node = random.choice(nodes_list)
            pts = pathfinder.find_path(entity.get_pos(), target_node.center)
            if pts and len(pts) >= desired_nodes:
                best_pts = pts
                break
            if pts and (best_pts is None or len(pts) > len(best_pts)):
                best_pts = pts
            attempts += 1

        if not best_pts:
            # fallback a wander si no se obtuvo ruta útil
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
            return
        pts = best_pts
        poly = PolylinePath(pts, closed=False)
        try:
            entity.follow_path = FollowPath(
                character=entity,
                path=poly,
                path_offset=hinst.blackboard.get("path_offset", getattr(entity, "path_offset", 1.0)),
                current_param=0.0,
                max_acceleration=getattr(entity, "max_acceleration", 300.0)
            )
            entity.algorithm = CONF.ALG.ALGORITHM.PATH_FOLLOWING
            hinst.set_blackboard("patrol_target", pts[-1])
            hinst.set_blackboard("patrol_requested_at", time.time())
        except Exception:
            entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
            hinst.set_blackboard("patrol_requested_at", time.time())
    except Exception:
        return

@_register("patrol_tick")
def patrol_tick(hinst, entity):
    try:
        poly_follow = getattr(entity, "follow_path", None)
        throttle = hinst.get_blackboard("_spec_params", {}).get("patrol_tick_throttle", 3.0)
        last = hinst.get_blackboard("patrol_requested_at", 0)
        now = time.time()
        need_new = False
        if poly_follow is None:
            if now - last > throttle:
                need_new = True
        else:
            # if path finished or current_param near end -> request new
            path_obj = getattr(poly_follow, "path", None)
            curp = getattr(poly_follow, "current_param", 0.0)
            seg_count = getattr(path_obj, "segment_count", None) or getattr(path_obj, "segment_count", None) or 0
            if seg_count and curp >= max(0, seg_count - 1):
                need_new = True
            # if follow_path was forcibly cleared, request new after throttle
            if getattr(entity, "algorithm", None) != CONF.ALG.ALGORITHM.PATH_FOLLOWING:
                if now - last > throttle:
                    need_new = True
        if need_new:
            start_random_patrol(hinst, entity)
    except Exception:
        pass

@_register("stop_patrol")
def stop_patrol(hinst, entity):
    try:
        entity.follow_path = None
        # fallback to wander to keep entity moving
        entity.algorithm = CONF.ALG.ALGORITHM.WANDER_KINEMATIC
    except Exception:
        pass

# --- Visibility / bookkeeping -----------------------------------------
@_register("throttle_check_player_visibility")
def throttle_check_player_visibility(hinst, entity):
    try:
        manager = _get_manager(hinst)
        player = getattr(manager, "player", None) if manager else None
        if not player:
            return
        params = hinst.blackboard.get("_spec_params", {})
        throttle = params.get("check_los_throttle", 0.25)
        last = hinst.get_blackboard("last_los_check", 0)
        now = time.time()
        if now - last < throttle:
            return
        hinst.set_blackboard("last_los_check", now)

        # compute vector & distance
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dx, dz = px - ex, pz - ez
        dist = math.hypot(dx, dz)
        vision = float(params.get("vision_range", 300.0))

        # distance fail -> not visible
        if dist > vision:
            hinst.set_blackboard("player_visible", False)
            return

        # FOV check: use entity.orientation as forward direction
        fov_deg = float(params.get("vision_fov_deg", 120.0))
        half_fov_rad = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)
        # orientation: entity.orientation (radians); angle to player:
        try:
            angle_to_player = math.atan2(dz, dx)
            facing = float(getattr(entity, "orientation", 0.0))
            # normalize difference to [-pi, pi]
            diff = (angle_to_player - facing + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) <= half_fov_rad:
                # visible: update blackboard and last seen
                hinst.set_blackboard("last_known_player_pos", (px, pz))
                hinst.set_blackboard("player_visible", True)
                hinst.set_blackboard("last_player_visible_at", now)
                return
        except Exception:
            # fallback to distance-only if something goes wrong
            pass

        # not visible by FOV
        hinst.set_blackboard("player_visible", False)
    except Exception:
        pass

# --- Pursue ------------------------------------------------------------
@_register("start_pursue_target")
def start_pursue_target(hinst, entity):
    try:
        manager = _get_manager(hinst)
        player = getattr(manager, "player", None) if manager else None
        if not player:
            return
        # set pursue algorithm - entity.pursue uses target reference set at creation (usually player)
        entity.algorithm = CONF.ALG.ALGORITHM.PURSUE
        # ensure pursue target reference updated
        try:
            entity.pursue.target = player
        except Exception:
            pass
        hinst.set_blackboard("pursuing", True)
        hinst.set_blackboard("last_known_player_pos", player.get_pos())
        hinst.set_blackboard("player_visible_since", time.time())
    except Exception:
        pass

@_register("pursue_tick")
def pursue_tick(hinst, entity):
    try:
        # maintain last_known_player_pos when visible
        throttle_check_player_visibility(hinst, entity)
    except Exception:
        pass

@_register("stop_pursue")
def stop_pursue(hinst, entity):
    try:
        hinst.set_blackboard("pursuing", False)
        # fallback to patrolling
        stop_patrol(hinst, entity)
    except Exception:
        pass

@_register("try_melee_attack")
def try_melee_attack(hinst, entity):
    """
    The actual damage application is handled by Enemy.update melee code.
    This action will ensure the animation and quick check for same-frame attacks.
    """
    try:
        manager = _get_manager(hinst)
        player = getattr(manager, "player", None) if manager else None
        if not player:
            return
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)
        attack_r = getattr(entity, "attack_range", hinst.get_blackboard("_spec_params", {}).get("attack_range", 48.0))
        if dist <= attack_r:
            # set attack animation; actual damage executed in Enemy.update
            try:
                from characters.animation import set_animation_state
                set_animation_state(entity, CONF.ENEMY.ACTIONS.ATTACK)
            except Exception:
                pass
    except Exception:
        pass

# --- Evade -------------------------------------------------------------
@_register("start_evade_from_player")
def start_evade_from_player(hinst, entity):
    try:
        manager = _get_manager(hinst)
        player = getattr(manager, "player", None) if manager else None
        if not player:
            return
        # store previous algorithm BEFORE changing it
        prev_alg = getattr(entity, "algorithm", None)
        hinst.set_blackboard("prev_algorithm", prev_alg)
        # Ensure LookWhereYoureGoing target points to player (for angular component)
        try:
            entity.look_where.target = manager.player
        except Exception:
            pass
        
        entity.algorithm = CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING

        hinst.set_blackboard("is_fleeing", True)
    except Exception:
        pass

@_register("evade_tick")
def evade_tick(hinst, entity):
    try:
        # monitor distance to player — no heavy ops here
        manager = _get_manager(hinst)
        if not manager:
            return
        player = getattr(manager, "player", None)
        if not player:
            return
        ex, ez = entity.get_pos()
        px, pz = player.get_pos()
        dist = math.hypot(px - ex, pz - ez)
        hinst.set_blackboard("distance_to_player", dist)
    except Exception:
        pass

@_register("stop_evade")
def stop_evade(hinst, entity):
    try:
        hinst.set_blackboard("is_fleeing", False)
        prev = hinst.get_blackboard("prev_algorithm", None)
        # restore previous algorithm if available, otherwise fallback to patrol/wander
        if prev:
            entity.algorithm = prev
        else:
            stop_patrol(hinst, entity)
    except Exception:
        pass

# --- Face / Safe anchor / movement ------------------------------------
@_register("face_towards_safe_anchor")
def face_towards_safe_anchor(hinst, entity):
    try:
        manager = _get_manager(hinst)
        player = getattr(manager, "player", None) if manager else None

        params = hinst.blackboard.get("_spec_params", {})
        vision = float(params.get("vision_range", 300.0))
        fov_deg = float(params.get("vision_fov_deg", 120.0))
        face_mult = float(params.get("face_range_multiplier", 1.5))
        face_range = vision * face_mult
        half_fov_rad = math.radians(max(0.0, min(180.0, fov_deg)) / 2.0)

        # safe_anchor / last_known
        last_known = hinst.get_blackboard("last_known_player_pos", None)
        safe = hinst.get_blackboard("safe_anchor", None)

        # compute safe_anchor if missing (fallback away from player)
        if not safe:
            ex, ez = entity.get_pos()
            if player:
                px, pz = player.get_pos()
                dx = ex - px
                dz = ez - pz
                dist = math.hypot(dx, dz) or 1.0
                sd = _spec_param(hinst, "safe_distance", 200.0)
                sx = ex + dx / dist * sd
                sz = ez + dz / dist * sd
            else:
                ang = random.random() * (2 * math.pi)
                r = 80.0
                sx = ex + math.cos(ang) * r
                sz = ez + math.sin(ang) * r
            safe = (sx, sz)
            hinst.set_blackboard("safe_anchor", safe)

        # If player exists and is within extended face range AND inside FOV relative to enemy orientation,
        # make Face target the live player (dynamic). Use this extended range only for Face (not for Huyó/Atacar).
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
                    # dynamic face to player (will update as player moves)
                    entity.face.target = player
                    entity.algorithm = CONF.ALG.ALGORITHM.FACE
                    hinst.set_blackboard("curing_face_target", player.get_pos())
                    return
            except Exception:
                # fallback to static target below
                pass

        # otherwise face last known pos (static kinematic) so enemy watches that point while healing
        target_pos = last_known if last_known is not None else safe
        try:
            from kinematics.kinematic import Kinematic as KinematicClass
            tgt = KinematicClass(position=target_pos, orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
            entity.face.target = tgt
            entity.algorithm = CONF.ALG.ALGORITHM.FACE
            hinst.set_blackboard("curing_face_target", target_pos)
        except Exception:
            pass
    except Exception:
        pass

@_register("clear_safe_anchor")
def clear_safe_anchor(hinst, entity):
    try:
        if "safe_anchor" in hinst.blackboard:
            del hinst.blackboard["safe_anchor"]
        if "curing_face_target" in hinst.blackboard:
            del hinst.blackboard["curing_face_target"]
        # restore face target to default (use player as target if available)
        manager = _get_manager(hinst)
        player = getattr(manager, "player", None) if manager else None
        try:
            if player:
                entity.face.target = player
        except Exception:
            pass
    except Exception:
        pass

@_register("stop_movement")
def stop_movement(hinst, entity):
    try:
        entity.velocity = (0.0, 0.0)
        entity._pending_steering = SteeringOutput(linear=(0.0, 0.0), angular=0.0)
    except Exception:
        pass

# --- Healing -----------------------------------------------------------
@_register("start_heal_tick")
def start_heal_tick(hinst, entity):
    hinst.set_blackboard("healing", True)
    hinst.set_blackboard("heal_accum", 0.0)
    hinst.set_blackboard("last_heal_at", time.time())

@_register("heal_tick")
def heal_tick(hinst, entity):
    try:
        if not hinst.get_blackboard("healing", False):
            return
        dt = float(hinst.get_blackboard("_dt", 0.0) or 0.0)
        params = hinst.blackboard.get("_spec_params", {})
        rate = params.get("heal_rate_per_sec", 0.10)  # fraction of max_health per second
        max_hp = getattr(entity, "max_health", 100.0)
        if max_hp <= 0:
            return
        inc = rate * max_hp * dt
        entity.health = min(max_hp, getattr(entity, "health", 0.0) + inc)
    except Exception:
        pass

@_register("stop_heal_tick")
def stop_heal_tick(hinst, entity):
    hinst.set_blackboard("healing", False)
    hinst.set_blackboard("heal_accum", 0.0)

# --- Behavior flags / monitoring -------------------------------------
@_register("set_behavior_flag_fleeing")
def set_behavior_flag_fleeing(hinst, entity):
    hinst.set_blackboard("is_fleeing", True)

@_register("clear_behavior_flag_fleeing")
def clear_behavior_flag_fleeing(hinst, entity):
    hinst.set_blackboard("is_fleeing", False)

@_register("monitor_player_presence")
def monitor_player_presence(hinst, entity):
    try:
        throttle_check_player_visibility(hinst, entity)
        # optionally compute time since last seen
        last_seen = hinst.get_blackboard("last_player_visible_at", None)
        if last_seen:
            hinst.set_blackboard("time_since_player_seen", time.time() - last_seen)
    except Exception:
        pass