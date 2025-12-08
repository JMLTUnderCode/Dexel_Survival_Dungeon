import pygame
from ui.ui_elements import UIButton, UIIconToggle, UISlider
from ui.audio_manager import AudioManager
from helper.asset_loader import load_ui_assets
from configs.package import CONF

class Menu:
    """
    Descripción
        CLASE: Gestiona la pantalla del menú principal, incluyendo renderizado,
        eventos y transiciones hacia el juego o configuraciones.

    Atributos
        - screen (pygame.Surface): Superficie principal de la ventana.
        - clock (pygame.time.Clock): Reloj para controlar FPS.
        - running (bool): Controla el bucle del menú.
        - buttons_assets (Dict): Imágenes de botones cargadas.
        - icons_assets (Dict): Imágenes de iconos cargadas.
        - ui_buttons (Dict[str, UIButton]): Instancias de botones interactivos.
        - sound_toggle (UIIconToggle): Instancia del toggle de sonido.
        - current_state (str): Estado actual del menú ("MAIN", "SETTINGS").

    Métodos y Funciones
        - run: Ejecuta el bucle del menú y retorna la acción seleccionada.
        - _init_ui: Inicializa posiciones y objetos de UI.
        - _draw: Renderiza la escena.
        - _handle_input: Procesa eventos.

    Propósito
        - Servir como punto de entrada visual y de configuración antes del juego.
    """
    def __init__(self) -> None:
        # 1. Inicializar Pygame y ventana
        pygame.init()
        display_info = pygame.display.Info()
        w = display_info.current_w - CONF.MAIN_WIN.SCREEN_OFF_SET
        h = display_info.current_h - CONF.MAIN_WIN.SCREEN_OFF_SET
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(CONF.MAIN_WIN.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "MAIN" # MAIN, SETTINGS

        # 2. Cargar recursos
        self.buttons_assets, self.icons_assets = load_ui_assets()
        
        # 3. Fuente para versión y Títulos
        self.font_version = pygame.font.SysFont("Segoe UI", 20)
        self.font_title = pygame.font.SysFont("Segoe UI", 48, bold=True) # Fuente grande
        self.font_label = pygame.font.SysFont("Segoe UI", 24) # Fuente etiquetas

        # 4. Inicializar Audio Manager (MOVER ANTES DE _init_ui para tener volumen inicial)
        self.audio_manager = AudioManager()
        self.audio_manager.play_music("menu_theme")

        # 5. Construir UI (Ahora tiene acceso a audio_manager)
        self._init_ui(w, h)

    def _init_ui(self, screen_w: int, screen_h: int) -> None:
        """
        Descripción
            MÉTODO: Crea las instancias de botones y las posiciona.

        Argumentos
            - screen_w (int) : Ancho de pantalla.
            - screen_h (int) : Alto de pantalla.
        """
        self.ui_buttons = {}
        center_x = screen_w // 2
        start_y = screen_h // 2 - 200 # Offset vertical para centrar el bloque
        spacing = 200 # Espacio entre botones

        # 1. Botones Principales (Play, Options, Exit)
        # Usamos claves del diccionario de assets (ver ui.py)
        if "play" in self.buttons_assets:
            self.ui_buttons["play"] = UIButton(self.buttons_assets["play"], (center_x, start_y))
        
        if "options" in self.buttons_assets:
            self.ui_buttons["options"] = UIButton(self.buttons_assets["options"], (center_x, start_y + spacing))
            
        if "exit" in self.buttons_assets:
            self.ui_buttons["exit"] = UIButton(self.buttons_assets["exit"], (center_x, start_y + spacing * 2))

        # 2. Botón de regreso (para submenú settings)
        if "back" in self.buttons_assets:
            # Posicionado abajo a la izquierda o centro
            self.ui_buttons["back"] = UIButton(self.buttons_assets["back"], (center_x, screen_h - 100))

        # 3. Icono de Sonido (Top Right)
        # Margen de 20px
        if "sound on" in self.icons_assets and "sound off" in self.icons_assets:
            self.sound_toggle = UIIconToggle(
                self.icons_assets["sound on"],
                self.icons_assets["sound off"],
                (screen_w - 20, 20)
            )
        
        # 4. Sliders de Configuración (Centrados)
        # SFX Slider
        self.slider_sfx = UISlider(
            center_pos=(center_x, screen_h // 2 - 50),
            width=400,
            initial_value=self.audio_manager.sfx_volume
        )
        
        # Music Slider
        self.slider_music = UISlider(
            center_pos=(center_x, screen_h // 2 + 50),
            width=400,
            initial_value=self.audio_manager.music_volume
        )

    def run(self) -> str:
        """
        Descripción
            MÉTODO: Bucle principal del menú.

        Retorno
            - str: Acción a ejecutar ("play", "exit").
        """
        action = "none"
        while self.running:
            self.clock.tick(CONF.MAIN_WIN.FPS)
            
            # 1. Input
            action = self._handle_input()
            if action != "none":
                return action

            # 2. Update (Hover logic)
            mx, my = pygame.mouse.get_pos()
            if self.current_state == "MAIN":
                for key in ["play", "options", "exit"]:
                    if key in self.ui_buttons:
                        self.ui_buttons[key].update((mx, my), self.audio_manager)
            elif self.current_state == "SETTINGS":
                if "back" in self.ui_buttons:
                    self.ui_buttons["back"].update((mx, my), self.audio_manager)

            # 3. Draw
            self._draw()

        return "exit"

    def _handle_input(self) -> str:
        """
        Descripción
            MÉTODO: Procesa eventos de Pygame.

        Retorno
            - str: Acción resultante o "none".
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "exit"

            # Toggle de sonido (siempre visible en MAIN)
            if hasattr(self, "sound_toggle"):
                if self.sound_toggle.handle_event(event):
                    # Efecto de click
                    self.audio_manager.play_sfx("click")
                    # Alternar mute en el manager
                    is_muted = self.audio_manager.toggle_mute()
                    # Actualizar estado visual del botón
                    self.sound_toggle.state = not is_muted 

            # Botones según estado
            if self.current_state == "MAIN":
                if "play" in self.ui_buttons and self.ui_buttons["play"].handle_event(event):
                    self.audio_manager.play_sfx("loading")
                    pygame.mixer.music.stop() # Detener música del menú antes de ir al juego
                    return "play"
                
                if "options" in self.ui_buttons and self.ui_buttons["options"].handle_event(event):
                    self.audio_manager.play_sfx("click")
                    self.current_state = "SETTINGS"
                
                if "exit" in self.ui_buttons and self.ui_buttons["exit"].handle_event(event):
                    self.audio_manager.play_sfx("click")
                    return "exit"

            elif self.current_state == "SETTINGS":
                # 1. Botón Back
                if "back" in self.ui_buttons and self.ui_buttons["back"].handle_event(event):
                    self.audio_manager.play_sfx("click")
                    self.current_state = "MAIN"
                
                # 2. Manejo de Sliders
                if self.slider_sfx.handle_event(event):
                    # Actualizar volumen SFX si cambió
                    self.audio_manager.set_sfx_volume(self.slider_sfx.get_value())
                    
                if self.slider_music.handle_event(event):
                    # Actualizar volumen Música si cambió
                    self.audio_manager.set_music_volume(self.slider_music.get_value())

        return "none"

    def _draw(self) -> None:
        """
        Descripción
            MÉTODO: Renderiza el fondo y los elementos de UI.
        """
        # 1. Fondo
        self.screen.fill(CONF.UI.BACKGROUND_COLOR)

        # 2. Elementos según estado
        if self.current_state == "MAIN":
            # Botones
            for key in ["play", "options", "exit"]:
                if key in self.ui_buttons:
                    self.ui_buttons[key].draw(self.screen)
            
            # Icono Sonido
            if hasattr(self, "sound_toggle"):
                self.sound_toggle.draw(self.screen)

            # Texto Versión (Bottom Right)
            ver_surf = self.font_version.render(f"v{CONF.UI.VERSION}", True, (150, 150, 150))
            ver_rect = ver_surf.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10))
            self.screen.blit(ver_surf, ver_rect)

        elif self.current_state == "SETTINGS":
            center_x = self.screen.get_width() // 2
            # Icono Sonido
            if hasattr(self, "sound_toggle"):
                self.sound_toggle.draw(self.screen)

            # 1. Título SETTINGS
            title = self.font_title.render("SETTINGS", True, (255, 255, 255))
            title_rect = title.get_rect(center=(center_x, 100))
            self.screen.blit(title, title_rect)
            
            # 2. Slider SFX
            # Etiqueta
            lbl_sfx = self.font_label.render(f"SFX Volume: {int(self.slider_sfx.get_value() * 100)}%", True, (200, 200, 200))
            lbl_sfx_rect = lbl_sfx.get_rect(center=(center_x, self.slider_sfx.rect.top - 20))
            self.screen.blit(lbl_sfx, lbl_sfx_rect)
            # Barra
            self.slider_sfx.draw(self.screen)
            
            # 3. Slider Music
            # Etiqueta
            lbl_mus = self.font_label.render(f"Music Volume: {int(self.slider_music.get_value() * 100)}%", True, (200, 200, 200))
            lbl_mus_rect = lbl_mus.get_rect(center=(center_x, self.slider_music.rect.top - 20))
            self.screen.blit(lbl_mus, lbl_mus_rect)
            # Barra
            self.slider_music.draw(self.screen)
            
            # 4. Botón Back
            if "back" in self.ui_buttons:
                self.ui_buttons["back"].draw(self.screen)

        pygame.display.flip()