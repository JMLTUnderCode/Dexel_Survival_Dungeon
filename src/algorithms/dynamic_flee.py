import math
from entity.kinematic import Kinematic, SteeringOutput
from configs.package import CONF

class DynamicFlee:
    """
    Descripción
        CLASE: Comportamiento DynamicFlee que genera una aceleración lineal
        para que un kinematic se aleje directamente de un objetivo.

    Atributos
        - character (Kinematic): kinematic que realizará el flee.
        - target (Kinematic): kinematic objetivo del que escapar.
        - max_acceleration (float): aceleración máxima aplicada en la dirección de escape.

    Métodos y Funciones
        - get_steering(): calcula y devuelve el SteeringOutput con la aceleración lineal necesaria.

    Propósito
        - Proveer un steering que impulse al personaje en dirección opuesta al objetivo,
          respetando un límite de aceleración y manejando casos degenerados (distancia 0).
    """
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float = 300.0) -> None:
        # asignar atributos
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula el SteeringOutput para alejarse del target usando una
            aceleración dirigida opuesta a la posición del objetivo.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: contiene la componente linear (ax, az) con la aceleración
              deseada y angular = 0.0.
        """
        # 1. Calcular vector desde target hacia character (dirección de escape)
        dx = self.character.position[0] - self.target.position[0]
        dz = self.character.position[1] - self.target.position[1]

        # 2. Calcular la distancia; si es cero usamos una dirección arbitraria para evitar NaNs
        dist = math.hypot(dx, dz)
        if dist <= CONF.ALG.EPS:
            # 2.1 Si estan en la misma posición, elegir un vector unitario fijo (ej. eje X)
            escape_dir = (1.0, 0.0)
        else:
            # 2.2 Normalizar el vector de escape
            escape_dir = (dx / dist, dz / dist)

        # 3. Construir la aceleración objetivo con magnitud max_acceleration en la dirección de escape
        accel_x = escape_dir[0] * self.max_acceleration
        accel_z = escape_dir[1] * self.max_acceleration

        # 4. Retornar SteeringOutput con componente linear igual a la aceleración calculada y angular = 0.0
        return SteeringOutput((accel_x, accel_z), 0.0)