import math
from kinematics.kinematic import Kinematic, SteeringOutput

PI = math.pi
TWO_PI = 2.0 * PI

class Align:
    """
    Align behaviour.

    - Alinea la orientación de `character` con la de `target`.
    - Devuelve un SteeringOutput donde:
        * linear = (0.0, 0.0)
        * angular = aceleración angular deseada (radianes/seg^2)
    - Parametros:
        character: Kinematic que se girará
        target: Kinematic objetivo (usa target.orientation)
        target_radius: umbral de orientación donde se considera "ya alineado" (radianes)
        slow_radius: radio donde se empieza a desacelerar (radianes)
        time_to_target: tiempo deseado para alcanzar la rotación objetivo (segundos)
        max_rotation: velocidad angular máxima (radianes/seg)
        max_angular_accel: límite de aceleración angular (radianes/seg^2)
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
        self.target_radius = float(target_radius)
        self.slow_radius = float(slow_radius)
        self.time_to_target = float(max(1e-4, time_to_target))
        self.max_rotation = float(max_rotation)
        self.max_angular_accel = float(max_angular_accel)

    @staticmethod
    def _map_to_range(angle: float) -> float:
        """
        Map angle to range [-pi, pi].
        """
        return (angle + PI) % TWO_PI - PI

    def get_steering(self) -> SteeringOutput:
        """
        Calcula y devuelve SteeringOutput con la aceleración angular necesaria.
        Retorna None si ya está dentro de target_radius (sin cambios).
        """
        result = SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        # 1) Diferencia angular "naiva"
        rotation = self.target.orientation - self.character.orientation

        # 2) Mapear a [-pi, pi]
        rotation = self._map_to_range(rotation)
        rotation_size = abs(rotation)

        print("\n", rotation_size, " ", self.target_radius )
        # 3) Si ya llegamos, no hay steering
        if rotation_size < self.target_radius:
            return result

        # 4) Determinar targetRotation (velocidad angular deseada)
        if rotation_size > self.slow_radius:
            target_rotation = self.max_rotation
        else:
            target_rotation = self.max_rotation * rotation_size / self.slow_radius

        # Darle signo (dirección) a la rotación
        target_rotation *= rotation / rotation_size

        # 5) Calcular la aceleración angular necesaria para alcanzar target_rotation en time_to_target
        angular = (target_rotation - self.character.rotation) / self.time_to_target

        # 6) Limitar la aceleración angular a max_angular_accel
        angular_accel_mag = abs(angular)
        if angular_accel_mag > self.max_angular_accel:
            angular = (angular / angular_accel_mag) * self.max_angular_accel

        result.angular = angular
        return result