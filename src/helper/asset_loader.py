import pygame
import os
from typing import Dict, Tuple
from configs.package import CONF
from utils.resource_path_dir import resource_path_dir

def load_ui_assets() -> Tuple[Dict[str, pygame.Surface], Dict[str, pygame.Surface]]:
    """
    Descripción
        FUNCIÓN: Carga y procesa las imágenes de botones e iconos para la UI.
        Escala las imágenes según las dimensiones especificadas en la configuración.

    Argumentos
        - Ninguno

    Retorno
        - Tuple[Dict, Dict]: Tupla conteniendo (diccionario_botones, diccionario_iconos).
    """
    # 1. Inicializar diccionarios
    buttons = {}
    icons = {}
    
    # 2. Definir ruta base de assets
    base_path = resource_path_dir("assets")
    ui_folder = CONF.UI.FOLDER_UI

    # 3. Cargar Botones
    for key, data in CONF.UI.BUTTONS.items():
        try:
            path = os.path.join(base_path, ui_folder, data["file"])
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Escalar a las dimensiones configuradas
                scaled = pygame.transform.smoothscale(img, (data["w"], data["h"]))
                buttons[key] = scaled
            else:
                print(f"[AssetLoader] Advertencia: No se encontró {path}")
        except Exception as e:
            print(f"[AssetLoader] Error cargando botón {key}: {e}")

    # 4. Cargar Iconos
    for key, data in CONF.UI.ICONS.items():
        try:
            path = os.path.join(base_path, ui_folder, data["file"])
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Escalar a las dimensiones configuradas
                scaled = pygame.transform.smoothscale(img, (data["w"], data["h"]))
                icons[key] = scaled
            else:
                print(f"[AssetLoader] Advertencia: No se encontró {path}")
        except Exception as e:
            print(f"[AssetLoader] Error cargando icono {key}: {e}")

    return buttons, icons

def load_sfx_assets() -> Dict[str, pygame.mixer.Sound]:
    """
    Descripción
        FUNCIÓN: Carga los archivos de efectos de sonido (.wav) en memoria.

    Argumentos
        - Ninguno

    Retorno
        - Dict[str, pygame.mixer.Sound]: Diccionario con objetos Sound listos para reproducir.
    """
    sfx_dict = {}
    
    # 1. Definir ruta base
    base_path = resource_path_dir("assets")
    audio_folder = CONF.AUDIO.FOLDER_AUDIO
    
    # 2. Inicializar mixer si no está listo (por seguridad)
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # 3. Cargar cada efecto definido en la configuración
    for key, filename in CONF.AUDIO.SFX.items():
        try:
            path = os.path.join(base_path, audio_folder, filename)
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(CONF.AUDIO.DEFAULT_SFX_VOLUME)
                sfx_dict[key] = sound
            else:
                print(f"[AssetLoader] Advertencia: No se encontró SFX {path}")
        except Exception as e:
            print(f"[AssetLoader] Error cargando SFX {key}: {e}")
            
    return sfx_dict