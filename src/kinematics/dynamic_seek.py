import math
from typing import Tuple

from kinematics.kinematic import Kinematic, SteeringOutput

class DynamicSeek:
    """
    Dynamic Seek behaviour (direct seeking).

    Objetivo
    - Calcular un SteeringOutput que haga que `character` se dirija de forma directa
      hacia `target` con una aceleración máxima.

    Parámetros (constructor)
    - character: Kinematic que se moverá.
    - target: Kinematic objetivo.
    - max_acceleration: aceleración máxima permitida (unidades/segundo²).
    """
    def __init__(
        self, 
        character : Kinematic, 
        target : Kinematic, 
        max_acceleration : float = 300.0
    ) -> None:
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)

    def get_steering(self) -> SteeringOutput:
        """
        Calcula el SteeringOutput para dirigirse directamente al target.

        Flujo:
        1) Calcular vector hacia target.
        2) Velocidad objetivo = max_acceleration en dirección al target.
        3) Retornar SteeringOutput(linear=target_velocity, angular=0).
        """
        # 1) Calcular vector y distancia al objetivo
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]
        
        # 2) Velocidad deseada en dirección al objetivo. (magnitude = max_acceleration)
        dist = math.hypot(dx, dz)
        target_velocity = (dx / dist * self.max_acceleration, dz / dist * self.max_acceleration)

        # 3) Devolver steering: la parte lineal es la velocidad objetivo; angular se maneja por orientación
        return SteeringOutput(target_velocity, 0.0)