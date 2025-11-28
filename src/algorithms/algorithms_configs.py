"""
Descripción
    MÓDULO: Definiciones de configuraciones (configs) por algoritmo.
    Cada dataclass representa los parámetros que necesita un algoritmo concreto.
    Estas clases se usan desde EntitySpec / Enemy para instanciar sólo las configs
    relevantes por entidad, evitando campos innecesarios.
"""

# 1. Imports necesarios
from dataclasses import dataclass
from typing import Optional, Union
from data.paths import PathInstance

# 2. Configs kinematic (básicos)
@dataclass
class KinematicSeekConfig:
    """
    Descripción
        CLASE: Configuración para KinematicSeek.

    Atributos
        - max_speed (float): velocidad máxima objetivo del seek.
    """
    max_speed: float = 150.0

@dataclass
class KinematicFleeConfig:
    """
    Descripción
        CLASE: Configuración para KinematicFlee.

    Atributos
        - max_speed (float): velocidad máxima objetivo del flee.
    """
    max_speed: float = 150.0

@dataclass
class KinematicArriveConfig:
    """
    Descripción
        CLASE: Configuración para KinematicArrive.

    Atributos
        - max_speed (float): velocidad máxima.
        - target_radius_dist (float): distancia considerada llegada.
        - time_to_target (float): tiempo objetivo para alcanzar velocidad deseada.
    """
    max_speed: float = 200.0
    target_radius_dist: float = 30.0
    time_to_target: float = 0.1

@dataclass
class KinematicWanderConfig:
    """
    Descripción
        CLASE: Configuración para KinematicWander.

    Atributos
        - max_speed (float): velocidad de desplazamiento.
        - max_rotation (float): rotación máxima aplicada por tick.
    """
    max_speed: float = 100.0
    max_rotation: float = 1.0

# 3. Configs dynamic (aceleración)
@dataclass
class DynamicSeekConfig:
    """
    Descripción
        CLASE: Configuración para DynamicSeek.

    Atributos
        - max_speed (float): velocidad máxima deseada.
        - max_acceleration (float): aceleración máxima permitida.
    """
    max_speed: float = 150.0
    max_acceleration: float = 200.0

@dataclass
class DynamicFleeConfig:
    """
    Descripción
        CLASE: Configuración para DynamicFlee.

    Atributos
        - max_speed (float): velocidad máxima deseada.
        - max_acceleration (float): aceleración máxima permitida.
    """
    max_speed: float = 150.0
    max_acceleration: float = 200.0

@dataclass
class DynamicArriveConfig:
    """
    Descripción
        CLASE: Configuración para DynamicArrive.

    Atributos
        - max_speed (float): velocidad máxima.
        - target_radius_dist (float): umbral de llegada.
        - slow_radius_dist (float): radio de desaceleración.
        - time_to_target (float): tiempo objetivo para ajustar velocidad.
        - max_acceleration (float): aceleración máxima aplicada.
    """
    max_speed: float = 150.0
    target_radius_dist: float = 30.0
    slow_radius_dist: float = 150.0
    time_to_target: float = 0.1
    max_acceleration: float = 300.0

@dataclass
class DynamicWanderConfig:
    """
    Descripción
        CLASE: Configuración para DynamicWander.

    Atributos
        - max_speed (float): velocidad máxima.
        - target_radius_deg (float): radio objetivo angular (en grados).
        - slow_radius_deg (float): radio de desaceleración angular (en grados).
        - time_to_target (float): tiempo objetivo para igualar velocidad/rotación.
        - max_acceleration (float): aceleración máxima.
        - max_rotation (float): rotación máxima.
        - max_angular_accel (float): aceleración angular máxima.
        - wander_offset (float): offset del circle center para wander.
        - wander_radius (float): radio del circle de wander.
        - wander_rate (float): tasa de cambio de orientación.
        - wander_orientation (float): orientación inicial del wander.
    """
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

# 4. Configs de orientación / matching
@dataclass
class AlignConfig:
    """
    Descripción
        CLASE: Configuración para Align.

    Atributos
        - target_radius_deg (float): radio angular para considerar llegada.
        - slow_radius_deg (float): radio angular de desaceleración.
        - time_to_target (float): tiempo objetivo para alcanzar la rotación deseada.
        - max_rotation (float): rotación máxima permitida.
        - max_angular_accel (float): aceleración angular máxima.
    """
    target_radius_deg: float = 2.0
    slow_radius_deg: float = 10.0
    time_to_target: float = 0.1
    max_rotation: float = 3.0
    max_angular_accel: float = 8.0

@dataclass
class VelocityMatchConfig:
    """
    Descripción
        CLASE: Configuración para VelocityMatch.

    Atributos
        - time_to_target (float): tiempo para igualar velocidad.
        - max_acceleration (float): aceleración máxima permitida.
    """
    time_to_target: float = 0.1
    max_acceleration: float = 200.0

# 5. Configs avanzadas (pursue / evade / face / look)
@dataclass
class PursueConfig:
    """
    Descripción
        CLASE: Configuración para Pursue.

    Atributos
        - max_speed (float): velocidad máxima de persecución.
        - target_radius_dist (float): umbral de llegada en distancia.
        - slow_radius_dist (float): radio de desaceleración.
        - time_to_target (float): tiempo objetivo para igualar velocidad.
        - max_acceleration (float): aceleración máxima.
        - max_prediction (float): tiempo máximo de predicción.
    """
    max_speed: float = 200.0
    target_radius_dist: float = 40.0
    slow_radius_dist: float = 180.0
    time_to_target: float = 0.15
    max_acceleration: float = 300.0
    max_prediction: float = 0.5

@dataclass
class EvadeConfig:
    """
    Descripción
        CLASE: Configuración para Evade.

    Atributos
        - max_speed (float): velocidad máxima.
        - max_acceleration (float): aceleración máxima.
        - max_prediction (float): tiempo máximo de predicción.
    """
    max_speed: float = 150.0
    max_acceleration: float = 300.0
    max_prediction: float = 0.5

@dataclass
class FaceConfig:
    """
    Descripción
        CLASE: Configuración para Face.

    Atributos
        - target_radius_deg (float): radio angular para considerar alineado.
        - slow_radius_deg (float): radio angular de desaceleración.
        - time_to_target (float): tiempo objetivo para igualar rotación.
        - max_rotation (float): rotación máxima permitida.
        - max_angular_accel (float): aceleración angular máxima.
    """
    target_radius_deg: float = 2.0
    slow_radius_deg: float = 10.0
    time_to_target: float = 0.1
    max_rotation: float = 2.0
    max_angular_accel: float = 8.0

@dataclass
class LookWhereYouAreGoingConfig:
    """
    Descripción
        CLASE: Configuración para LookWhereYouAreGoing.

    Atributos
        - target_radius_deg (float): radio angular para considerar alineado.
        - slow_radius_deg (float): radio angular de desaceleración.
        - time_to_target (float): tiempo objetivo para igualar rotación.
        - max_rotation (float): rotación máxima permitida.
        - max_angular_accel (float): aceleración angular máxima.
    """
    target_radius_deg: float = 5.0
    slow_radius_deg: float = 20.0
    time_to_target: float = 0.1
    max_rotation: float = 3.0
    max_angular_accel: float = 8.0

# 6. Configs para path following
@dataclass
class PathFollowingConfig:
    """
    Descripción
        CLASE: Configuración para PathFollowing.

    Atributos
        - max_acceleration (float): aceleración máxima aplicada por el seek delegado.
        - path_instance (Optional[PathInstance]): referencia a la instancia de ruta a seguir.
    """
    max_acceleration: float = 200.0
    path_instance: Optional[PathInstance] = None

@dataclass
class TempPathFollowingConfig:
    """
    Descripción
        CLASE: Configuración temporal/auxiliar para PathFollowing (offset).
    
    Atributos
        - path_offset (float): distancia en parámetros a avanzar sobre la ruta.
    """
    path_offset: float = 1.0

# 7. Tipo unión para facilitar type hints
AlgorithmConfigType = Union[
    KinematicSeekConfig,
    KinematicFleeConfig,
    KinematicArriveConfig,
    KinematicWanderConfig,
    DynamicSeekConfig,
    DynamicFleeConfig,
    DynamicArriveConfig,
    DynamicWanderConfig,
    AlignConfig,
    VelocityMatchConfig,
    PursueConfig,
    EvadeConfig,
    FaceConfig,
    LookWhereYouAreGoingConfig,
    PathFollowingConfig,
    TempPathFollowingConfig,
]