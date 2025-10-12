import math

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.align import Align

class LookWhereYoureGoing:
    """
    LookWhereYoureGoing behaviour: calcula orientación objetivo a partir
    de la velocidad actual del character y delega la rotación a Align.
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
            target=Kinematic(position=self.character.position, orientation=0.0, velocity=self.character.velocity, rotation=self.character.rotation),
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

    def get_steering(self) -> SteeringOutput:
        vx, vz = self.character.velocity
        # Si no hay velocidad, no rotamos hacia la dirección de movimiento
        if vx == 0 and vz == 0:
            return SteeringOutput((0.0, 0.0), 0.0)

        # Orientación objetivo basada en la velocidad
        target_orientation = math.atan2(vz, vx)

        explicit_target = Kinematic(
            position=self.character.position,
            orientation=target_orientation,
            velocity=self.character.velocity,
            rotation=self.character.rotation,
        )

        self._align.target = explicit_target
        return self._align.get_steering()