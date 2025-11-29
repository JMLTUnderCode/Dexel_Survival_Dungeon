import math
from entity.kinematic import Kinematic, SteeringOutput
from algorithms.align import Align

class LookWhereYoureGoing:
    """
    Descripción
        CLASE: Comportamiento que orienta al personaje hacia la dirección de su
        velocidad actual y delega la rotación en Align.

    Atributos
        - character (Kinematic): kinematic que será orientado.
        - target (Kinematic): kinematic auxiliar usado para calcular orientación.
        - _align (Align): instancia delegada que genera la aceleración angular.

    Métodos y Funciones
        - get_steering(): calcula y devuelve el SteeringOutput de orientación.

    Propósito
        - Mantener la orientación del personaje alineada con su vector de movimiento
          para obtener un comportamiento natural al desplazarse.
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
        # 1. Guardar referencias a character y target
        self.character = character
        self.target = target

        # 2. Crear una instancia Align delegada usando un Kinematic temporal como target
        self._align = Align(
            character=self.character,
            target=Kinematic(position=self.character.position, orientation=0.0, velocity=self.character.velocity, rotation=self.character.rotation),
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            FUNCIÓN: Calcula el SteeringOutput que orienta al character hacia su
            dirección de movimiento actual delegando la rotación en Align.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: salida con componente linear = (0.0, 0.0) y componente
              angular calculada por Align.
        """
        # 1. Obtener componentes de velocidad actuales
        vx, vz = self.character.velocity

        # 2. Si no hay velocidad significativa, no generar steering para evitar jitter
        if abs(vx) < 1e-9 and abs(vz) < 1e-9:
            return SteeringOutput((0.0, 0.0), 0.0)

        # 3. Calcular la orientación objetivo a partir de la velocidad (atan2)
        target_orientation = math.atan2(vz, vx)

        # 4. Construir un Kinematic temporal que represente el objetivo con la orientación calculada
        explicit_target = Kinematic(
            position=self.character.position,
            orientation=target_orientation,
            velocity=self.character.velocity,
            rotation=self.character.rotation,
        )

        # 5. Actualizar el target de la instancia Align y delegar el cálculo del steering
        self._align.target = explicit_target
        steering = self._align.get_steering()

        # 6. Devolver el SteeringOutput resultante (la componente linear se mantiene en cero)
        return steering