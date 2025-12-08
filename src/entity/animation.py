import os
import pygame
from enum import Enum
from typing import List, Optional, Tuple, Type, Dict
from utils.resource_path_dir import resource_path_dir

__all__ = ["Animation", "load_animations", "set_animation_state", "load_attack_effects"]

class Animation:
    """
    Descripción
        CLASE: Representa una animación extraída de un sprite sheet horizontal.
    
    Atributos
        - sprite_sheet (pygame.Surface): imagen fuente con todos los frames.
        - frame_width (int): ancho de cada frame en la hoja original.
        - frame_height (int): alto de cada frame en la hoja original.
        - frame_count (int): número de frames en la animación.
        - frame_duration (float): duración de cada frame en segundos.
        - frames (List[pygame.Surface]): lista de frames extraídos.
        - current_frame (int): índice del frame actual.
        - time_acc (float): acumulador de tiempo para avanzar frames.
        - loop (bool): indica si la animación debe repetirse al finalizar.
        - finished (bool): indica si la animación ha terminado (solo si loop=False).
    
    Métodos y Funciones
        - update(dt): avanza la animación según delta time.
        - get_frame(): devuelve el Surface del frame actual.
        - reset(): resetea la animación al primer frame.
        - get_size(): devuelve (width, height) del frame actual.
        - is_finished: propiedad que indica si la animación finalizó.
    
    Propósito
        - Proveer una forma simple de gestionar animaciones basadas en sprite sheets
          horizontales y exponer la superficie actual para renderizado.
    """
    def __init__(
        self,
        image_path: str,
        frame_width: int,
        frame_height: int,
        frame_count: int,
        frame_duration: float,
        scale_to: Optional[Tuple[int, int]] = None,
        loop: bool = True,
    ) -> None:
        # 1. Cargar la imagen y almacenar parámetros básicos
        self.sprite_sheet: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.frame_width: int = int(frame_width)
        self.frame_height: int = int(frame_height)
        self.frame_count: int = int(frame_count)
        self.frame_duration: float = float(frame_duration)
        self.frames: List[pygame.Surface] = []
        self.loop: bool = loop
        self.finished: bool = False

        # 2. Extraer cada frame desde la fila horizontal del sprite sheet
        for i in range(self.frame_count):
            rect = (i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame = self.sprite_sheet.subsurface(rect).copy()
            if scale_to:
                # 2.1 Escalar el frame si se pidió un tamaño objetivo
                frame = pygame.transform.scale(frame, (int(scale_to[0]), int(scale_to[1])))
            self.frames.append(frame)

        # 3. Validación: asegurar que se hayan extraído frames
        if not self.frames:
            raise RuntimeError(f"No frames extracted from {image_path}")

        # 4. Inicializar estado de reproducción
        self.current_frame: int = 0
        self.time_acc: float = 0.0

    def update(self, dt: float) -> None:
        """
        Descripción
            MÉTODO: Avanza la animación en base a dt (segundos).
        
        Argumentos
            - dt (float): delta time en segundos desde la última actualización.
        """
        # 1. No avanzar si ya terminó (y no es loop) o si solo hay un frame
        if self.finished or self.frame_count <= 1:
            return

        # 2. Acumular tiempo y calcular cuantos frames avanzar si corresponde
        self.time_acc += float(dt)
        if self.time_acc >= self.frame_duration:
            steps = int(self.time_acc / self.frame_duration)
            self.time_acc -= steps * self.frame_duration
            
            if self.loop:
                self.current_frame = (self.current_frame + steps) % self.frame_count
            else:
                # Lógica para animaciones one-shot
                self.current_frame += steps
                if self.current_frame >= self.frame_count:
                    self.current_frame = self.frame_count - 1
                    self.finished = True

    def get_frame(self) -> pygame.Surface:
        """
        Descripción
            FUNCIÓN: Devuelve el Surface del frame actual.
        
        Argumentos
            - Ninguno

        Retorno
            - pygame.Surface: surface correspondiente al frame actual.
        """
        return self.frames[self.current_frame]

    def reset(self) -> None:
        """
        Descripción
            MÉTODO: Resetea la animación al primer frame y limpia el acumulador.

        Argumentos
            - Ninguno
        """
        self.current_frame = 0
        self.time_acc = 0.0
        self.finished = False

    @property
    def is_finished(self) -> bool:
        """
        Descripción
            PROPIEDAD: Indica si la animación ha terminado (útil para one-shot).
        """
        return self.finished

    def get_size(self) -> Tuple[int, int]:
        """
        Descripción
            FUNCIÓN: Devuelve el tamaño (width, height) del frame actual.

        Argumentos
            - Ninguno

        Retorno
            - Tuple[int, int]: (width, height) del frame actual.
        """
        frame = self.get_frame()
        return frame.get_width(), frame.get_height()

    def __len__(self) -> int:
        """
        Descripción
            FUNCIÓN: Devuelve la cantidad de frames en la animación.

        Argumentos
            - Ninguno

        Retorno
            - int: número de frames.
        """
        return self.frame_count

def load_animations(
    dir: str,
    type: str,
    states_anims: Type[Enum],
    w_tile: int,
    h_tile: int,
    frame_duration: float,
    scale: float,
) -> Dict[str, Animation]:
    """
    Descripción
        FUNCIÓN: Carga las animaciones para un personaje dado su tipo y estados.

    Argumentos
        - dir (str): carpeta base dentro de assets ('enemies' o 'player').
        - type (str): tipo de personaje (ej. 'goblin', 'berserker').
        - states_anims (Type[Enum]): Enum que contiene los estados/keys de animación.
        - w_tile (int): ancho de cada frame en el sprite sheet original.
        - h_tile (int): alto de cada frame en el sprite sheet original.
        - frame_duration (float): duración de cada frame en segundos.
        - scale (float): factor de escala para redimensionar cada frame.

    Retorno
        - Dict[str, Animation]: diccionario map state_name -> Animation.
    """
    # 1. Construir ruta base y mapa de animaciones vacío
    base = os.path.join("assets", dir)
    anims: Dict[str, Animation] = {}
    scale_to = (int(w_tile * scale), int(h_tile * scale))

    # 2. Iterar sobre cada estado definido en el Enum de estados
    for state in states_anims:
        state_value = state.value
        filename = f"{type}-{state_value}.png"
        path = resource_path_dir(os.path.join(base, filename))

        # 3. Si existe el archivo, cargar y construir la Animation; si no, fallar explícitamente
        if os.path.exists(path):
            img = pygame.image.load(path)
            frame_count = max(1, img.get_width() // w_tile)
            anims[state_value] = Animation(path, w_tile, h_tile, frame_count, frame_duration, scale_to=scale_to)
        else:
            raise RuntimeError(f"No se encontró la animación '{state_value}' para '{type}'. Verifica que exista el archivo '{path}'.")

    # 4. Devolver el diccionario de animaciones cargadas
    return anims

def load_effects(entity, dir: str, effects: dict, scale: float) -> Dict[str, Animation]:
    """
    Descripción
        FUNCIÓN: Carga las animaciones de efectos de ataque para un personaje.

    Argumentos
        - entity (Any): objeto que tiene atributos 'type' (str).
        - dir (str): carpeta base dentro de assets ('attacks').
        - effects (dict): configuración de efectos con metadatos.
        - scale (float): factor de escala para redimensionar cada frame.

    Retorno
        - Dict[str, Animation]: diccionario map effect_name -> Animation.
    """
    # 1. Construir ruta base y mapa de efectos vacío
    base = os.path.join("assets", dir)
    loaded_effects: Dict[str, Animation] = {}

    # 2. Iterar sobre cada efecto definido en la configuración
    for effect_name, effect_data in effects.items():
        filename = effect_data["file"]
        path = resource_path_dir(os.path.join(base, filename))

        # 3. Si existe el archivo, cargar y construir la Animation; si no, fallar explícitamente
        if os.path.exists(path):
            w_tile = effect_data["w"]
            h_tile = effect_data["h"]
            frame_count = effect_data["frames"]
            scale_to = (int(w_tile * scale), int(h_tile * scale))
            duration = None
            loop=False
            if effect_name == "magic":
                duration = entity.magic_cooldown/frame_count
            elif effect_name == "mele":
                duration = entity.mele_cooldown/frame_count
            elif effect_name == "invocation":
                time_for_invocation = entity.behavior.spec['params']["time_for_invocation"] if "time_for_invocation" in entity.behavior.spec['params'] else 6.0
                allies_for_invocation = entity.behavior.spec['params']["allies_for_invocation"] if "allies_for_invocation" in entity.behavior.spec['params'] else 1
                duration = time_for_invocation / allies_for_invocation / frame_count
                scale_to = (int(w_tile * scale * 1.5), int(h_tile * scale * 1.5))
                loop = True
            elif effect_name == "healing":
                duration = 1.0 / frame_count
                loop = True

            loaded_effects[effect_name] = Animation(
                image_path=path,
                frame_width=w_tile,
                frame_height=h_tile,
                frame_count=frame_count,
                frame_duration=duration,
                scale_to=scale_to,
                loop=loop
            )
        else:
            raise RuntimeError(f"No se encontró el efecto '{effect_name}' para '{entity.type}'. Verifica que exista el archivo '{path}'.")

    # 4. Devolver el diccionario de efectos cargados
    return loaded_effects

def set_animation_state(character, state: str) -> None:
    """
    Descripción
        FUNCIÓN: Cambia la animación actual del personaje al estado dado. Resetea
                 la animación si el estado cambia.

    Argumentos
        - character (Any): objeto que tiene atributos 'state', 'animations' (dict) y 'current_animation'.
        - state (str): nuevo estado (clave en character.animations).
    """
    # 1. Validar que el estado exista en las animaciones del personaje
    if state not in getattr(character, "animations", {}):
        raise RuntimeError(f"No se encontró la animación '{state}' para '{getattr(character, 'type', 'unknown')}'.")

    # 2. Si el estado cambió, asignar y resetear la animación asociada
    if state != getattr(character, "state", None):
        character.state = state
        character.current_animation = character.animations[state]
        
        # 2.1 Resetear completamente la animación (incluyendo flag finished)
        # IMPORTANTE: Usar .reset() para asegurar que animaciones one-shot (loop=False)
        # puedan volver a reproducirse limpiando la bandera 'finished'.
        character.current_animation.reset()