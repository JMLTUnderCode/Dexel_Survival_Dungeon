import math
from typing import Tuple

from kinematic import Kinematic, SteeringOutput

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
    - slow_radius: radio a partir del cual desacelera (unidades)
    - time_to_target: tiempo deseado para alcanzar la velocidad objetivo (segundos). Controla la suavidad.
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 200.0,
        target_radius: float = 40.0,
        slow_radius: float = 180.0,
        time_to_target: float = 0.15,
    ) -> None:
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)
        self.target_radius = float(target_radius)
        self.slow_radius = float(slow_radius)
        self.time_to_target = float(time_to_target)

    def get_steering(self) -> SteeringOutput:
        """
        Calcula y devuelve el SteeringOutput.

        Flujo:
        1) Calcular vector hacia target y su magnitud (dist).
        2) Si dentro de target_radius -> devolver 0 (llegado).
        3) Escoger velocidad objetivo (v_desired):
           - fuera de slow_radius -> max_speed
           - dentro -> escala entre 0..max_speed
        4) Construir v_desired vectorial normalizando la dirección al target.
        5) Devolver SteeringOutput(linear=desired_accel, angular=0).
        """

        # 1) Vector hacia target
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]
        dist = math.hypot(dx, dz)

        # 1.a) Si la distancia es extremadamente pequeña, consideramos que llegó.
        if dist <= self.target_radius:
            # Asegurar que el character pare: reset de velocidad no se hace aquí, solo se solicita 0 accel.
            return SteeringOutput((0.0, 0.0), 0.0)

        # 2) Actualizar orientación basada en la dirección hacia el objetivo
        #     Mantener la orientación actual si la dirección es nula.
        self.character.orientation = self.newOrientation(self.character.orientation, (dx, dz))

        # 3) Velocidad objetivo (magnitud)
        if dist > self.slow_radius:
            speed = self.max_speed
        else:
            ratio = dist / self.slow_radius
            speed = self.max_speed * ratio # Se puede ajustar la escala (lineal, cuadrática, etc.)

        # 4) Vector de velocidad deseada (normalizamos la dirección)
        desired_velocity = (dx / dist * speed, dz / dist * speed)

        # 5) Calcular aceleración deseada para alcanzar desired_velocity en time_to_target segundos.
        current_vx, current_vy = self.character.velocity
        steering_linear = (
            (desired_velocity[0] - current_vx) / self.time_to_target,
            (desired_velocity[1] - current_vy) / self.time_to_target,
        )

        # 6) Devolver steering (solo componente lineal). Angular se gestiona por el sistema de orientación.
        return SteeringOutput(steering_linear, 0.0)

    def newOrientation(self, current_orientation: float, velocity: Tuple[float, float]) -> float:
        """
        Devuelve la orientación (ángulo en radianes) derivada de la dirección del vector `velocity`.

        - Si velocity es (0,0) devuelve la orientación actual (no rotar).
        - Se usa atan2(y, x) → ángulo en radianes en el rango [-pi, pi].
        """
        if velocity == (0, 0):
            return current_orientation
        return math.atan2(velocity[1], velocity[0])