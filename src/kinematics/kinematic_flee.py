import math
from typing import Tuple

from kinematics.kinematic import Kinematic, KinematicSteeringOutput

class KinematicFlee:
    """
    Kinematic Flee behaviour (direct fleeing).

    Objetivo
    - Calcular un SteeringOutput que haga que `character` se dirija de forma directa
      en dirección opuesta a `target` a la máxima velocidad especificada (`max_speed`).
    - No implementa desaceleración ni radios de llegada: es un movimiento directo y agresivo.

    Parámetros (constructor)
    - character: Kinematic que se moverá.
    - target: Kinematic objetivo.
    - max_speed: velocidad máxima a la que el character intentará moverse (unidades/segundo).
    """
    def __init__(
        self, 
        character : Kinematic, 
        target : Kinematic, 
        max_speed : float = 200.0
    ) -> None:
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)

    def get_steering(self) -> KinematicSteeringOutput:
        """
        Calcula el KinematicSteeringOutput para alejarse directamente del target.

        Flujo:
        1) Calcular vector en dirección opuesta al target y su magnitud (dist).
        2) Velocidad objetivo = max_speed en dirección opuesta al target.
        3) Actualizar orientación del character para que mire en la dirección del movimiento.
        4) Retornar KinematicSteeringOutput(velocity=target_velocity, rotation=0).
        """
        # 1) Calcular vector y distancia al objetivo
        dx = self.character.position[0] - self.target.position[0]
        dy = self.character.position[1] - self.target.position[1]
        dist = math.hypot(dx, dy)

        # 2) Velocidad objetivo en dirección al objetivo (magnitude = max_speed)
        target_velocity = (dx / dist * self.max_speed, dy / dist * self.max_speed)

        # 3) Actualizar orientación del character para que mire en la dirección del movimiento
        self.character.orientation = self.newOrientation(self.character.orientation, target_velocity)

        # 4) Devolver steering: la parte lineal es la velocidad objetivo; angular se maneja por orientación
        return KinematicSteeringOutput(target_velocity, 0.0)

    def newOrientation(self, current_orientation: float, velocity: Tuple[float, float]) -> float:
        """
        Calcula y devuelve la nueva orientación (ángulo en radianes) a partir de la dirección del vector velocity.

        - Si velocity == (0,0): devuelve current_orientation (sin cambios).
        - Se usa math.atan2(vy, vx) para obtener el ángulo en radianes en el rango [-pi, pi].
        """
        if velocity == (0, 0):
            return current_orientation
        return math.atan2(velocity[1], velocity[0])