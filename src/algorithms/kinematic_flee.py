import math
from entity.kinematic import Kinematic, KinematicSteeringOutput
from configs.package import CONF

class KinematicFlee:
    """
    Descripción
        CLASE: Comportamiento KinematicFlee que calcula una velocidad objetivo
        para que `character` se aleje directamente de `target` a máxima velocidad.

    Atributos
        - character (Kinematic): kinematic que se moverá.
        - target (Kinematic): kinematic objetivo del que escapar.
        - max_speed (float): velocidad máxima deseada (unidades/seg).

    Métodos y Funciones
        - get_steering(): devuelve la velocidad objetivo para el flee.

    Propósito
        - Proveer una velocidad objetivo que haga al `character` desplazarse
          en dirección opuesta a `target` de forma directa y eficiente.
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
            MÉTODO: Calcula el KinematicSteeringOutput para alejarse directamente del target.

        Argumentos
            - Ninguno

        Retorno
            - KinematicSteeringOutput: objeto con la velocidad lineal objetivo y rotación 0.0.
        """
        # 1. Calcular vector desde el target hacia el character y su magnitud
        dx = self.character.position[0] - self.target.position[0]
        dy = self.character.position[1] - self.target.position[1]
        dist = math.hypot(dx, dy)

        # 2. Manejar caso degenerado (misma posición): elegir una dirección arbitraria
        if dist <= CONF.ALG.EPS:
            # usar eje X como dirección por defecto para evitar NaNs
            target_velocity = (self.max_speed, 0.0)
        else:
            # 3. Normalizar dirección y aplicar magnitud max_speed
            target_velocity = (dx / dist * self.max_speed, dy / dist * self.max_speed)

        # 4. Retornar el KinematicSteeringOutput con la velocidad objetivo y sin rotación
        return KinematicSteeringOutput(target_velocity, 0.0)