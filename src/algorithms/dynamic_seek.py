import math
from entity.kinematic import Kinematic, SteeringOutput
from configs.package import CONF

class DynamicSeek:
    """
    Descripción
        CLASE: Comportamiento DynamicSeek que genera una aceleración lineal
        para que un kinematic se dirija directamente hacia un objetivo.

    Atributos
        - character (Kinematic): kinematic que se moverá.
        - target (Kinematic): kinematic objetivo.
        - max_acceleration (float): aceleración máxima aplicada.

    Métodos y Funciones
        - get_steering(): calcula y devuelve el SteeringOutput con la aceleración necesaria.

    Propósito
        - Proveer una aceleración dirigida al objetivo con magnitud limitada por max_acceleration,
          evitando divisiones por cero y manejando casos degenerados.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_acceleration: float = 300.0,
    ) -> None:
        # asignar atributos
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula el SteeringOutput para dirigir `character` hacia `target`.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: contiene la componente linear (ax, az) con la aceleración
              dirigida al objetivo y angular = 0.0.
        """
        # 1. Calcular vector desde character hacia target
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]

        # 2. Calcular distancia al objetivo y manejar caso degenerado (distancia cero)
        dist = math.hypot(dx, dz)
        if dist <= CONF.ALG.EPS:
            # si están prácticamente en la misma posición, no aplicar aceleración
            return SteeringOutput((0.0, 0.0), 0.0)

        # 3. Normalizar dirección y aplicar magnitud máxima de aceleración
        dir_x = dx / dist
        dir_z = dz / dist
        accel_x = dir_x * self.max_acceleration
        accel_z = dir_z * self.max_acceleration

        # 4. Devolver SteeringOutput con componente linear y sin componente angular
        return SteeringOutput((accel_x, accel_z), 0.0)