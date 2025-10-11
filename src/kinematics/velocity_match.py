import math

from kinematics.kinematic import Kinematic, SteeringOutput

class VelocityMatch:
    """
    Velocity Matching behaviour.

    - Intenta que la velocidad del `character` coincida con la de `target`
      en `time_to_target` segundos, limitando la aceleración a `max_acceleration`.
    - Devuelve un `SteeringOutput` con componente linear = (ax, ay) y angular = 0.0.
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_acceleration: float = 300.0,
        time_to_target: float = 0.1,
    ) -> None:
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)
        # evitar división por cero
        self.time_to_target = float(max(1e-4, time_to_target))

    def get_steering(self) -> SteeringOutput:
        """
        Calcula la aceleración necesaria para igualar la velocidad del target.
        """
        # Computar aceleración deseada para igualar velocidades en time_to_target
        tvx, tvy = self.target.velocity
        cvx, cvy = self.character.velocity

        ax = (tvx - cvx) / self.time_to_target
        ay = (tvy - cvy) / self.time_to_target

        # Limitar magnitud de aceleración
        mag = math.hypot(ax, ay)
        if mag > self.max_acceleration and mag > 0:
            scale = self.max_acceleration / mag
            ax *= scale
            ay *= scale

        return SteeringOutput(linear=(ax, ay), angular=0.0)