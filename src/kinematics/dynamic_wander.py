import math
import random
from typing import Tuple

from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.face import Face

class DynamicWander:
    """
    Dynamic Wander (delegated) behaviour.

    Descripción
    - Sitúa un objetivo en una circunferencia "wander circle" situada
      delante del personaje (wander_offset) y con radio (wander_radius).
    - La orientación del punto sobre la circunferencia se desplaza cada
      frame por un pequeño delta aleatorio (wander_rate * randomBinomial()).
    - Delegamos la rotación a `Face` usando el objetivo calculado.
    - La componente lineal del `SteeringOutput` se fija como aceleración
      máxima en la dirección de la orientación actual del personaje,
      lo que genera un movimiento suave con rotación controlada por `Face`.

    Parámetros (constructor)
    - character: Kinematic que se moverá / orientará.
    - target: Kinematic (no usado directamente, pero mantenido por compatibilidad).
    - wander_offset: distancia delante del personaje donde se coloca el centro de la circunferencia.
    - wander_radius: radio de la circunferencia de wander.
    - wander_rate: máximo cambio por frame de la wanderOrientation (radianes).
    - wander_orientation: orientación actual del objetivo dentro de la circunferencia.
    - max_acceleration: aceleración lineal máxima aplicada como "empuje" forward.
    - target_radius/slow_radius/time_to_target/max_rotation/max_angular_accel:
      parámetros pasados al `Face` delegado (controlan la suavidad de la rotación).
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        target_radius: float = 0.05,
        slow_radius: float = 0.5,
        time_to_target: float = 0.1,
        max_acceleration: float = 300.0,
        max_rotation: float = 3.0,
        max_angular_accel: float = 8.0,
        wander_offset: float = 40.0,
        wander_radius: float = 20.0,
        wander_rate: float = 0.6,
        wander_orientation: float = 0.0,
    ) -> None:
        self.character = character
        self.target = target

        self.max_acceleration = float(max_acceleration)

        self.wander_offset = float(wander_offset)
        self.wander_radius = float(wander_radius)
        self.wander_rate = float(wander_rate)
        self.wander_orientation = float(wander_orientation)

        self.face = Face(
            character=self.character,
            target=Kinematic(position=self.character.position, orientation=0.0, velocity=self.character.velocity, rotation=self.character.rotation),
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

    def random_binomial(self) -> float:
        """Devuelve valor en [-1,1] centrado en 0 (random() - random())."""
        return random.random() - random.random()

    def orientation_to_vector(self,orientation: float) -> Tuple[float, float]:
        """Convierte una orientación (radianes) a un vector unitario (x, z)."""
        return (math.cos(orientation), math.sin(orientation))

    def get_steering(self) -> SteeringOutput:
        """
        Calcula y devuelve un SteeringOutput:
          - angular: delegada por Face (direccion hacia el objetivo wander).
          - linear: aceleración máxima hacia adelante según la orientación actual.

        Flujo:
        1) Actualizar wander_orientation: wander_orientation += randomBinomial() * wander_rate
        2) Calcular targetOrientation = wander_orientation + character.orientation
        3) Calcular center = character.position + wander_offset * orientation.asVector()
        4) Calcular target_pos = center + wander_radius * targetOrientation.asVector()
        5) Delegar rotación a Face usando explicit_target (posición y orientation)
        6) Colocar componente linear = max_acceleration * character.forward_vector
        7) Devolver SteeringOutput(linear, angular)
        """
        # 1) Actualizar orientación del punto en la circunferencia
        self.wander_orientation += self.random_binomial() * self.wander_rate

        # 2) Orientación combinada del objetivo en la circunferencia
        target_orientation = self.wander_orientation + self.character.orientation

        # 3) Centro de la circunferencia delante del personaje
        forward = self.orientation_to_vector(self.character.orientation)
        center_x = self.character.position[0] + self.wander_offset * forward[0]
        center_z = self.character.position[1] + self.wander_offset * forward[1]

        # 4) Posición objetivo sobre la circunferencia
        to_target = self.orientation_to_vector(target_orientation)
        target_x = center_x + self.wander_radius * to_target[0]
        target_z = center_z + self.wander_radius * to_target[1]

        # 5) Crear target temporal para Face (evitar mutar target real)
        explicit_target = Kinematic(
            position=(target_x, target_z),
            orientation=target_orientation,
            velocity=(0.0, 0.0),
            rotation=0.0,
        )

        # Delegar la rotación a Face (obtiene SteeringOutput.angular)
        self.face.target = explicit_target
        angular_steering = self.face.get_steering()

        # 6) Componente linear: empuje hacia adelante en dirección de orientation actual
        forward_vec = forward
        lin_x = forward_vec[0] * self.max_acceleration
        lin_z = forward_vec[1] * self.max_acceleration

        # 7) Construir resultado final: combinar linear + angular
        #    Face devuelve SteeringOutput(linear=(0,0), angular=...).
        result = SteeringOutput(linear=(lin_x, lin_z), angular=angular_steering.angular)

        return result