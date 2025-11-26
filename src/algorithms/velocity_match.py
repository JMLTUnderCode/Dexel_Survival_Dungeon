import math
from entity.kinematic import Kinematic, SteeringOutput
from configs.package import CONF

class VelocityMatch:
    """
    Descripción
        CLASE: Comportamiento VelocityMatch que ajusta la aceleración del `character`
        para que su velocidad coincida con la del `target` en un tiempo objetivo.

    Atributos
        - character (Kinematic): kinematic cuyo movimiento será ajustado.
        - target (Kinematic): kinematic cuya velocidad se desea igualar.
        - max_acceleration (float): aceleración máxima permitida (unidades/seg^2).
        - time_to_target (float): tiempo deseado para igualar la velocidad (segundos).

    Métodos y Funciones
        - get_steering(): Calcula y devuelve el SteeringOutput con la aceleración necesaria.

    Propósito
        - Generar un SteeringOutput que lleve la velocidad del `character` a coincidir
          con la del `target` de forma estable y limitada por `max_acceleration`.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_acceleration: float = 300.0,
        time_to_target: float = 0.1,
    ) -> None:
        # asignar referencias y parámetros
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)
        # evitar divisiones por cero asegurando un mínimo usando la constante del proyecto
        self.time_to_target = float(max(CONF.ALG.EPS, time_to_target))

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula la aceleración necesaria para igualar la velocidad del target
            en `time_to_target` segundos, limitando la magnitud a `max_acceleration`.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: objeto con `linear`=(ax, ay) y `angular`=0.0 donde `ax, ay`
              son las aceleraciones calculadas para igualar la velocidad del target.
        """
        # 1. Obtener componentes de velocidad del target y del character
        tvx, tvy = self.target.velocity
        cvx, cvy = self.character.velocity

        # 2. Calcular aceleración deseada para igualar velocidades en time_to_target
        ax = (tvx - cvx) / self.time_to_target
        ay = (tvy - cvy) / self.time_to_target

        # 3. Limitar la magnitud de la aceleración a max_acceleration si es necesario
        mag = math.hypot(ax, ay)
        if mag > 0.0 and mag > self.max_acceleration:
            # 3.1 Escalar componentes para respetar el máximo permitido
            scale = self.max_acceleration / mag
            ax *= scale
            ay *= scale

        # 4. Construir y retornar el SteeringOutput resultante
        return SteeringOutput(linear=(ax, ay), angular=0.0)