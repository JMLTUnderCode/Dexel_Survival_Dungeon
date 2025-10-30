import pygame
import sys
from map.map import Map
from ui.algorithms import *
from helper.entity_manager import EntityManager
from configs.package import CONF

class Game:
    """
    Clase principal que encapsula la lógica y el estado del juego.
    
    Gestiona la inicialización de Pygame, la ventana, el bucle principal del juego,
    el manejo de eventos, la actualización de entidades y el renderizado, siguiendo
    una arquitectura profesional de separación de responsabilidades.
    """
    def __init__(self):
        """
        Inicializa el juego, configurando Pygame, la ventana, el reloj y
        cargando todos los recursos iniciales como el mapa, jugador y enemigos.
        """
        # --- Inicialización de Pygame y Ventana ---
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w - CONF.MAIN_WIN.SCREEN_OFF_SET
        self.screen_height = display_info.current_h - CONF.MAIN_WIN.SCREEN_OFF_SET
        
        if CONF.DEV.DEBUG:
            print("\n ******** DEVELOPMENT MODE ACTIVE ******** ")
            print(f"[Game] Juego iniciado en resolución {self.screen_width}x{self.screen_height}.")

        self.camera_width = max(320, self.screen_width - CONF.ALG_UI.PANEL_WIDTH if CONF.ALG_UI.ACTIVE else self.screen_width)
        self.camera_height = max(240, self.screen_height)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_surface = pygame.Surface((self.camera_width, self.camera_height))
        pygame.display.set_caption(CONF.MAIN_WIN.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.running = True

        # --- Gestor de Entidades y Estado del Juego ---
        self.game_map = Map(level=1)
        self.entity_manager = EntityManager()
        
        # Crear entidades iniciales
        self.entity_manager.create_player()
        initial_group = CONF.ALG_UI.SELECTED_ALGORITHM if CONF.ALG_UI.ACTIVE else CONF.MAP.LEVELS[self.game_map.level]
        self.entity_manager.create_enemy_group(initial_group)
        
        self.camera_x = 0
        self.camera_z = 0

        # --- Inicializar UI si está activa ---
        if CONF.ALG_UI.ACTIVE:
            init_ui_fonts()
            build_ui_buttons(self.entity_manager)

    def _handle_events(self):
        """
        Procesa la cola de eventos de Pygame. Gestiona el cierre del juego
        y delega los eventos de input al jugador.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            changed = False
            if CONF.ALG_UI.ACTIVE:
                # La UI ahora modifica el entity_manager directamente
                changed = handle_ui_event(event)

            if not changed and self.entity_manager.player:
                self.entity_manager.player.handle_event(event)

    def _update(self):
        """
        Actualiza el estado de todas las entidades del juego y la cámara.
        Se llama una vez por frame, después de manejar eventos y antes de renderizar.
        """
        player = self.entity_manager.player
        if not player: return

        # 1. Manejar input y actualizar cámara
        player.handle_input(self.camera_x, self.camera_z, self.dt)
        px, pz = player.get_pos()
        self.camera_x = max(0, min(px - self.camera_width // 2, self.game_map.width - self.camera_width))
        self.camera_z = max(0, min(pz - self.camera_height // 2, self.game_map.height - self.camera_height))

        # 2. Actualizar la lógica de las entidades
        player.update(self.game_map.collision_rects, self.dt)
        for enemy in self.entity_manager.enemies:
            enemy.update(self.game_map.collision_rects, self.dt)

    def _render(self):
        """
        Dibuja todos los elementos del juego en la pantalla con un orden de renderizado fijo
        para garantizar que el jugador siempre sea visible.
        Orden: 1. Mapa -> 2. Enemigos -> 3. Jugador -> 4. UI
        """
        # 1. Limpiar la superficie del juego y dibujar el mapa
        self.game_surface.fill((30, 30, 30))
        self.game_map.draw(self.game_surface, self.camera_x, self.camera_z, self.camera_width, self.camera_height)
        
        # 2. Dibujar todos los enemigos
        for enemy in self.entity_manager.enemies:
            enemy.draw(self.game_surface, self.camera_x, self.camera_z)

        # 3. Dibujar al jugador (siempre al final, para que aparezca por encima de los enemigos)
        if self.entity_manager.player:
            self.entity_manager.player.draw(self.game_surface, self.camera_x, self.camera_z)

        # 4. Dibujar la superficie del juego en la pantalla principal
        self.screen.fill((0, 0, 0))
        blit_position = (CONF.ALG_UI.PANEL_WIDTH if CONF.ALG_UI.ACTIVE else 0, 0)
        self.screen.blit(self.game_surface, blit_position)

        # 5. Dibujar la UI encima de todo
        if CONF.ALG_UI.ACTIVE:
            draw_ui(self.screen, CONF.ALG_UI.PANEL_WIDTH, self.screen_height)

        # 6. Actualizar la pantalla para mostrar los cambios
        pygame.display.flip()

    def run(self):
        """
        Inicia y mantiene el bucle principal del juego.
        """
        while self.running:
            # Calcular delta time para un movimiento independiente de los FPS
            self.dt = self.clock.tick(CONF.MAIN_WIN.FPS) / 1000.0
            
            # Ciclo de juego estándar: Eventos -> Lógica -> Renderizado
            self._handle_events()
            self._update()
            self._render()
        
        # Salir del juego de forma limpia
        pygame.quit()
        sys.exit()