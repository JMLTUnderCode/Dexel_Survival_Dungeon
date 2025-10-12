import math

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.dynamic_arrive import DynamicArrive

EPS = 1e-6

class Pursue:
    """
    Pursue: predice posición futura del target y delega a DynamicArrive.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 150.0,
        target_radius: float = 40.0,
        slow_radius: float = 180.0,
        time_to_target: float = 0.1,
        max_acceleration: float = 300.0,
        max_prediction: float = 1.0,
    ) -> None:
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)
        self.max_prediction = float(max_prediction)
        self.arrive: DynamicArrive = DynamicArrive(
            character=self.character, 
            target=self.target, 
            max_speed=max_speed,
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_acceleration=self.max_acceleration
        )

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
        Calcula la predicción y delega a DynamicArrive con el target temporal.
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

        # Delegar a DynamicArrive con target temporal
        self.arrive.target = explicit_target
        self.arrive.max_acceleration = self.max_acceleration
        return self.arrive.get_steering()

