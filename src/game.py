import pygame
import sys
from map.map import Map
from ui.enemy_set import EnemySet
from ui.map_set import MapSet
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

        self.ui_panel_width = 0
        if CONF.ALG_UI.ACTIVE:
            self.ui_panel_width = CONF.ALG_UI.PANEL_WIDTH
        elif CONF.MAP_UI.ACTIVE:
            self.ui_panel_width = CONF.MAP_UI.PANEL_WIDTH

        self.camera_width = self.screen_width - self.ui_panel_width
        self.camera_height = self.screen_height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_surface = pygame.Surface((self.camera_width, self.camera_height))
        pygame.display.set_caption(CONF.MAIN_WIN.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.running = True

        # --- Gestor de Entidades y Estado del Juego ---
        self.game_map = Map(level=CONF.MAP_UI.SELECTED)
        self.entity_manager = EntityManager()
        
        # Crear entidades iniciales
        self.entity_manager.create_player()
        initial_group = None
        type_group = None
        if CONF.ALG_UI.ACTIVE: 
            initial_group = CONF.ALG_UI.SELECTED
            type_group = "alg"
        if CONF.MAP_UI.ACTIVE: 
            initial_group = CONF.MAP_UI.SELECTED
            type_group = "map"
        if initial_group and type_group:
            self.entity_manager.create_enemy_group(initial_group, type_group)
        
        self.camera_x = 0
        self.camera_z = 0

        # --- Inicializar UI si está activa ---
        self.enemy_set_ui = None
        self.map_set_ui = None
        if CONF.ALG_UI.ACTIVE:
            self.enemy_set_ui = EnemySet(self.entity_manager)
        if CONF.MAP_UI.ACTIVE:
            self.map_set_ui = MapSet(self, self.entity_manager)

    def load_level(self, level_number: int):
        """
        Carga un nivel específico, reconstruyendo el mapa, el navmesh y las entidades.
        """
        if CONF.DEV.DEBUG:
            print(f"[Game] Cargando nivel {level_number}...")
        
        # 1. Cargar el nuevo mapa
        self.game_map = Map(level=level_number)
        
        # 2. Recrear el pathfinder con el nuevo navmesh
        self.pathfinder = None
        if self.game_map.navmesh:
            pass
            #self.pathfinder = Pathfinder(self.game_map.navmesh)
        #self.entity_manager.pathfinder = self.pathfinder # Actualizar referencia en el manager

        # 3. Crear las entidades para el nuevo nivel
        self.entity_manager.create_player()
        self.entity_manager.create_enemy_group(level_number, "map")

    def _handle_events(self):
        """
        Procesa la cola de eventos de Pygame. Gestiona el cierre del juego
        y delega los eventos a los subsistemas correspondientes (UI, Jugador).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Delegar evento a las UIs
            ui_handled = False
            if self.enemy_set_ui:
                ui_handled = self.enemy_set_ui.handle_event(event)
            if not ui_handled and self.map_set_ui:
                ui_handled = self.map_set_ui.handle_event(event)

            # Si no fue manejado por la UI, pasarlo al jugador
            if not ui_handled:
                self._forward_event_to_player(event)

    def _forward_event_to_player(self, event: pygame.event.Event):
        """
        Envía un evento al jugador, ajustando las coordenadas del mouse si es necesario.
        Esta función actúa como un traductor entre las coordenadas de la pantalla
        y las coordenadas del área de juego.
        """
        if not self.entity_manager.player:
            return

        # Si el evento no tiene posición (ej. teclado), se pasa directamente.
        if not hasattr(event, "pos"):
            self.entity_manager.player.handle_event(event)
            return

        # Si el evento tiene posición (mouse), se ajusta.
        mouse_x, mouse_y = event.pos
        game_area_start_x = CONF.ALG_UI.PANEL_WIDTH if self.enemy_set_ui else 0

        # Solo si el evento ocurrió dentro del área de juego, se procesa.
        if mouse_x >= game_area_start_x:
            # Ajustar la coordenada X para que sea relativa al game_surface
            adjusted_x = mouse_x - game_area_start_x
            
            try:
                # Crear un nuevo evento con la posición ajustada
                adjusted_event = pygame.event.Event(event.type, {**event.__dict__, "pos": (adjusted_x, mouse_y)})
                self.entity_manager.player.handle_event(adjusted_event)
            except Exception:
                self.entity_manager.player.handle_event(event) # Fallback

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
        # Actualizar nodo del jugador usando BFS local en NavMesh (si existe)
        if self.game_map.navmesh:
            new_node = self.game_map.navmesh.find_node_from(player.node_location, player.get_pos())
            player.node_location = new_node

        for enemy in self.entity_manager.enemies:
            enemy.update(self.game_map.collision_rects, self.dt)
            if self.game_map.navmesh:
                # mantener id o nodo según convenga; aquí guardamos el NavMeshNode objeto
                enemy.node_location = self.game_map.navmesh.find_node_from(enemy.node_location, enemy.get_pos())

    def _render(self):
        """
        Dibuja todos los elementos del juego en la pantalla con un orden de renderizado fijo
        para garantizar que el jugador siempre sea visible.
        Orden: 1. Mapa -> 2. Enemigos -> 3. Jugador -> 4. UI
        """
        # 1. Limpiar la superficie del juego y dibujar el mapa
        self.game_surface.fill((30, 30, 30))
        self.game_map.draw(self.game_surface, self.camera_x, self.camera_z, self.camera_width, self.camera_height)

        # DEBUG: dibujar el nodo actual de cada entidad (solo bordes)
        if CONF.DEV.DEBUG and self.game_map.navmesh:
            for entity in self.entity_manager.enemies + [self.entity_manager.player]:
                node = getattr(entity, "node_location", None)
                if node and getattr(node, "polygon", None):
                    try:
                        pts = [(int(p[0] - self.camera_x), int(p[1] - self.camera_z)) for p in node.polygon]
                        if len(pts) >= 3:
                            pygame.draw.polygon(self.game_surface, (255, 0, 0), pts, 2)
                    except Exception:
                        pass

        # 2. Dibujar todos los enemigos
        for enemy in self.entity_manager.enemies:
            enemy.draw(self.game_surface, self.camera_x, self.camera_z)

        # 3. Dibujar al jugador (siempre al final, para que aparezca por encima de los enemigos)
        if self.entity_manager.player:
            self.entity_manager.player.draw(self.game_surface, self.camera_x, self.camera_z)

        # 4. Dibujar la superficie del juego en la pantalla principal
        self.screen.fill((0, 0, 0))
        blit_position = (self.ui_panel_width, 0)
        self.screen.blit(self.game_surface, blit_position)

        # 5. Dibujar la UI encima de todo
        if self.enemy_set_ui:
            self.enemy_set_ui.draw(self.screen)
        if self.map_set_ui:
            self.map_set_ui.draw(self.screen)

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