import math
from entity.kinematic import Kinematic, SteeringOutput
from algorithms.dynamic_flee import DynamicFlee
from configs.package import CONF

class Evade:
    """
    Descripción
        CLASE: Evade que predice la posición futura del objetivo y delega la
        lógica de escape a DynamicFlee para generar el steering necesario.

    Atributos
        - character (Kinematic): kinematic que realizará la evasión.
        - target (Kinematic): kinematic objetivo al que se evadirá.
        - max_acceleration (float): aceleración máxima aplicada durante la evasión.
        - max_prediction (float): tiempo máximo de predicción (segundos).
        - _flee (DynamicFlee): instancia delegada que produce el SteeringOutput final.

    Métodos y Funciones
        - predict_target(prediction): predice la posición futura del target.
        - get_steering(): calcula y devuelve el SteeringOutput de evasión.

    Propósito
        - Prever dónde estará el objetivo y forzar al character a alejarse usando
          DynamicFlee, respetando límites de aceleración y evitando divisiones por cero.
    """

    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_acceleration: float = 300.0,
        max_prediction: float = 1.0
    ) -> None:
        # asignar atributos internos sin docstring según convención
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)
        self.max_prediction = float(max_prediction)
        # crear la instancia delegada de flee con parámetros iniciales
        self._flee = DynamicFlee(character=self.character, target=self.target, max_acceleration=self.max_acceleration)

    def predict_target(self, prediction: float) -> Kinematic:
        """
        Descripción
            FUNCIÓN: Predice la posición futura del target usando su velocidad actual.

        Argumentos
            - prediction (float): tiempo en segundos hacia el futuro para la predicción.

        Retorno
            - Kinematic: objeto temporal con la posición predicha y demás atributos copiados.
        """
        # 1. Calcular posición futura simple usando velocidad constante
        future_pos = (
            self.target.position[0] + self.target.velocity[0] * prediction,
            self.target.position[1] + self.target.velocity[1] * prediction,
        )

        # 2. Construir y devolver un Kinematic temporal con la posición futura
        return Kinematic(
            position=future_pos,
            orientation=self.target.orientation,
            velocity=self.target.velocity,
            rotation=self.target.rotation,
        )

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula y devuelve el SteeringOutput de evasión.
        
        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: salida de steering calculada por la delegación a DynamicFlee.
        """
        # 1. Calcular vector y distancia actual entre character y target
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]
        distance = math.hypot(dx, dy)

        # 2. Calcular velocidad actual del character
        speed = math.hypot(self.character.velocity[0], self.character.velocity[1])

        # 3. Determinar tiempo de predicción:
        #    - si la velocidad es casi cero usamos el máximo permitido
        #    - en otro caso usamos distance / speed limitado por max_prediction
        if speed < CONF.ALG.EPS:
            prediction = self.max_prediction
        else:
            prediction = distance / speed
            if prediction > self.max_prediction:
                prediction = self.max_prediction

        # 4. Generar target explícito predicho usando la función de predicción
        explicit_target = self.predict_target(prediction)

        # 5. Actualizar la instancia delegada DynamicFlee para que use el target predicho
        self._flee.target = explicit_target
        # 5.1 asegurar que la aceleración máxima de la delegada está sincronizada
        self._flee.max_acceleration = self.max_acceleration

        # 6. Delegar el cálculo final a DynamicFlee y devolver su SteeringOutput
        return self._flee.get_steering()