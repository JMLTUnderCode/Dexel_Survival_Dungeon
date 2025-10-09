import math
from typing import Tuple

from kinematic import Kinematic, SteeringOutput

class KinematicSeek:
    """
    Kinematic Seek behaviour (direct seeking).

    Objetivo
    - Calcular un SteeringOutput que haga que `character` se dirija de forma directa
      hacia `target` a la máxima velocidad especificada (`max_speed`).
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

    def get_steering(self) -> SteeringOutput:
        """
        Calcula el SteeringOutput para dirigirse directamente al target.

        Flujo:
        1) Calcular vector hacia target y su magnitud (dist).
        2) Si dist == 0 -> devolver 0 (ya está en el objetivo).
        3) Velocidad deseada = max_speed en dirección al target.
        4) Actualizar orientación del character para que mire en la dirección del movimiento.
        5) Retornar SteeringOutput(linear=desired_velocity, angular=0).
        """
        # 1) Calcular vector y distancia al objetivo
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]
        dist = math.hypot(dx, dy)

        # 2) Si ya está en el objetivo, no moverse
        if dist == 0:
            return SteeringOutput((0.0, 0.0), 0.0)

        # 3) Velocidad deseada en dirección al objetivo (magnitude = max_speed)
        desired_velocity = (dx / dist * self.max_speed, dy / dist * self.max_speed)

        # 4) Actualizar orientación del character para que mire en la dirección del movimiento
        self.character.orientation = self.newOrientation(self.character.orientation, desired_velocity)

        # 5) Devolver steering: la parte lineal es la velocidad objetivo; angular se maneja por orientación
        return SteeringOutput(desired_velocity, 0.0)

    def newOrientation(self, current_orientation: float, velocity: Tuple[float, float]) -> float:
        """
        Calcula y devuelve la nueva orientación (ángulo en radianes) a partir de la dirección del vector velocity.

        - Si velocity == (0,0): devuelve current_orientation (sin cambios).
        - Se usa math.atan2(vy, vx) para obtener el ángulo en radianes en el rango [-pi, pi].
        """
        if velocity == (0, 0):
            return current_orientation
        return math.atan2(velocity[1], velocity[0])