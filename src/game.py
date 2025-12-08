import sys
import pygame
from typing import Optional
from map.map import Map
from map.pathfinder import Pathfinder
from map.tactical_pathfinder import TacticalPathfinder
from ui.enemy_set import EnemySet
from ui.map_set import MapSet
from ui.audio_manager import AudioManager
from entity.entity_manager import EntityManager
import helper.debugging  as DEBUG
from configs.package import CONF

class Game:
    """
    Descripción
        CLASE: Clase principal que encapsula la lógica y el estado del juego.

    Atributos
        - screen_width (int): ancho de la ventana en píxeles.
        - screen_height (int): alto de la ventana en píxeles.
        - ui_panel_width (int): ancho del panel de UI activo (si aplica).
        - camera_width (int): ancho del área de juego (sin UI).
        - camera_height (int): alto del área de juego.
        - screen (pygame.Surface): superficie principal de la ventana.
        - game_surface (pygame.Surface): superficie donde se dibuja el mundo (viewport).
        - clock (pygame.time.Clock): reloj de Pygame para control de FPS.
        - dt (float): delta time del frame actual en segundos.
        - running (bool): indicador de ejecución del bucle principal.
        - game_map (Optional[Map]): mapa cargado actualmente.
        - pathfinder (Optional[Pathfinder]): pathfinder construido sobre el navmesh del mapa.
        - entity_manager (EntityManager): gestor de entidades (jugador, enemigos).
        - enemy_set_ui (Optional[EnemySet]): UI de selección de enemigos.
        - map_set_ui (Optional[MapSet]): UI de selección de mapas.
        - camera_x (int): coordenada X de la cámara (esquina superior izquierda).
        - camera_z (int): coordenada Z de la cámara (esquina superior izquierda).
        - audio_manager (AudioManager): gestor de audio para música y efectos.

    Métodos y Funciones
        - load_level: Carga y prepara un nivel completo (mapa, navmesh, entidades).
        - _handle_events: Procesa la cola de eventos de Pygame y delega a subsistemas.
        - _forward_event_to_player: Traduce eventos con posición y los entrega al jugador.
        - _update: Actualiza la lógica del juego (jugador, enemigos, cámara).
        - _render: Renderiza el mapa, entidades y UI en pantalla.
        - run: Bucle principal del juego.
    
    Propósito
        - Orquestar inicialización, ciclo de vida, actualización y renderizado del juego.
    """
    def __init__(self) -> None:
        # 1. Inicializar Pygame y calcular resolución disponible
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w - CONF.MAIN_WIN.SCREEN_OFF_SET
        self.screen_height = display_info.current_h - CONF.MAIN_WIN.SCREEN_OFF_SET

        # 2. Depuración: imprimir información inicial si está activo
        if CONF.DEV.DEBUG:
            print("\n ******** DEVELOPMENT MODE ACTIVE ******** ")
            print(f"[Game] Juego iniciado en resolución {self.screen_width}x{self.screen_height}.")

        # 3. Determinar ancho del panel UI activo
        self.ui_panel_width = 0
        if CONF.ALG_UI.ACTIVE:
            self.ui_panel_width = CONF.ALG_UI.PANEL_WIDTH
        elif CONF.MAP_UI.ACTIVE:
            self.ui_panel_width = CONF.MAP_UI.PANEL_WIDTH

        # 4. Calcular dimensiones del viewport y crear superficies
        self.camera_width = self.screen_width - self.ui_panel_width
        self.camera_height = self.screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_surface = pygame.Surface((self.camera_width, self.camera_height))
        pygame.display.set_caption(CONF.MAIN_WIN.GAME_TITLE)

        # 5. Inicializar reloj, variables de tiempo y control del bucle
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.running = True
        
        # 6. Inicializar Audio (o recibirlo como argumento si quieres persistencia)
        self.audio_manager = AudioManager()
        self.audio_manager.play_music("game_theme")
        
        # 7. Inicializar mapa, pathfinder y gestor de entidades
        self.game_map: Optional[Map] = None
        self.pathfinder: Optional[Pathfinder] = None
        self.entity_manager = EntityManager(audio_manager=self.audio_manager)

        # 8. Preparar clave/grupo para creación de entidades según UI activa
        self.level = CONF.MAP_UI.SELECTED
        self.group_key = CONF.MAP_UI.SELECTED
        self.group_type = "map"
        if CONF.ALG_UI.ACTIVE:
            self.group_key = CONF.ALG_UI.SELECTED
            self.group_type = "alg"
        if CONF.MAP_UI.ACTIVE:
            self.group_key = CONF.MAP_UI.SELECTED
            self.group_type = "map"
        self.load_level(level_number=self.level, g_key=self.group_key, g_type=self.group_type)

        # 9. Posición inicial de la cámara
        self.camera_x = 0
        self.camera_z = 0

        # 10. Inicializar componentes de UI si están activos
        self.enemy_set_ui: Optional[EnemySet] = None
        self.map_set_ui: Optional[MapSet] = None
        if CONF.ALG_UI.ACTIVE:
            self.enemy_set_ui = EnemySet(self.entity_manager)
        if CONF.MAP_UI.ACTIVE:
            self.map_set_ui = MapSet(self, self.entity_manager)

    def load_level(self, level_number: int, g_key: int, g_type: str) -> None:
        """
        Descripción
            MÉTODO: Carga un nivel específico, reconstruyendo el mapa, el navmesh y las entidades.
        
        Argumentos
            - level_number (int) : Índice del nivel en la configuración.
            - g_key (int) : Clave del grupo de enemigos a instanciar.
            - g_type (str) : Tipo de grupo ("map" o "alg").
        """
        # 1. Depuración: mensajes de carga
        if CONF.DEV.DEBUG:
            print(f"[Game] Cargando nivel {level_number}...")

        # 2. Cargar el mapa y calcular dimensiones
        self.game_map = Map(level=level_number)

        # 3. Construir pathfinder si el mapa tiene navmesh
        self.pathfinder = None
        self.tactical_pathfinder = None
        if self.game_map.navmesh:
            self.pathfinder = Pathfinder(self.game_map.navmesh)
            self.tactical_pathfinder = TacticalPathfinder(self.game_map.navmesh)

        # 4. Exponer el pathfinder al EntityManager para peticiones de ruta
        self.entity_manager.pathfinder = self.pathfinder
        self.entity_manager.tactical_pathfinder = self.tactical_pathfinder

        # 5. Crear jugador y grupo de enemigos para el nivel
        self.entity_manager.create_player()
        self.entity_manager.create_enemy_group(g_key, g_type)

    def _handle_events(self) -> None:
        """
        Descripción
            MÉTODO: Procesa la cola de eventos de Pygame y delega el manejo a UI y jugador.
        
        Argumentos
            - Ninguno
        """
        # 1. Iterar la cola de eventos
        for event in pygame.event.get():
            # 1.1 Manejo de cierre de ventana
            if event.type == pygame.QUIT:
                self.running = False
                return

            # 2. Intentar que la UI maneje el evento (primer nivel)
            ui_handled = False
            if self.enemy_set_ui:
                ui_handled = self.enemy_set_ui.handle_event(event)
            if not ui_handled and self.map_set_ui:
                ui_handled = self.map_set_ui.handle_event(event)

            # 3. Si la UI no lo manejó, procesar eventos con posición para el juego
            if not ui_handled and hasattr(event, "pos"):

                # 3.1 Herramientas de debug: actualizar rutas si se clickea en el world area
                if CONF.DEV.DEBUG:
                    DEBUG.update_enemy_paths_to(self.entity_manager, event, self.ui_panel_width, self.camera_x, self.camera_z)

                # 3.2 Reenviar evento al jugador (con ajuste de coordenadas)
                self._forward_event_to_player(event)

            # 4. Si evento no tiene posición y la UI no lo manejó, reenviar igualmente
            elif not ui_handled:
                self._forward_event_to_player(event)

    def _forward_event_to_player(self, event: pygame.event.Event) -> None:
        """
        Descripción
            MÉTODO: Envía un evento al jugador, ajustando las coordenadas del mouse si es necesario.
        
        Argumentos
            - event (pygame.event.Event) : Evento recibido desde Pygame.
        """
        # 1. No hacer nada si no hay jugador creado
        if not self.entity_manager.player:
            return

        # 2. Si el evento no tiene posición (teclado u otros), pasarlo directamente
        if not hasattr(event, "pos"):
            self.entity_manager.player.handle_event(event)
            return

        # 3. Ajustar la posición del mouse para que sea relativa al área de juego
        mouse_x, mouse_y = event.pos
        game_area_start_x = CONF.ALG_UI.PANEL_WIDTH if self.enemy_set_ui else 0

        # 4. Solo procesar si el click ocurrió dentro del área de juego
        if mouse_x >= game_area_start_x:
            adjusted_x = mouse_x - game_area_start_x
            try:
                # 4.1 Crear un nuevo evento con la posición ajustada y enviarlo al jugador
                adjusted_event = pygame.event.Event(event.type, {**event.__dict__, "pos": (adjusted_x, mouse_y)})
                self.entity_manager.player.handle_event(adjusted_event)
            except Exception:
                # 4.2 Fallback: enviar el evento original si la reconstrucción falla
                self.entity_manager.player.handle_event(event)

    def _update(self) -> None:
        """
        Descripción
            MÉTODO: Actualiza el estado de todas las entidades del juego y la cámara.
        
        Argumentos
            - Ninguno
        """
        # 1. Obtener referencia al jugador y salir si no existe
        player = self.entity_manager.player
        if not player:
            return

        # 2. Manejar input del jugador y centrar la cámara en su posición
        player.handle_input(self.camera_x, self.camera_z, self.dt)
        px, pz = player.get_pos()
        self.camera_x = max(0, min(px - self.camera_width // 2, self.game_map.width - self.camera_width))
        self.camera_z = max(0, min(pz - self.camera_height // 2, self.game_map.height - self.camera_height))

        # 3. Actualizar jugador y enemigos (fisica y animaciones)
        player.update(self.game_map.collision_rects, self.dt)

        # 4. Actualizar el estado del EntityManager (procesar ataques, resolver daños, limpiar)
        try:
            self.entity_manager.update(self.dt)
        except Exception:
            pass

        # 5. Actualizar nodo de navmesh para el jugador (si existe navmesh)
        if self.game_map.navmesh:
            new_node = self.game_map.navmesh.find_node_from(player.node_location, player.get_pos())
            player.node_location = new_node

        # 6. Actualizar enemigos y su nodo navmesh
        for enemy in self.entity_manager.enemies:
            enemy.update(self.game_map.collision_rects, self.dt)
            if self.game_map.navmesh:
                enemy.node_location = self.game_map.navmesh.find_node_from(enemy.node_location, enemy.get_pos())

    def _render(self) -> None:
        """
        Descripción
            MÉTODO: Dibuja todos los elementos del juego en la pantalla con un orden fijo.
        
        Argumentos
            - Ninguno
        """
        # 1. Limpiar la superficie del juego y dibujar el mapa
        self.game_surface.fill((30, 30, 30))
        if self.game_map:
            self.game_map.draw(self.game_surface, self.camera_x, self.camera_z, self.camera_width, self.camera_height)

        # 2. DEBUGS
        if CONF.DEV.DEBUG:
            # 2.1 Dibujar localización de nodos si está activo
            DEBUG.draw_node_location(self.game_surface, self.game_map, self.entity_manager, self.camera_x, self.camera_z)
            
            # 2.2 Dibujar nodos tácticos si está activo
            DEBUG.draw_tactical_nodes(self.game_surface, self.game_map, self.entity_manager, self.camera_x, self.camera_z)

        # 3. Dibujar enemigos
        for enemy in self.entity_manager.enemies:
            enemy.draw(self.game_surface, self.camera_x, self.camera_z)

        # 4. Dibujar jugador al final para mantener por encima
        if self.entity_manager.player:
            self.entity_manager.player.draw(self.game_surface, self.camera_x, self.camera_z)

        # 5. Dibujar textos flotantes de daño (UI de Mundo)
        self.entity_manager.draw_floating_texts(self.game_surface, self.camera_x, self.camera_z)

        # 6. Blit del game_surface en la pantalla principal (ajustando posición por panel UI)
        self.screen.fill((0, 0, 0))
        blit_position = (self.ui_panel_width, 0)
        self.screen.blit(self.game_surface, blit_position)

        # 7. Dibujar UI si está presente
        if self.enemy_set_ui:
            self.enemy_set_ui.draw(self.screen)
        if self.map_set_ui:
            self.map_set_ui.draw(self.screen)

        # 8. Actualizar la pantalla
        pygame.display.flip()

    def run(self) -> None:
        """
        Descripción
            MÉTODO: Inicia y mantiene el bucle principal del juego.
        
        Argumentos
            - Ninguno
        """
        # 1. Bucle principal: calcular dt, manejar eventos, actualizar y renderizar
        while self.running:
            self.dt = self.clock.tick(CONF.MAIN_WIN.FPS) / 1000.0
            self._handle_events()
            self._update()
            self._render()

        # 2. Salida limpia de Pygame y del proceso
        pygame.quit()
        sys.exit()