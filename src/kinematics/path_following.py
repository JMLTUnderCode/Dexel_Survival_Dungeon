from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.dynamic_seek import DynamicSeek
from utils.create_paths import Path

class FollowPath:
    """
    FollowPath (Chase-the-Rabbit) behaviour.

    Descripción
    - Este comportamiento calcula un único objetivo a lo largo de una `path`
      (ruta) usando el enfoque "chase the rabbit":
        1) Encuentra el parámetro `current_param` de la ruta más cercano a la posición
           actual del personaje (usando `path.get_param(position, hint)`).
        2) Avanza a lo largo de la ruta una distancia `path_offset` para obtener el
           parámetro objetivo `target_param`.
        3) Recupera la posición objetivo con `path.get_position(target_param)`.
        4) Delega la persecución de esa posición al `DynamicSeek` (seek dinámico).
    - Devuelve un `SteeringOutput` con la aceleración lineal calculada por `DynamicSeek`
      y componente angular 0 (la orientación la puede gestionar otro comportamiento,
      p. ej. `LookWhereYoureGoing` o `Face` si se desea).

    Notas sobre la interfaz `path`
    - Se asume que `path` implementa al menos:
        - `get_param(position: Tuple[float, float], hint: float) -> float`
          (devuelve el parámetro en la ruta más cercano a `position`. `hint` es un
           parámetro inicial/estimación para búsqueda eficiente).
        - `get_position(param: float) -> Tuple[float, float]`
          (devuelve la posición 2D correspondiente al parámetro `param`).
    - `path` puede representar rutas cerradas o abiertas. El manejo de límites/Wrap
      depende de la implementación de `path.get_param` / `get_position`.
    - `path_offset` puede ser negativo para moverse en sentido inverso.

    Parámetros (constructor)
    - character: instancia de Kinematic que sigue la ruta.
    - path: objeto que representa la ruta (ver la interfaz arriba).
    - path_offset: distancia a lo largo de la ruta desde el punto más cercano
                   para generar el objetivo (p. ej. 5.0 - 20.0 unidades).
    - current_param: parámetro inicial estimado en la ruta (se actualiza internamente).
    - max_acceleration: aceleración máxima pasada a DynamicSeek.
    """

    def __init__(
        self,
        character: Kinematic,
        path: Path,
        path_offset: float = 12.0,
        current_param: float = 0.0,
        max_acceleration: float = 300.0,
    ) -> None:
        self.character = character
        self.path = path
        self.path_offset = float(path_offset)
        # current_param se mantiene entre frames para búsquedas locales rápidas
        self.current_param = float(current_param)
        self.max_acceleration = float(max_acceleration)

        # Delegate seek: usaremos un target temporal Kinematic que reemplazamos
        # cada frame. DynamicSeek espera un Kinematic como target.
        self.dummy_target = Kinematic(position=(0.0, 0.0), orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
        self._seek = DynamicSeek(character=self.character, target=self.dummy_target, max_acceleration=self.max_acceleration)

    def get_steering(self) -> SteeringOutput:
        """
        Calcula y devuelve el SteeringOutput delegando en DynamicSeek.

        Flujo:
        1) current_param <- path.get_param(character.position, current_param)
        2) target_param <- current_param + path_offset
        3) target_pos <- path.get_position(target_param)
        4) crear explicit_target (Kinematic) con position = target_pos
        5) asignar self._seek.target = explicit_target y devolver self._seek.get_steering()
        """
        # 1) Encontrar el parámetro en la ruta más cercano a la posición actual
        try:
            param = self.path.get_param(self.character.position, self.current_param)
        except Exception as e:
            # Si la implementación de path no está disponible o falla, no generamos steering.
            # Caller puede interpretar SteeringOutput((0,0), 0) como "no change".
            # Loggear/elevar según políticas del proyecto.
            return SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        self.current_param = float(param)

        # 2) Avanzar por la ruta
        target_param = self.current_param + self.path_offset

        # 3) Obtener posición objetivo en la ruta
        try:
            target_pos = self.path.get_position(target_param)
        except Exception as e:
            # Fallback si get_position falla
            return SteeringOutput(linear=(0.0, 0.0), angular=0.0)

        # Asegurar formato de tupla (x, z)
        tx, tz = float(target_pos[0]), float(target_pos[1])

        # 4) Construir target temporal y delegar a DynamicSeek
        self.dummy_target.position = (tx, tz)
        self._seek.target = self.dummy_target
        self._seek.max_acceleration = self.max_acceleration

        # 5) Devolver el steering calculado por DynamicSeek
        return self._seek.get_steering()