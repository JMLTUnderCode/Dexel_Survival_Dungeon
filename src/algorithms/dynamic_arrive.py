import math
from entity.kinematic import Kinematic, SteeringOutput

class DynamicArrive:
    """
    Descripción
        CLASE: Comportamiento DynamicArrive que genera una aceleración lineal
        para que un kinematic alcance suavemente a un target.

    Atributos
        - character (Kinematic): kinematic que se moverá hacia el objetivo.
        - target (Kinematic): kinematic objetivo que provee la posición destino.
        - max_speed (float): velocidad máxima deseada (unidades/segundo).
        - target_radius (float): distancia a la que se considera que ha llegado (unidades).
        - slow_radius (float): radio desde el cual se empieza a desacelerar (unidades).
        - time_to_target (float): tiempo objetivo para alcanzar la velocidad deseada (segundos).
        - max_acceleration (float): aceleración máxima permitida (unidades/segundo²).

    Métodos y Funciones
        - get_steering(): calcula y devuelve un SteeringOutput con la aceleración lineal necesaria.

    Propósito
        - Proveer un steering lineal que detenga al character en el umbral, reduzca velocidad
          dentro de slow_radius y limite la aceleración máxima.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 200.0,
        target_radius: float = 40.0,
        slow_radius: float = 180.0,
        time_to_target: float = 0.15,
        max_acceleration: float = 300.0,
    ) -> None:
        # asignar atributos
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)
        self.target_radius = float(target_radius)
        self.slow_radius = float(slow_radius)
        self.time_to_target = float(time_to_target)
        self.max_acceleration = float(max_acceleration)

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula y devuelve un SteeringOutput con la aceleración lineal necesaria.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: componente linear (ax, az) y angular (0.0).
        """
        # 1. Calcular vector hacia target (dx, dz)
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]

        # 2. Calcular distancia; si está dentro de target_radius devolver cero (llegado)
        dist = math.hypot(dx, dz)
        if dist <= self.target_radius:
            return SteeringOutput((0.0, 0.0), 0.0)

        # 3. Determinar la velocidad objetivo (magnitud)
        if dist > self.slow_radius:
            target_speed = self.max_speed
        else:
            target_speed = self.max_speed * dist / self.slow_radius

        # 4. Construir target_velocity (dirección normalizada * target_speed)
        target_velocity = (dx, dz)
        mag = math.hypot(target_velocity[0], target_velocity[1])
        if mag == 0.0:
            target_velocity = (0.0, 0.0)
        else:
            target_velocity = (
                target_velocity[0] / mag * target_speed,
                target_velocity[1] / mag * target_speed,
            )

        # 5. Calcular la aceleración necesaria para alcanzar target_velocity en time_to_target
        current_vx, current_vy = self.character.velocity
        steering_linear = (
            (target_velocity[0] - current_vx) / self.time_to_target,
            (target_velocity[1] - current_vy) / self.time_to_target,
        )

        # 6. Limitar la magnitud de la aceleración a max_acceleration
        mag = math.hypot(steering_linear[0], steering_linear[1])
        if mag > self.max_acceleration:
            steering_linear = (
                steering_linear[0] / mag * self.max_acceleration,
                steering_linear[1] / mag * self.max_acceleration,
            )

        # 7. Devolver SteeringOutput con componente linear calculada y angular = 0.0
        return SteeringOutput(steering_linear, 0.0)