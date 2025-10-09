from kinematic import Kinematic, SteeringOutput
import math

class KinematicSeek:
    """
    Algoritmo de KinematicSeek para bots que buscan un objetivo de manera directa.
    Permite que un NPC se dirija rápidamente hacia un target sin considerar desaceleraciones.
    """
    def __init__(self, character : Kinematic, target : Kinematic, max_speed : float):
        """
        - character: objeto que se moverá (debe tener position y velocity)
        - target: objeto objetivo (debe tener position)
        - max_speed: velocidad máxima del NPC
        """
        self.character = character
        self.target = target
        self.max_speed = max_speed

    def get_steering(self) -> SteeringOutput:
        """
        Calcula el SteeringOutput necesario para que el character se dirija directamente al target.
        - Siempre va a velocidad máxima hacia el objetivo.
        - No considera desaceleraciones ni radios de llegada.
        """
        # 1. Calcular vector y distancia al objetivo
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]
        dist = math.hypot(dx, dy)
            
        if dist == 0:
            # Ya está en el objetivo, no moverse
            return SteeringOutput((0, 0), 0)
        
        # 2. Calcular velocidad deseada (en dirección al objetivo a velocidad máxima)
        desired_velocity = (dx / dist * self.max_speed, dy / dist * self.max_speed)

        # 3. Calcular nueva orientación
        self.character.orientation = self.newOrientation(self.character.orientation, desired_velocity)
        
        return SteeringOutput(desired_velocity, 0)

    def newOrientation(self, current_orientation: float, velocity: tuple) -> float:
        """
        Calcula la nueva orientación basada en la dirección de la velocidad.
        Si la velocidad es cero, mantiene la orientación actual.
        """
        if velocity == (0, 0):
            return current_orientation
        return math.atan2(velocity[1], velocity[0])