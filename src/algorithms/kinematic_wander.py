import math
import random
from entity.kinematic import Kinematic, KinematicSteeringOutput

class KinematicWander:
    """
    Descripción
        CLASE: Comportamiento kinematic wander que genera una velocidad objetivo
        y una rotación aleatoria suave para simular deambular.

    Atributos
        - character (Kinematic): kinematic que se moverá.
        - max_speed (float): velocidad objetivo en unidades/segundo.
        - max_rotation (float): magnitud máxima de cambio de rotación (radianes).

    Métodos y Funciones
        - _random_binomial(): devuelve un valor aleatorio en [-1,1] centrado en 0.
        - get_steering(): calcula y devuelve el KinematicSteeringOutput con la velocidad
          objetivo y la rotación aleatoria.

    Propósito
        - Proveer una salida kinemática que permita al personaje moverse en una
          dirección cambiable suavemente, ideal para NPCs que vagan sin objetivo.
    """
    def __init__(
        self,
        character: Kinematic,
        max_speed: float = 120.0,
        max_rotation: float = 1.0
    ) -> None:
        # 1. Guardar referencia al character y parámetros de comportamiento
        self.character = character
        self.max_speed = float(max_speed)
        self.max_rotation = float(max_rotation)

    @staticmethod
    def _random_binomial() -> float:
        """
        Descripción
            FUNCIÓN: Genera un valor en el rango [-1, 1] usando diferencia de dos uniformes.

        Argumentos
            - Ninguno

        Retorno
            - float: valor aleatorio en [-1, 1].
        """
        # 1. Generar dos valores uniformes en [0,1]
        a = random.random()
        b = random.random()
        # 2. Devolver su diferencia para centrar la distribución en 0
        return a - b

    def get_steering(self) -> KinematicSteeringOutput:
        """
        Descripción
            MÉTODO: Calcula el KinematicSteeringOutput para wandering.

        Argumentos
            - Ninguno

        Retorno
            - KinematicSteeringOutput: velocidad objetivo (linear) y rotación aleatoria (angular).
        """
        # 1. Obtener la orientación actual del character y convertirla a vector dirección
        ori = self.character.orientation
        dir_x = math.cos(ori)
        dir_z = math.sin(ori)

        # 2. Calcular la velocidad objetivo como dirección normalizada * max_speed
        target_velocity = (dir_x * self.max_speed, dir_z * self.max_speed)

        # 3. Generar una rotación aleatoria pequeña en el rango [-max_rotation, max_rotation]
        random_rot = self._random_binomial() * self.max_rotation

        # 4. Construir y devolver el resultado kinemático con la velocidad y la rotación
        return KinematicSteeringOutput(target_velocity, random_rot)