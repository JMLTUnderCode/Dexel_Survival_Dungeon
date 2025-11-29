from entity.kinematic import Kinematic, SteeringOutput
from configs.package import CONF

class Align:
    """
    Descripción
        CLASE: Comportamiento de alineación que ajusta la orientación de un kinematic
        para apuntar hacia la orientación objetivo de otro kinematic.

    Atributos
        - character (Kinematic): kinematic que será alineado.
        - target (Kinematic): kinematic objetivo cuya orientación se pretende alcanzar.
        - target_radius (float): umbral en radianes donde se considera ya alineado.
        - slow_radius (float): radio en radianes donde se empieza a reducir la velocidad.
        - time_to_target (float): tiempo objetivo para alcanzar la rotación deseada.
        - max_rotation (float): velocidad angular máxima permitida.
        - max_angular_accel (float): aceleración angular máxima permitida.

    Métodos y Funciones
        - _map_to_range(angle): normaliza un ángulo al intervalo [-pi, pi].
        - get_steering(): calcula y devuelve el SteeringOutput con la aceleración angular necesaria.

    Propósito
        - Proveer una aceleración angular que lleve la orientación de `character`
          a coincidir con la orientación de `target` de forma suave y limitada.
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
        # asignar atributos
        self.character = character
        self.target = target
        self.target_radius = float(target_radius)
        self.slow_radius = float(slow_radius)
        # evitar división por cero al calcular aceleración
        self.time_to_target = float(max(CONF.ALG.EPS, time_to_target))
        self.max_rotation = float(max_rotation)
        self.max_angular_accel = float(max_angular_accel)

    @staticmethod
    def _map_to_range(angle: float) -> float:
        """
        Descripción
            FUNCIÓN: Normaliza un ángulo al rango [-pi, pi].

        Argumentos
            - angle (float): ángulo en radianes a normalizar.

        Retorno
            - float: ángulo normalizado en [-pi, pi].
        """
        # 1. Ajustar el ángulo sumando PI para facilitar el módulo
        # 2. Aplicar módulo de 2*PI y re-centrar en [-PI, PI]
        return (angle + CONF.CONST.PI) % (2.0 * CONF.CONST.PI) - CONF.CONST.PI

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula la aceleración angular necesaria para alinear `character`
            con la orientación de `target`. Devuelve un SteeringOutput con `linear`
            en (0.0, 0.0) y `angular` con la aceleración calculada.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: objeto con los componentes `linear` y `angular`.
        """
        # 1. Inicializar resultado sin componente lineal
        result = SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        # 2. Calcular diferencia angular entre target y character
        rotation = self.target.orientation - self.character.orientation

        # 3. Normalizar la diferencia al rango [-pi, pi]
        rotation = self._map_to_range(rotation)
        rotation_size = abs(rotation)

        # 4. Si ya estamos dentro del umbral objetivo, no aplicar aceleración
        if rotation_size < self.target_radius:
            return result

        # 5. Determinar la velocidad angular objetivo:
        #    - fuera de slow_radius -> max_rotation
        #    - dentro de slow_radius -> escala proporcional
        if rotation_size > self.slow_radius:
            target_rotation = self.max_rotation
        else:
            target_rotation = self.max_rotation * rotation_size / self.slow_radius

        # 6. Aplicar signo según dirección deseada
        target_rotation *= rotation / rotation_size

        # 7. Calcular la aceleración angular necesaria para alcanzar target_rotation en time_to_target
        angular = (target_rotation - self.character.rotation) / self.time_to_target

        # 8. Limitar la magnitud de la aceleración a max_angular_accel
        angular_accel_mag = abs(angular)
        if angular_accel_mag > self.max_angular_accel:
            angular = (angular / angular_accel_mag) * self.max_angular_accel

        # 9. Asignar componente angular al resultado y devolver
        result.angular = angular
        return result