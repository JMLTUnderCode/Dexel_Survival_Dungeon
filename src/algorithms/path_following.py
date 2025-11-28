from entity.kinematic import Kinematic, SteeringOutput
from algorithms.dynamic_seek import DynamicSeek
from map.paths import Path

class FollowPath:
    """
    Descripción
        CLASE: Comportamiento FollowPath (chase-the-rabbit) que sigue una ruta
        polilínea avanzando un offset a partir del punto más cercano.

    Atributos
        - character (Kinematic): kinematic que seguirá la ruta.
        - path (Path): objeto que representa la ruta (debe exponer get_param/get_position).
        - offset (float): distancia a lo largo de la ruta para definir el objetivo.
        - current_param (float): parámetro estimado actual en la ruta (se mantiene entre frames).
        - max_acceleration (float): aceleración máxima pasada al DynamicSeek.
        - dummy_target (Kinematic): target temporal usado para delegar en DynamicSeek.
        - _seek (DynamicSeek): instancia delegada que calcula el steering lineal.

    Métodos y Funciones
        - get_steering(): Calcula y devuelve el SteeringOutput delegando en DynamicSeek.

    Propósito
        - Proveer un objetivo puntual sobre la ruta y delegar la persecución de ese objetivo
          a DynamicSeek, manteniendo la orientación separada (por ejemplo Face o LookWhereYoureGoing).
    """
    def __init__(
        self,
        character: Kinematic,
        path: Path,
        offset: float = 12.0,
        current_param: float = 0.0,
        max_acceleration: float = 300.0,
    ) -> None:
        # 1. Guardar referencias y parámetros del comportamiento
        self.character = character
        self.path = path
        self.offset = float(offset)
        self.current_param = float(current_param)
        self.max_acceleration = float(max_acceleration)

        # 2. Preparar target temporal y delegado DynamicSeek
        self.dummy_target = Kinematic(position=(0.0, 0.0), orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
        self._seek = DynamicSeek(character=self.character, target=self.dummy_target, max_acceleration=self.max_acceleration)
 
    def get_steering(self) -> SteeringOutput:
        """
        Descripción
            MÉTODO: Calcula y devuelve un SteeringOutput que mueve `character` hacia
            un punto adelantado sobre la `path` (chase-the-rabbit), delegando en DynamicSeek.

        Argumentos
            - Ninguno

        Retorno
            - SteeringOutput: salida con componente linear calculada por DynamicSeek y
              componente angular = 0.0 (por convención la orientación la gestiona otro behaviour).
        """
        # 1. Obtener el parámetro en la ruta más cercano a la posición actual (búsqueda con hint)
        try:
            param = self.path.get_param(self.character.position, self.current_param)
        except Exception:
            # 1.1 Si la ruta no responde, no generar steering (resultado neutro)
            return SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        # 2. Actualizar current_param para la siguiente invocación
        self.current_param = float(param)

        # 3. Avanzar a lo largo de la ruta usando offset para obtener el parámetro objetivo
        target_param = self.current_param + self.offset

        # 4. Obtener la posición objetivo en la ruta; manejar fallo defensivamente
        try:
            target_pos = self.path.get_position(target_param)
        except Exception:
            # 4.1 Si get_position falla, devolver steering neutro
            return SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        # 5. Normalizar la posición objetivo a (x, z)
        tx, tz = float(target_pos[0]), float(target_pos[1])

        # 6. Actualizar el dummy_target con la posición calculada y sincronizar parámetros del delegado
        self.dummy_target.position = (tx, tz)
        self._seek.target = self.dummy_target
        self._seek.max_acceleration = self.max_acceleration

        # 7. Delegar el cálculo al DynamicSeek y devolver el resultado
        return self._seek.get_steering()