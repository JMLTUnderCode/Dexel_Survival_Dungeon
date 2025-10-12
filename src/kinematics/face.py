import math

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.align import Align

class Face:
    """
    Face behaviour: calcula la orientación hacia la posición del objetivo
    y delega la rotación a Align (retorna SteeringOutput con componente angular).
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        target_radius: float = 0.05,
        slow_radius: float = 0.5,
        time_to_target: float = 0.1,
        max_rotation: float = 3.0,
        max_angular_accel: float = 8.0,
    ) -> None:
        self.character = character
        self.target = target
        self._align = Align(
            character=self.character,
            target=Kinematic(position=self.target.position, orientation=0.0, velocity=self.target.velocity, rotation=self.target.rotation),
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

    def get_steering(self) -> SteeringOutput:
        # Dirección hacia el objetivo (x, y)
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]

        # Si no hay dirección, no hacemos nada (sin jitter)
        if dx == 0 and dz == 0:
            return SteeringOutput((0.0, 0.0), 0.0)

        # Calcular orientación objetivo.
        target_orientation = math.atan2(dz, dx)

        # Crear target temporal para pasar a Align (evitar mutar el target real)
        explicit_target = Kinematic(
            position=self.target.position,
            orientation=target_orientation,
            velocity=self.target.velocity,
            rotation=self.target.rotation,
        )

        # Delegar a Align con el target temporal
        self._align.target = explicit_target
        return self._align.get_steering()