import math
from entity.kinematic import Kinematic, KinematicSteeringOutput
from configs.package import CONF

class KinematicSeek:
    """
    Descripción
        CLASE: Comportamiento KinematicSeek que calcula una velocidad objetivo
        para que `character` se dirija directamente hacia `target` a máxima velocidad.

    Atributos
        - character (Kinematic): kinematic que se moverá.
        - target (Kinematic): kinematic objetivo.
        - max_speed (float): velocidad máxima deseada (unidades/seg).

    Métodos y Funciones
        - get_steering(): calcula y devuelve el KinematicSteeringOutput con la velocidad objetivo.

    Propósito
        - Proveer una velocidad objetivo que haga que `character` se dirija de forma
          directa y eficiente hacia `target`, sin desaceleración.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 200.0
    ) -> None:
        # asignar atributos
        self.character = character
        self.target = target
        self.max_speed = float(max_speed)

    def get_steering(self) -> KinematicSteeringOutput:
        """
        Descripción
            MÉTODO: Calcula el KinematicSteeringOutput que dirige `character` hacia `target`.

        Argumentos
            - Ninguno

        Retorno
            - KinematicSteeringOutput: velocidad lineal objetivo (vector) y rotación = 0.0.
        """
        # 1. Calcular vector desde el character hacia el target
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]

        # 2. Calcular la distancia al objetivo
        dist = math.hypot(dx, dy)

        # 3. Manejar caso degenerado (distancia ~ 0) para evitar divisiones por cero
        if dist <= CONF.ALG.EPS:
            # devolver velocidad cero si ya está prácticamente en la misma posición
            return KinematicSteeringOutput((0.0, 0.0), 0.0)

        # 4. Normalizar dirección y aplicar magnitud max_speed
        dir_x = dx / dist
        dir_y = dy / dist
        target_velocity = (dir_x * self.max_speed, dir_y * self.max_speed)

        # 5. Devolver el KinematicSteeringOutput con la velocidad objetivo y sin rotación
        return KinematicSteeringOutput(target_velocity, 0.0)