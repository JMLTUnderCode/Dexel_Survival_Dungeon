from dataclasses import dataclass
from data.paths import PathInstance

@dataclass
class KinematicSeekConfig:
    max_speed: float = 150.0

@dataclass
class KinematicFleeConfig:
    max_speed: float = 150.0

@dataclass
class KinematicArriveConfig:
    max_speed: float = 200.0
    target_radius_dist: float = 30.0
    time_to_target: float = 0.1

@dataclass
class KinematicWanderConfig:
    max_speed: float = 100.0
    max_rotation: float = 1.0

@dataclass
class DynamicSeekConfig:
    max_speed: float = 150.0
    max_acceleration: float = 200.0

@dataclass
class DynamicFleeConfig:
    max_speed: float = 150.0
    max_acceleration: float = 200.0

@dataclass
class DynamicArriveConfig:
    max_speed: float = 150.0
    target_radius_dist: float = 30.0
    slow_radius_dist: float = 150.0
    time_to_target: float = 0.1
    max_acceleration: float = 300.0

@dataclass
class DynamicWanderConfig:
    max_speed: float = 150.0
    target_radius_deg: float = 5.0
    slow_radius_deg: float = 20.0
    time_to_target: float = 0.1
    max_acceleration: float = 50.0
    max_rotation: float = 3.0
    max_angular_accel: float = 8.0
    wander_offset: float = 50.0
    wander_radius: float = 30.0
    wander_rate: float = 0.4
    wander_orientation: float = 0.0

@dataclass
class AlignConfig:
    target_radius_deg: float = 2.0
    slow_radius_deg: float = 10.0
    time_to_target: float = 0.1
    max_rotation: float = 3.0
    max_angular_accel: float = 8.0

@dataclass
class VelocityMatchConfig:
    time_to_target: float = 0.1
    max_acceleration: float = 200.0

@dataclass
class PursueConfig:
    max_speed: float = 200.0
    target_radius_dist: float = 40.0
    slow_radius_dist: float = 180.0
    time_to_target: float = 0.15
    max_acceleration: float = 300.0
    max_prediction: float = 0.5

@dataclass
class EvadeConfig:
    max_speed: float = 150.0
    max_acceleration: float = 300.0
    max_prediction: float = 0.5

@dataclass
class FaceConfig:
    target_radius_deg: float = 2.0
    slow_radius_deg: float = 10.0
    time_to_target: float = 0.1
    max_rotation: float = 2.0
    max_angular_accel: float = 8.0

@dataclass
class LookWhereYouAreGoingConfig:
    target_radius_deg: float = 5.0
    slow_radius_deg: float = 20.0
    time_to_target: float = 0.1
    max_rotation: float = 3.0
    max_angular_accel: float = 8.0

@dataclass
class PathFollowingConfig:
    max_acceleration: float = 200.0
    path_instance: PathInstance = None

@dataclass
class TempPathFollowingConfig:
    path_offset: float = 1.0

AlgorithmConfigs = (
    KinematicSeekConfig
    | KinematicFleeConfig
    | KinematicArriveConfig
    | KinematicWanderConfig
    | DynamicSeekConfig
    | DynamicFleeConfig
    | DynamicArriveConfig
    | DynamicWanderConfig
    | AlignConfig
    | VelocityMatchConfig
    | PursueConfig
    | EvadeConfig
    | FaceConfig
    | LookWhereYouAreGoingConfig
    | PathFollowingConfig
    | TempPathFollowingConfig
)
