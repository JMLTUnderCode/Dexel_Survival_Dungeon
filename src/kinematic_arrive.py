from kinematic import Kinematic, SteeringOutput
import math

class KinematicArrive:
    """
    Algoritmo de KinematicArrive para bots que buscan acercarse suavemente a un objetivo.
    Permite que un NPC desacelere gradualmente al acercarse al target, evitando frenadas bruscas y logrando un movimiento natural.
    """
    def __init__(self, character : Kinematic, target : Kinematic, max_speed : float, target_radius : float, slow_radius : float, time_to_target : float, max_accel : float):
        """
        - character: objeto que se moverá (debe tener position y velocity)
        - target: objeto objetivo (debe tener position)
        - max_speed: velocidad máxima del NPC
        - target_radius: radio en el que se considera que el NPC ha llegado al objetivo
        - slow_radius: radio a partir del cual el NPC empieza a desacelerar
        - time_to_target: tiempo deseado para alcanzar la velocidad objetivo (controla la suavidad)
        - max_accel: aceleración máxima permitida (limita cambios bruscos)
        """
        self.character = character
        self.target = target
        self.max_speed = max_speed
        self.target_radius = target_radius
        self.slow_radius = slow_radius
        self.time_to_target = time_to_target
        self.max_accel = max_accel

    def get_steering(self) -> SteeringOutput:
        """
        Calcula el SteeringOutput necesario para que el character se acerque al target de forma suave.
        - Si está dentro de target_radius, se detiene completamente.
        - Si está dentro de slow_radius, desacelera suavemente usando una función cuadrática.
        - Si está fuera de slow_radius, va a velocidad máxima.
        - Limita la aceleración máxima para evitar cambios bruscos.
        """
        # 1. Calcular vector y distancia al objetivo
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]
        dist = math.hypot(dx, dy)
            
        if dist < self.target_radius:
            # 2. Si está dentro del radio objetivo, no moverse
            return SteeringOutput((0, 0), 0)
        # 3. Calcular velocidad deseada
        if dist > self.slow_radius:
            speed = self.max_speed  # Fuera del slow_radius, velocidad máxima
        else:
            # Dentro del slow_radius, desacelerar suavemente (cuadrático)
            speed = self.max_speed * (dist / self.slow_radius) ** 2
        # 4. Calcular vector de velocidad deseada (en dirección al objetivo)
        desired_velocity = (dx / dist * speed, dy / dist * speed)
        # 5. Calcular steering: diferencia entre velocidad deseada y actual, ajustada por time_to_target
        steering_linear = (
            (desired_velocity[0] - self.character.velocity[0]) / self.time_to_target,
            (desired_velocity[1] - self.character.velocity[1]) / self.time_to_target
        )
        # 6. Limitar la aceleración máxima para evitar cambios bruscos
        accel_mag = math.hypot(*steering_linear)
        if accel_mag > self.max_accel:
            steering_linear = (
                steering_linear[0] / accel_mag * self.max_accel,
                steering_linear[1] / accel_mag * self.max_accel
            )

        # 7. Calcular nueva orientación
        self.character.orientation = self.newOrientation(self.character.orientation, desired_velocity)

        # 8. SteeringOutput: solo steering lineal, sin rotación angular
        return SteeringOutput(steering_linear, 0)
    
    def newOrientation(self, current_orientation: float, velocity: tuple) -> float:
        """
        Calcula la nueva orientación basada en la dirección de la velocidad.
        Si la velocidad es cero, mantiene la orientación actual.
        """
        if velocity == (0, 0):
            return current_orientation
        return math.atan2(velocity[1], velocity[0])