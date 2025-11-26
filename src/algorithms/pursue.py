import math
from entity.kinematic import Kinematic, SteeringOutput
from algorithms.dynamic_arrive import DynamicArrive
from configs.package import CONF

class Pursue:
    """
    Descripción
        CLASE: Comportamiento Pursue que predice la posición futura del objetivo
        y delega la generación de aceleración en DynamicArrive.

    Atributos
        - character (Kinematic): kinematic que realizará la persecución.
        - target (Kinematic): kinematic objetivo a perseguir.
        - max_acceleration (float): aceleración máxima permitida para el arrive delegado.
        - max_prediction (float): tiempo máximo de predicción (segundos).
        - arrive (DynamicArrive): instancia delegada que produce el SteeringOutput de llegada.

    Métodos y Funciones
        - _predict_target(prediction): predice la posición futura del objetivo.
        - get_steering(): calcula y devuelve el SteeringOutput de persecución.

    Propósito
        - Prever la posición futura del target en función de su velocidad actual y
          usar DynamicArrive para generar la aceleración necesaria para interceptarlo.
    """
    def __init__(
        self,
        character: Kinematic,
        target: Kinematic,
        max_speed: float = 150.0,
        target_radius: float = 40.0,
        slow_radius: float = 180.0,
        time_to_target: float = 0.1,
        max_acceleration: float = 300.0,
        max_prediction: float = 1.0,
    ) -> None:
        # asignar referencias y parámetros
        self.character = character
        self.target = target
        self.max_acceleration = float(max_acceleration)
        self.max_prediction = float(max_prediction)

        # crear la instancia delegada DynamicArrive con parámetros iniciales
        self.arrive: DynamicArrive = DynamicArrive(
            character=self.character,
            target=self.target,
            max_speed=max_speed,
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_acceleration=self.max_acceleration,
        )

    def _predict_target(self, prediction: float) -> Kinematic:
        """
        Descripción
            FUNCIÓN: Predice la posición futura del target usando su velocidad actual.

        Argumentos
            - prediction (float): tiempo en segundos hacia el futuro para la predicción.

        Retorno
            - Kinematic: kinematic temporal con la posición predicha y atributos copiados.
        """
        # 1. Calcular la posición futura asumiendo velocidad constante
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
            MÉTODO: Calcula y devuelve el SteeringOutput de persecución delegando
            en DynamicArrive con un target predicho.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: aceleración resultante para perseguir/interceptar al objetivo.
        """
        # 1. Calcular vector y distancia actual entre character y target
        dx = self.target.position[0] - self.character.position[0]
        dy = self.target.position[1] - self.character.position[1]
        distance = math.hypot(dx, dy)

        # 2. Calcular la velocidad actual del character
        speed = math.hypot(self.character.velocity[0], self.character.velocity[1])

        # 3. Determinar el tiempo de predicción:
        #    - si la velocidad es aproximadamente cero usar el máximo permitido
        #    - en otro caso usar distance / speed y limitar por max_prediction
        if speed < CONF.ALG.EPS:
            prediction = self.max_prediction
        else:
            prediction = distance / speed
            if prediction > self.max_prediction:
                prediction = self.max_prediction

        # 4. Generar un target explícito predicho usando la función _predict_target
        explicit_target = self._predict_target(prediction)

        # 5. Actualizar la instancia DynamicArrive con el target predicho y sincronizar parámetros
        self.arrive.target = explicit_target
        self.arrive.max_acceleration = self.max_acceleration

        # 6. Delegar el cálculo final a DynamicArrive y devolver su SteeringOutput
        return self.arrive.get_steering()