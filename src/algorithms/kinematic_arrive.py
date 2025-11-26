import math
from entity.kinematic import Kinematic, KinematicSteeringOutput

class KinematicArrive:
    """
    Descripción
        CLASE: Comportamiento kinematic arrive que calcula una velocidad objetivo
        para acercar un `character` a un `target` de forma suave y controlada.

    Atributos
        - character (Kinematic): kinematic que se moverá hacia el objetivo.
        - target (Kinematic): kinematic objetivo cuya posición se desea alcanzar.
        - max_speed (float): velocidad máxima deseada (unidades/seg).
        - target_radius (float): distancia a la que se considera que se ha llegado (unidades).
        - time_to_target (float): tiempo objetivo para alcanzar la velocidad deseada (segundos).

    Métodos y Funciones
        - get_steering(): calcula y devuelve el KinematicSteeringOutput con la velocidad objetivo.

    Propósito
        - Generar un KinematicSteeringOutput que permita al `character` aproximarse
          al `target` deteniéndose dentro de `target_radius` y desacelerando de forma suave.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 200.0,
        target_radius: float = 40.0,
        time_to_target: float = 0.15,
    ) -> None:
        # Inicializar atributos sin docstring (convención: __init__ sin docstring)
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)
        self.target_radius = float(target_radius)
        self.time_to_target = float(time_to_target)

    def get_steering(self) -> KinematicSteeringOutput:
        """
        Descripción
            MÉTODO: Calcula y devuelve el KinematicSteeringOutput que mueve el
            `character` hacia el `target` de forma suavizada.

        Argumentos
            - Ninguno

        Retorno
            - KinematicSteeringOutput: salida con la velocidad objetivo (linear) y rotación angular (0.0).
        """
        # 1. Calcular el vector desde el character hasta el target
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]

        # 2. Calcular la distancia y comprobar si ya se alcanzó el objetivo
        dist = math.hypot(dx, dz)
        if dist <= self.target_radius:
            # Si está dentro del umbral de llegada, devolver velocidad cero (llegado)
            return KinematicSteeringOutput((0.0, 0.0), 0.0)

        # 3. Calcular la velocidad objetivo necesaria para acercarse en time_to_target segundos
        #    (esto produce una velocidad proporcional a la distancia)
        target_velocity = (dx / self.time_to_target, dz / self.time_to_target)

        # 4. Limitar la magnitud de la velocidad objetivo a max_speed
        vel_mag = math.hypot(target_velocity[0], target_velocity[1])
        if vel_mag > self.max_speed:
            target_velocity = (
                target_velocity[0] / vel_mag * self.max_speed,
                target_velocity[1] / vel_mag * self.max_speed,
            )

        # 5. Devolver el KinematicSteeringOutput con la velocidad deseada y sin rotación
        return KinematicSteeringOutput(target_velocity, 0.0)