import pygame
import os
import random
from typing import Dict, Optional
from configs.package import CONF
from helper.asset_loader import load_sfx_assets
from utils.resource_path_dir import resource_path_dir

class AudioManager:
    """
    Descripción
        CLASE: Singleton (o gestor único) encargado de controlar la música y los efectos de sonido.

    Atributos
        - sfx_library (Dict[str, pygame.mixer.Sound]): Biblioteca de sonidos cargados.
        - music_volume (float): Volumen actual de la música.
        - sfx_volume (float): Volumen actual de los efectos.
        - is_muted (bool): Estado global de silencio.

    Métodos y Funciones
        - play_music: Inicia la reproducción de una pista de música en bucle.
        - play_sfx: Reproduce un efecto de sonido una vez (o en bucle).
        - play_random_sfx: Reproduce una variante aleatoria de un sonido base.
        - stop_sfx: Detiene un efecto de sonido específico.
        - toggle_mute: Alterna el silencio global.

    Propósito
        - Abstraer la complejidad de pygame.mixer del resto del juego.
    """
    def __init__(self) -> None:
        # 1. Inicializar mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # 2. Cargar efectos
        self.sfx_library = load_sfx_assets()
        
        # 3. Configuración inicial
        self.music_volume = CONF.AUDIO.DEFAULT_MUSIC_VOLUME
        self.sfx_volume = CONF.AUDIO.DEFAULT_SFX_VOLUME
        self.is_muted = False
        
        # 4. Aplicar volumen inicial a la música
        pygame.mixer.music.set_volume(self.music_volume)

    def play_music(self, track_key: str) -> None:
        """
        Descripción
            MÉTODO: Carga y reproduce una canción en bucle infinito.

        Argumentos
            - track_key (str): Clave de la canción en CONF.AUDIO.MUSIC.
        """
        if track_key not in CONF.AUDIO.MUSIC:
            print(f"[AudioManager] Música '{track_key}' no encontrada.")
            return

        try:
            # 1. Construir ruta
            filename = CONF.AUDIO.MUSIC[track_key]
            path = os.path.join(resource_path_dir("assets"), CONF.AUDIO.FOLDER_AUDIO, filename)
            
            # 2. Cargar y reproducir (-1 = loop infinito)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[AudioManager] Error reproduciendo música: {e}")

    def play_sfx(self, sfx_key: str, loops: int = 0) -> None:
        """
        Descripción
            MÉTODO: Reproduce un efecto de sonido.

        Argumentos
            - sfx_key (str): Clave del efecto en CONF.AUDIO.SFX.
            - loops (int): Número de repeticiones (-1 para infinito).
        """
        if self.is_muted:
            return

        if sfx_key in self.sfx_library:
            # 1. Reproducir sonido (loops=0 es una vez, loops=-1 es infinito)
            self.sfx_library[sfx_key].play(loops=loops)

    def play_random_sfx(self, base_name: str, count: int) -> None:
        """
        Descripción
            MÉTODO: Selecciona aleatoriamente un sonido de una serie (ej. "mele 1" a "mele 5")
            y lo reproduce.

        Argumentos
            - base_name (str): Prefijo del nombre del sonido (ej. "mele").
            - count (int): Cantidad total de variantes disponibles.
        """
        if self.is_muted:
            return

        # 1. Generar índice aleatorio entre 1 y count
        idx = random.randint(1, count)
        key = f"{base_name} {idx}"
        
        # 2. Reproducir
        self.play_sfx(key)

    def stop_sfx(self, sfx_key: str) -> None:
        """
        Descripción
            MÉTODO: Detiene la reproducción de un efecto de sonido específico.

        Argumentos
            - sfx_key (str): Clave del efecto en CONF.AUDIO.SFX.
        """
        if sfx_key in self.sfx_library:
            self.sfx_library[sfx_key].stop()

    def toggle_mute(self) -> bool:
        """
        Descripción
            MÉTODO: Alterna entre silencio y volumen normal.

        Retorno
            - bool: Nuevo estado de is_muted.
        """
        self.is_muted = not self.is_muted
        
        if self.is_muted:
            pygame.mixer.music.set_volume(0.0)
            # Detener todos los canales de SFX activos
            pygame.mixer.stop()
        else:
            pygame.mixer.music.set_volume(self.music_volume)
            
        return self.is_muted

    def set_music_volume(self, volume: float) -> None:
        """
        Descripción
            MÉTODO: Ajusta el volumen de la música en tiempo real.

        Argumentos
            - volume (float): Valor entre 0.0 y 1.0.
        """
        # 1. Actualizar atributo y mixer
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.is_muted:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """
        Descripción
            MÉTODO: Ajusta el volumen global para los efectos de sonido.
            Nota: Afecta a los sonidos que se reproduzcan a partir de ahora.

        Argumentos
            - volume (float): Valor entre 0.0 y 1.0.
        """
        # 1. Actualizar atributo
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        # 2. Actualizar volumen base de la librería cargada
        # Esto asegura que play_sfx use el nuevo volumen sin lógica extra
        for sound in self.sfx_library.values():
            sound.set_volume(self.sfx_volume)