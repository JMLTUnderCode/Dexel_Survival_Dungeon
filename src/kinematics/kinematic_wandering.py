import math
import random

from kinematics.kinematic import Kinematic, SteeringOutput

class KinematicWander:
    """
    Kinematic Wander behaviour.

    Objetivo:
    - Mover el character en una dirección aleatoria que cambia suavemente con el tiempo.
    - Simula un movimiento errático pero natural, ideal para NPCs que deambulan sin un objetivo fijo.

    Parámetros (constructor):
    - character: Kinematic que se moverá.
    - max_speed: velocidad objetivo en píxeles/segundo.
    - max_rotation: magnitud máxima (radianes/segundo) del cambio aleatorio de rotación.
    """

    def __init__(
        self,
        character: Kinematic,
        max_speed: float = 120.0,
        max_rotation: float = 1.0
    ) -> None:
        self.character = character
        self.max_speed = float(max_speed)
        self.max_rotation = float(max_rotation)

    @staticmethod
    def random_binomial() -> float:
        """
        Devuelve un número en [-1, 1] con distribución aproximada binomial (random() - random()).
        Útil para obtener cambios positivos/negativos centrados en 0.
        """
        return random.random() - random.random()

    def get_steering(self) -> SteeringOutput:
        """
        Calcula el SteeringOutput para wandering.

        Flujo:
        1) Usa la orientación actual del character para obtener la dirección en vector.
        2) Calcula la velocidad objetivo = direction * max_speed.
        3) Genera una rotación aleatoria pequeña en [-max_rotation, max_rotation].
        4) Retorna SteeringOutput(linear=desired_velocity, angular=random_rotation)
        """
        # 1) Dirección desde la orientación (orientación en radianes)
        ori = self.character.orientation
        dir_x = math.cos(ori)
        dir_z = math.sin(ori)

        # 2) Velocidad objetivo
        desired_vx = dir_x * self.max_speed
        desired_vz = dir_z * self.max_speed

        # 3) Rotación aleatoria (pequeño cambio para vagar)
        random_rot = self.random_binomial() * self.max_rotation

        return SteeringOutput((desired_vx, desired_vz), random_rot)