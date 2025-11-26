import math
import random
from typing import Tuple
from entity.kinematic import Kinematic, SteeringOutput
from algorithms.face import Face

class DynamicWander:
    """
    Descripción
        CLASE: Comportamiento DynamicWander que genera movimiento aleatorio suave
        (wander) delegando la rotación en el comportamiento Face.

    Atributos
        - character (Kinematic): kinematic que se moverá.
        - target (Kinematic): kinematic objetivo de compatibilidad (no usado directamente).
        - wander_offset (float): distancia delante del personaje donde se sitúa el centro de la "wander circle".
        - wander_radius (float): radio de la circunferencia de wander.
        - wander_rate (float): máximo cambio por frame de la orientación del objetivo en la circunferencia.
        - wander_orientation (float): orientación actual del punto objetivo en la circunferencia.
        - max_acceleration (float): aceleración lineal máxima aplicada como impulso hacia adelante.
        - face (Face): instancia delegada para controlar la rotación del personaje.

    Métodos y Funciones
        - _random_binomial(): devuelve valor aleatorio en [-1,1] centrado en 0.
        - _orientation_to_vector(orientation): convierte orientación (radianes) a vector unitario (x,z).
        - get_steering(): calcula el SteeringOutput combinando empuje forward y rotación delegada.

    Propósito
        - Proveer un comportamiento de wander que mantenga movimiento hacia adelante y use Face
          para orientar suavemente hacia un punto móvil sobre una circunferencia frontal.
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
        # asignar atributos sin docstring según convención
        self.character = character
        self.target = target

        self.max_acceleration = float(max_acceleration)

        self.wander_offset = float(wander_offset)
        self.wander_radius = float(wander_radius)
        self.wander_rate = float(wander_rate)
        self.wander_orientation = float(wander_orientation)

        # crear instancia Face delegada para controlar la rotación
        self.face = Face(
            character=self.character,
            target=Kinematic(position=self.character.position, orientation=0.0, velocity=self.character.velocity, rotation=self.character.rotation),
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

    def _random_binomial(self) -> float:
        """
        Descripción
            FUNCIÓN: Genera un valor en el rango [-1, 1] centrado en 0 usando diferencia de dos uniformes.

        Argumentos
            - Ninguno

        Retorno
            - float: valor aleatorio en [-1,1]
        """
        # 1. Generar dos valores uniformes y devolver su diferencia para centrar en 0
        return random.random() - random.random()

    def _orientation_to_vector(self, orientation: float) -> Tuple[float, float]:
        """
        Descripción
            FUNCIÓN: Convierte una orientación en radianes a un vector unitario (x, z).

        Argumentos
            - orientation (float): orientación en radianes.

        Retorno
            - Tuple[float, float]: vector unitario (x, z).
        """
        # 1. Calcular coseno/seno para obtener vector unitario en el plano XZ
        return (math.cos(orientation), math.sin(orientation))

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula y devuelve un SteeringOutput que combina:
                - componente linear: empuje hacia adelante (max_acceleration)
                - componente angular: delegada por Face apuntando a un objetivo en la circunferencia de wander

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: objeto con `linear` (ax, az) y `angular` calculados.
        """
        # 1. Actualizar la orientación del punto objetivo en la circunferencia con un pequeño delta aleatorio
        self.wander_orientation += self._random_binomial() * self.wander_rate

        # 2. Combinar la wander_orientation con la orientación actual del personaje para obtener target_orientation
        target_orientation = self.wander_orientation + self.character.orientation

        # 3. Calcular el vector forward del personaje a partir de su orientación actual
        forward = self._orientation_to_vector(self.character.orientation)

        # 4. Calcular el centro de la circunferencia: posición adelante del personaje
        center_x = self.character.position[0] + self.wander_offset * forward[0]
        center_z = self.character.position[1] + self.wander_offset * forward[1]

        # 5. Calcular la posición objetivo sobre la circunferencia usando target_orientation
        to_target = self._orientation_to_vector(target_orientation)
        target_x = center_x + self.wander_radius * to_target[0]
        target_z = center_z + self.wander_radius * to_target[1]

        # 6. Construir un target temporal (Kinematic) para delegar la rotación en Face
        explicit_target = Kinematic(
            position=(target_x, target_z),
            orientation=target_orientation,
            velocity=(0.0, 0.0),
            rotation=0.0,
        )

        # 7. Actualizar el target de la instancia Face y obtener el steering angular resultante
        self.face.target = explicit_target
        angular_steering = self.face.get_steering()

        # 8. Calcular la componente linear: empuje hacia adelante usando max_acceleration
        lin_x = forward[0] * self.max_acceleration
        lin_z = forward[1] * self.max_acceleration

        # 9. Construir y devolver el SteeringOutput combinando linear y angular
        result = SteeringOutput(linear=(lin_x, lin_z), angular=angular_steering.angular)
        return result