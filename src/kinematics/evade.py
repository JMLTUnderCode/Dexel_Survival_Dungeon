import math

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.dynamic_flee import DynamicFlee

EPS = 1e-6

class Evade:
    """
    Evade: predice posición futura del target y delega a DynamicFlee.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_acceleration: float = 300.0,
        max_prediction: float = 1.0,
        time_to_target: float = 0.1
    ) -> None:
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)
        self.max_prediction = float(max_prediction)
        self.time_to_target = float(max(1e-4, time_to_target))
        self._flee = DynamicFlee(character=self.character, target=self.target, max_acceleration=self.max_acceleration)

    def predict_target(self, prediction: float) -> Kinematic:
        """
        Predice la posición futura del target.
        """
        future_pos = (
            self.target.position[0] + self.target.velocity[0] * prediction,
            self.target.position[1] + self.target.velocity[1] * prediction,
        )
        return Kinematic(position=future_pos, orientation=self.target.orientation, velocity=self.target.velocity, rotation=self.target.rotation)

    def get_steering(self) -> SteeringOutput:
        """
        Devuelve SteeringOutput (aceleración).
        Calcula la predicción y delega a DynamicFlee con el target temporal.
        """
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]
        distance = math.hypot(dx, dy)
        speed = math.hypot(self.character.velocity[0], self.character.velocity[1])

        if speed < EPS:
            prediction = self.max_prediction
        else:
            prediction = distance / speed
            if prediction > self.max_prediction:
                prediction = self.max_prediction

        explicit_target = self.predict_target(prediction)

        self._flee.target = explicit_target
        self._flee.max_acceleration = self.max_acceleration
        return self._flee.get_steering()