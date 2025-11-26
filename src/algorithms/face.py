import math
from entity.kinematic import Kinematic, SteeringOutput
from algorithms.align import Align

class Face:
    """
    Descripción
        CLASE: Comportamiento Face que calcula la orientación hacia la posición
        del objetivo y delega la rotación en Align para producir un SteeringOutput.

    Atributos
        - character (Kinematic): kinematic que será orientado.
        - target (Kinematic): kinematic objetivo cuya posición se usará para orientar.
        - _align (Align): instancia delegada que produce la aceleración angular.

    Métodos y Funciones
        - get_steering(): calcula y devuelve el SteeringOutput resultante.

    Propósito
        - Calcular la orientación deseada hacia el objetivo y delegar la generación
          de la aceleración angular en Align, manteniendo el character sin cambios
          indeseados en los datos del target real.
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

        # 2. Crear instancia Align delegada. Se crea un Kinematic temporal para target
        #    con orientation = 0.0; Align recibirá un target explícito en get_steering.
        self._align = Align(
            character=self.character,
            target=Kinematic(position=self.target.position, orientation=0.0, velocity=self.target.velocity, rotation=self.target.rotation),
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula la dirección hacia el objetivo, construye un target temporal
            y delega en Align la generación del SteeringOutput con componente angular.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: salida de steering con componente angular calculada por Align
              y componente linear a 0.0 (la componente lineal se gestiona por otros behaviours).
        """
        # 1. Calcular vector desde character hacia target (dx, dz)
        dx = self.target.position[0] - self.character.position[0]
        dz = self.target.position[1] - self.character.position[1]

        # 2. Si no existe dirección (misma posición), evitar jitter y no generar steering
        if abs(dx) < 1e-9 and abs(dz) < 1e-9:
            return SteeringOutput((0.0, 0.0), 0.0)

        # 3. Calcular la orientación objetivo usando atan2(dz, dx)
        target_orientation = math.atan2(dz, dx)

        # 4. Construir un Kinematic temporal que represente el objetivo con la orientación calculada
        explicit_target = Kinematic(
            position=self.target.position,
            orientation=target_orientation,
            velocity=self.target.velocity,
            rotation=self.target.rotation,
        )

        # 5. Actualizar el target de la instancia Align y delegar el cálculo
        self._align.target = explicit_target
        steering = self._align.get_steering()

        # 6. Devolver el SteeringOutput resultante (linear se mantiene en cero por convención)
        return steering