import os
import pygame
from enum import Enum
from typing import List, Optional, Tuple
from utils.resource_path_dir import resource_path_dir

__all__ = ["Animation", "load_animations", "set_animation_state"]

class Animation:
    """
    Representa una animación extraída de un sprite sheet horizontal.

    Cada frame se corta desde la imagen proporcionada (image_path) con tamaño
    (frame_width, frame_height). Opcionalmente cada frame puede escalarse a
    `scale_to` (ancho, alto).

    Parámetros
    - image_path: ruta al sprite sheet (frames en una sola fila).
    - frame_width: ancho de cada frame en el sprite sheet original.
    - frame_height: alto de cada frame en el sprite sheet original.
    - frame_count: número de frames a extraer.
    - frame_duration: duración de cada frame en segundos.
    - scale_to: tupla opcional (width, height) para escalar cada frame.

    Métodos relevantes
    - update(dt): avanzar la animación en base a dt (segundos).
    - get_frame(): devuelve el Surface actual.
    - reset(): vuelve al primer frame.
    - __len__(): devuelve la cantidad de frames.

    Ejemplo:
        anim = Animation("enemy-move.png", 64, 64, 8, 0.12, scale_to=(48,48))
        anim.update(0.016)
        frame = anim.get_frame()
    """

    def __init__(
        self,
        image_path: str,
        frame_width: int,
        frame_height: int,
        frame_count: int,
        frame_duration: float,
        scale_to: Optional[Tuple[int, int]] = None,
    ) -> None:
        # Cargar sprite sheet y extraer frames
        self.sprite_sheet: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.frame_width: int = frame_width
        self.frame_height: int = frame_height
        self.frame_count: int = frame_count
        self.frame_duration: float = frame_duration  # segundos por frame
        self.frames: List[pygame.Surface] = []

        for i in range(frame_count):
            rect = (i * frame_width, 0, frame_width, frame_height)
            frame = self.sprite_sheet.subsurface(rect).copy()
            if scale_to:
                # Asegurar que scale_to es una tupla de dos enteros
                frame = pygame.transform.scale(frame, (int(scale_to[0]), int(scale_to[1])))
            self.frames.append(frame)

        if not self.frames:
            raise RuntimeError(f"No frames extracted from {image_path}")

        self.current_frame: int = 0
        self.time_acc: float = 0.0

    def update(self, dt: float) -> None:
        """
        Avanza la animación en base a dt (segundos).
        Llama a este método desde el bucle principal con el delta time.
        """
        if self.frame_count <= 1:
            return
        self.time_acc += dt
        if self.time_acc >= self.frame_duration:
            # soporta dt mayor que frame_duration (varios frames)
            steps = int(self.time_acc / self.frame_duration)
            self.time_acc -= steps * self.frame_duration
            self.current_frame = (self.current_frame + steps) % self.frame_count

    def get_frame(self) -> pygame.Surface:
        """Devuelve el Surface del frame actual."""
        return self.frames[self.current_frame]

    def reset(self) -> None:
        """Vuelve al primer frame y resetea el acumulador de tiempo."""
        self.current_frame = 0
        self.time_acc = 0.0

    def get_size(self) -> Tuple[int, int]:
        """Devuelve (width, height) del frame actual."""
        frame = self.get_frame()
        return frame.get_width(), frame.get_height()

    def __len__(self) -> int:
        """Cantidad de frames en la animación."""
        return self.frame_count

def load_animations(dir: str, type: str, states_anims: type[Enum], w_tile: int, h_tile: int, frame_duration: float, scale: float) -> dict[str, Animation]:
    """
    Carga las animaciones para un personaje (enemigo o jugador) dado su tipo y estados.
    Retorna un diccionario con las animaciones cargadas.
    Cada animación se espera que esté en un archivo con el formato:
    '{type}-{state}.png' dentro de 'assets/{dir}/'.
    Ejemplo: 'assets/enemies/goblin/goblin-move.png'

    Parámetros:
    - dir: carpeta base ('enemies' o 'player').
    - type: tipo de personaje (ej. 'goblin', 'orc', 'knight').
    - states_anims: Enum con los estados y nombres de las animaciones.
    - w_tile, h_tile: tamaño de cada frame en el sprite sheet original.
    - frame_duration: duración de cada frame en segundos.
    - scale: factor de escala para redimensionar cada frame.
    """
    base = os.path.join("assets", dir)
    anims = {}
    scale_to = (int(w_tile * scale), int(h_tile * scale))
    for state in states_anims:
        state_value = state.value
        filename = f"{type}-{state_value}.png"
        path = resource_path_dir(os.path.join(base, filename))
        if os.path.exists(path):
            img = pygame.image.load(path)
            frame_count = img.get_width() // w_tile
            anims[state_value] = Animation(path, w_tile, h_tile, frame_count, frame_duration, scale_to=scale_to)
        else:
            raise RuntimeError(f"No se encontró la animación '{state}' para '{type}'. Verifica que exista el archivo '{path}'.")
    return anims

def set_animation_state(character, state: str):
    """
    Cambia la animación actual del personaje al estado dado.
    Resetea la animación si el estado cambia.
    
    Parámetros:
    - character: objeto que tiene atributos 'state', 'animations' (dict) y 'current_animation'.
    - state: nuevo estado (clave en character.animations).
    """
    if state != character.state and state in character.animations:
        character.state = state
        character.current_animation = character.animations[state]
        character.current_animation.current_frame = 0
        character.current_animation.time_acc = 0
    if state not in character.animations:
        raise RuntimeError(f"No se encontró la animación '{state}' para '{character.type}'.")