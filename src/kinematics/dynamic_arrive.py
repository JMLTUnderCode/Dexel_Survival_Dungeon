import math
from typing import Tuple

from kinematics.kinematic import Kinematic, SteeringOutput

class DynamicArrive:
    """
    Dynamic Arrive behaviour (smooth arrival).

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
    - slow_radius: radio a partir del cual desacelera (unidades)
    - time_to_target: tiempo deseado para alcanzar la velocidad objetivo (segundos). Controla la suavidad.
    - max_acceleration: aceleración máxima permitida (unidades/segundo²)
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 200.0,
        target_radius: float = 40.0,
        slow_radius: float = 180.0,
        time_to_target: float = 0.15,
        max_acceleration: float = 300.0,
    ) -> None:
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)
        self.target_radius = float(target_radius)
        self.slow_radius = float(slow_radius)
        self.time_to_target = float(time_to_target)
        self.max_acceleration = float(max_acceleration)

    def get_steering(self) -> SteeringOutput:
        """
        Calcula y devuelve el SteeringOutput.

        Flujo:
        1) Calcular vector hacia target.
        2) Si dentro de target_radius -> devolver 0 (llegado).
        3) Escoger velocidad objetivo (magnitud):
           - fuera de slow_radius -> max_speed
           - dentro -> escala entre 0..max_speed usando la distancia al target
        4) Calcular vector de velocidad deseada (dirección normalizada * velocidad objetivo).
        5) Calcular aceleración deseada para alcanzar la velocidad objetivo en time_to_target segundos.
        6) Limitar la aceleración a max_acceleration.
        7) Devolver steering (solo componente lineal). Angular se gestiona por el sistema de orientación.
        """

        # 1) Vector hacia target
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]
        
        # 2) Si la distancia es extremadamente pequeña, consideramos que llegó.
        dist = math.hypot(dx, dz)
        if dist <= self.target_radius:
            return SteeringOutput((0.0, 0.0), 0.0)

        # 3) Velocidad objetivo (magnitud)
        target_speed = 0.0
        if dist > self.slow_radius:
            target_speed = self.max_speed
        else:
            target_speed = self.max_speed *  dist / self.slow_radius # Se puede ajustar la escala (lineal, cuadrática, etc.)

        # 4) Vector de velocidad deseada (normalizamos la dirección)
        target_velocity = (dx, dz)
        mag = math.hypot(target_velocity[0], target_velocity[1])
        if mag == 0.0:
            target_velocity = (0.0, 0.0)
        else:
            target_velocity = (target_velocity[0] / mag * target_speed, target_velocity[1] / mag * target_speed)

        # 5) Calcular la aceleración deseada para alcanzar target_velocity en time_to_target segundos.
        current_vx, current_vy = self.character.velocity
        steering_linear = (
            (target_velocity[0] - current_vx) / self.time_to_target,
            (target_velocity[1] - current_vy) / self.time_to_target,
        )

        # 6) Limitar la aceleración a max_acceleration
        mag = math.hypot(steering_linear[0], steering_linear[1])
        if mag > self.max_acceleration:
            steering_linear = (
                steering_linear[0] / mag * self.max_acceleration,
                steering_linear[1] / mag * self.max_acceleration,
            )

        # 7) Devolver steering (solo componente lineal). Angular se gestiona por el sistema de orientación.
        return SteeringOutput(steering_linear, 0.0)