import os
import pygame
from pytmx.util_pygame import load_pygame
from utils.resource_path_dir import resource_path_dir
from .navmesh import NavMesh
from configs.package import CONF

class Map:
    """
    Clase que representa el mapa del juego cargado desde un archivo TMX.
    * Atributos:
        * level: nivel actual del mapa
        * tmx_data: datos del mapa cargados con pytmx
        * width: ancho del mapa en píxeles (ya escalado)
        * height: alto del mapa en píxeles (ya escalado)
        * collision_rects: lista de pygame.Rect que representan las áreas de colisión
        * navmesh: instancia de NavMesh para pathfinding
    * Métodos:
        * load(level): carga el mapa TMX y procesa colisionadores
        * next_level(): carga el siguiente nivel del mapa
        * draw(screen, camera_x, camera_z, camera_width, camera_height): dibuja el mapa en la pantalla
        * draw_collision_rects(screen, camera_x, camera_z, camera_width, camera_height): dibuja los rectángulos de colisión para depuración
    """
    def __init__(self, level: int) -> None:
        self.level = level
        self.tmx_data = None
        self.width = 0
        self.height = 0
        self.collision_rects = []
        self.navmesh: NavMesh | None = None
        self.load()

    def load(self) -> None:
        """
        Carga el mapa TMX correspondiente al nivel dado y procesa los colisionadores.
        Resetea la lista de rectángulos de colisión antes de cargar el nuevo mapa.
        Además, actualiza los atributos width y height del mapa.
        * [IMPORTANTE] Para la carga de colisionadores, se asume que existe una capa llamada "walls" en el TMX.
        """
        # --- Se crea la ruta al archivo TMX ---
        tmx_path = resource_path_dir(os.path.join("assets", "maps", CONF.MAP.LEVELS[self.level]))
        
        # --- Cargar datos del mapa TMX ---
        self.tmx_data = load_pygame(tmx_path)

        # --- Calcular el tamaño del mapa en píxeles (ya escalado) ---
        self.width = self.tmx_data.width * CONF.MAIN_WIN.RENDER_TILE_SIZE   # Ancho total del mapa en píxeles
        self.height = self.tmx_data.height * CONF.MAIN_WIN.RENDER_TILE_SIZE # Alto total del mapa en píxeles

        # --- Procesar colisionadores y NavMesh ---
        self.collision_rects = []
        navmesh_objects = []

        for layer_id, layer in enumerate(self.tmx_data.layers):
            # Cargar colisionadores de la capa "walls"
            if layer.name == "walls":
                # Obtiene todos los colisionadores definidos en el tileset (como objectgroup en Tiled)
                self.collision_rects = []
                colliders_gen = self.tmx_data.get_tile_colliders()
                colliders_list = list(colliders_gen)

                # Para cada tile del tileset que tiene colisionador (objectgroup)
                for i, (tile_id_local, obj_group) in enumerate(colliders_list):
                    if obj_group is not None:
                        # Para cada objeto de colisión dentro del objectgroup (puede haber varios por tile)
                        for obj in obj_group:
                            # Recorre todo el mapa buscando las posiciones donde ese tile está colocado
                            for y in range(self.tmx_data.height):
                                for x in range(self.tmx_data.width):
                                    gid = self.tmx_data.get_tile_gid(x, y, layer_id)
                                    # Si el GID del tile en el mapa coincide con el tile_id_local del colisionador
                                    if gid == tile_id_local:
                                        # Crea un rectángulo de colisión en coordenadas absolutas del mapa
                                        rect = pygame.Rect(
                                            int(x * CONF.MAIN_WIN.RENDER_TILE_SIZE + obj.x),
                                            int(y * CONF.MAIN_WIN.RENDER_TILE_SIZE + obj.y),
                                            int(obj.width * CONF.MAIN_WIN.ZOOM),
                                            int(obj.height * CONF.MAIN_WIN.ZOOM)
                                        )
                                        self.collision_rects.append(rect)
            
            # Recopilar objetos para NavMesh de la capa "graph"
            if layer.name == "graph":
                navmesh_objects.extend(list(layer))
        
        # Construir el NavMesh si se encontraron objetos
        if navmesh_objects:
            self.navmesh = NavMesh(navmesh_objects, CONF.MAIN_WIN.ZOOM)
            if CONF.DEV.DEBUG:
                print(f"[Map] NavMesh construido con {len(self.navmesh.nodes)} nodos.")

        if CONF.DEV.DEBUG:
            print(f"[Map] Mapa cargado: '{CONF.MAP.LEVELS[self.level]}'")
            print(f"[Map] Nivel actual: {self.level}.")
            print(f"[Map] Tamaño del tile: {CONF.MAIN_WIN.RENDER_TILE_SIZE}x{CONF.MAIN_WIN.RENDER_TILE_SIZE} píxeles.")
            print(f"[Map] Tamaño del mapa en tiles: {self.tmx_data.width}x{self.tmx_data.height} tiles.")
            print(f"[Map] Tamaño del mapa en píxeles: {self.width}x{self.height} píxeles.")
            print(f"[Map] Número de colisionadores: {len(self.collision_rects)}.")

    def next_level(self) -> None:
        """
        Carga el siguiente nivel del mapa.
        """
        if self.level + 1 in CONF.MAP.LEVELS:
            self.level += 1
            self.load()

    def draw(self, screen: pygame.Surface, camera_x: int, camera_z: int, camera_width: int, camera_height: int):
        """
        Dibuja todas las capas visibles del mapa en la superficie 'screen',
        ajustando la posición según la cámara (camera_x, camera_z).
        * Atributos:
            * screen: superficie de Pygame donde se dibuja el mapa
            * camera_x: posición X de la cámara (esquina superior izquierda)
            * camera_z: posición Z de la cámara (esquina superior izquierda)
            * camera_width: ancho del área visible de la cámara
            * camera_height: alto del área visible de la cámara
        """
        # Itera sobre todas las capas visibles del mapa
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                # Itera sobre todos los tiles de la capa
                for x, z, tile in layer.tiles():
                    tile_img = None
                    # tile puede ser una Surface o un GID
                    if isinstance(tile, pygame.Surface):
                        tile_img = pygame.transform.scale(tile, (CONF.MAIN_WIN.RENDER_TILE_SIZE, CONF.MAIN_WIN.RENDER_TILE_SIZE))
                    else:
                        tile_img = self.tmx_data.get_tile_image_by_gid(tile)
                        if tile_img:
                            tile_img = pygame.transform.scale(tile_img, (CONF.MAIN_WIN.RENDER_TILE_SIZE, CONF.MAIN_WIN.RENDER_TILE_SIZE))
                    # Si hay imagen de tile, calcular su posición en pantalla
                    if tile_img:
                        sx = x * CONF.MAIN_WIN.RENDER_TILE_SIZE - camera_x  # Posición X en pantalla (ajustada por la cámara)
                        sz = z * CONF.MAIN_WIN.RENDER_TILE_SIZE - camera_z  # Posición Z en pantalla (ajustada por la cámara)
                        # Solo dibuja el tile si está dentro de la cámara/ventana
                        if -CONF.MAIN_WIN.RENDER_TILE_SIZE < sx < camera_width and -CONF.MAIN_WIN.RENDER_TILE_SIZE < sz < camera_height:
                            screen.blit(tile_img, (sx, sz))

        """ if CONF.DEV.DEBUG:
            self.draw_collision_rects(screen, camera_x, camera_z, camera_width, camera_height)
            # Dibujar el NavMesh si existe
            if self.navmesh:
                self.navmesh.draw(screen, camera_x, camera_z) """

    def draw_collision_rects(self, screen: pygame.Surface, camera_x: int, camera_z: int, camera_width: int, camera_height: int):
        """
        Dibuja los rectángulos de colisión en la pantalla para depuración.
        Los rectángulos se dibujan en rojo semi-transparente.
        * Atributos:
            * screen: superficie de Pygame donde se dibujan los rectángulos
            * camera_x: posición X de la cámara (esquina superior izquierda)
            * camera_z: posición Z de la cámara (esquina superior izquierda)
            * camera_width: ancho del área visible de la cámara
            * camera_height: alto del área visible de la cámara
        """
        collider_surface = pygame.Surface((CONF.MAIN_WIN.RENDER_TILE_SIZE, CONF.MAIN_WIN.RENDER_TILE_SIZE), pygame.SRCALPHA)
        collider_surface.fill((255, 0, 0, 100))  # Rojo semi-transparente
        for rect in self.collision_rects:
            sx = rect.x - camera_x
            sz = rect.y - camera_z
            if -CONF.MAIN_WIN.RENDER_TILE_SIZE < sx < camera_width and -CONF.MAIN_WIN.RENDER_TILE_SIZE < sz < camera_height:
                # Dibuja el rectángulo del colisionador con el tamaño real
                debug_rect = pygame.Rect(sx, sz, rect.width, rect.height)
                pygame.draw.rect(screen, (255, 0, 0, 120), debug_rect, 1)  # Borde rojo
                # Si quieres ver el área rellena, descomenta la siguiente línea:
                # screen.blit(pygame.transform.scale(collider_surface, (rect.width, rect.height)), (sx, sz))