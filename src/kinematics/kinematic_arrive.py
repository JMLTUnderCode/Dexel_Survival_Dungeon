import math
from typing import Tuple

from kinematics.kinematic import Kinematic, KinematicSteeringOutput

class KinematicArrive:
    """
    Kinematic Arrive behaviour (smooth arrival).

    Objetivo
    - Generar un SteeringOutput (aceleración lineal, rotación angular) que permita
      a un `character` acercarse a un `target` de forma natural y suavizada:
        - detenerse si está dentro de `target_radius`
        - desacelerar progresivamente al entrar en `slow_radius`
        - mantener `max_speed` fuera de `slow_radius`

    Parámetros (constructor)
    - character: Kinematic que se mueve (debe exponer `position: (x,y)`, `velocity: (vx,vy)` y `orientation`)
    - target: Kinematic objetivo (debe exponer `position: (x,y)`)
    - max_speed: velocidad máxima deseada (unidades/segundo)
    - target_radius: distancia a la que se considera "llegado" (unidades)
    - time_to_target: tiempo deseado para alcanzar la velocidad objetivo (segundos). Controla la suavidad.
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 200.0,
        target_radius: float = 40.0,
        time_to_target: float = 0.15,
    ) -> None:
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)
        self.target_radius = float(target_radius)
        self.time_to_target = float(time_to_target)

    def get_steering(self) -> KinematicSteeringOutput:
        """
        Calcula y devuelve el KinematicSteeringOutput.

        Flujo:
        1) Calcular vector hacia target.
        2) Si dentro de target_radius -> devolver 0 (llegado).
        3) Aproximarse hacia el objetivo en time_to_target segundos
        4) Limitar velocidad a max_speed
        5) Devolver steering (solo componente velocidad). Rotación se gestiona por el sistema de orientación.
        """

        # 1) Vector hacia target
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]

        # 2) Si la distancia es extremadamente pequeña, consideramos que llegó.
        dist = math.hypot(dx, dz)
        if dist <= self.target_radius:
            return KinematicSteeringOutput((0.0, 0.0), 0.0)

        # 3) Aproximarse hacia el objetivo en time_to_target segundos
        #    (esto genera una velocidad objetivo proporcional a la distancia)
        target_velocity = (dx / self.time_to_target, dz / self.time_to_target)
        
        # 4) Limitar velocidad a max_speed
        dist = math.hypot(target_velocity[0], target_velocity[1])
        if dist > self.max_speed:
            target_velocity = (target_velocity[0] / dist * self.max_speed,
                               target_velocity[1] / dist * self.max_speed)

        # 5) Devolver steering (solo componente lineal). Angular se gestiona por el sistema de orientación.
        return KinematicSteeringOutput(target_velocity, 0.0)