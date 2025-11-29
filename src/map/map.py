import os
import pygame
from typing import Optional, List
from pytmx.util_pygame import load_pygame
from utils.resource_path_dir import resource_path_dir
from .navmesh import NavMesh
from configs.package import CONF

class Map:
    """
    Descripción
        CLASE: Representa el mapa del juego cargado desde un archivo TMX.

    Atributos
        - level (int): índice del nivel actual.
        - tmx_data (pytmx.TiledMap | None): datos cargados del TMX.
        - width (int): ancho del mapa en píxeles.
        - height (int): alto del mapa en píxeles.
        - collision_rects (List[pygame.Rect]): rectángulos de colisión del mapa.
        - navmesh (Optional[NavMesh]): instancia de NavMesh para pathfinding (si existe).

    Métodos y Funciones
        - load(): carga y procesa el TMX actual.
        - next_level(): avanza al siguiente nivel si existe.
        - draw(screen, camera_x, camera_z, camera_width, camera_height): dibuja el mapa.
        - draw_collision_rects(screen, camera_x, camera_z, camera_width, camera_height): dibuja rects debug.
    
    Propósito
        - Gestionar la carga, procesamiento y renderizado del mapa así como exponer
          colisiones y navmesh para el resto del motor.
    """
    def __init__(self, level: int) -> None:
        # Inicializar estado básico del mapa
        self.level: int = level
        self.tmx_data = None
        self.width: int = 0
        self.height: int = 0
        self.collision_rects: List[pygame.Rect] = []
        self.navmesh: Optional[NavMesh] = None

        # Cargar inmediatamente el mapa inicial
        self.load()

    def load(self) -> None:
        """
        Descripción
            MÉTODO: Carga el archivo TMX asociado al nivel actual y procesa colisionadores y navmesh.

        Argumentos
            - Ninguno
        """
        # 1. Construir la ruta al archivo TMX a partir de la configuración y resolverla
        tmx_path = resource_path_dir(os.path.join("assets", "maps", CONF.MAP.LEVELS[self.level]))

        # 2. Cargar los datos TMX usando pytmx (con soporte para pygame)
        self.tmx_data = load_pygame(tmx_path)

        # 3. Calcular dimensiones totales del mapa en píxeles
        self.width = int(self.tmx_data.width * CONF.MAIN_WIN.RENDER_TILE_SIZE)
        self.height = int(self.tmx_data.height * CONF.MAIN_WIN.RENDER_TILE_SIZE)

        # 4. Resetear colecciones de colisiones y objetos de navmesh
        self.collision_rects = []
        navmesh_objects = []

        # 5. Iterar capas para extraer colisionadores y objetos del grafo
        for layer_id, layer in enumerate(self.tmx_data.layers):
            # 5.1 Procesar colisionadores definidos en la capa "walls"
            if getattr(layer, "name", None) == "walls":
                # Obtener todos los colliders definidos por tile en el tileset
                colliders_gen = self.tmx_data.get_tile_colliders()
                colliders_list = list(colliders_gen)

                # Para cada tile que tiene un objectgroup de colisión
                for tile_id_local, obj_group in colliders_list:
                    if obj_group is None:
                        continue
                    # Recorremos todo el mapa buscando dónde aparece ese gid
                    for y in range(self.tmx_data.height):
                        for x in range(self.tmx_data.width):
                            gid = self.tmx_data.get_tile_gid(x, y, layer_id)
                            if gid != tile_id_local:
                                continue
                            # Para cada objeto de colisión en el objectgroup generar un rect absoluto
                            for obj in obj_group:
                                rect = pygame.Rect(
                                    int(x * CONF.MAIN_WIN.RENDER_TILE_SIZE + obj.x),
                                    int(y * CONF.MAIN_WIN.RENDER_TILE_SIZE + obj.y),
                                    int(obj.width * CONF.MAIN_WIN.ZOOM),
                                    int(obj.height * CONF.MAIN_WIN.ZOOM)
                                )
                                self.collision_rects.append(rect)

            # 5.2 Recolectar objetos para el NavMesh desde la capa "graph"
            if getattr(layer, "name", None) == "graph":
                navmesh_objects.extend(list(layer))

        # 6. Construir NavMesh si se encontraron objetos de grafo
        if navmesh_objects:
            self.navmesh = NavMesh(navmesh_objects, CONF.MAIN_WIN.ZOOM)
            if CONF.DEV.DEBUG:
                print(f"[Map] NavMesh construido con {len(self.navmesh.nodes)} nodos.")

        # 7. Debug: imprimir resumen de carga
        if CONF.DEV.DEBUG:
            print(f"[Map] Mapa cargado: '{CONF.MAP.LEVELS[self.level]}'")
            print(f"[Map] Nivel actual: {self.level}. Tamaño tiles: {CONF.MAIN_WIN.RENDER_TILE_SIZE}.")
            print(f"[Map] Dimensiones: {self.width}x{self.height} px. Colisionadores: {len(self.collision_rects)}.")

    def next_level(self) -> None:
        """
        Descripción
            MÉTODO: Avanza y carga el siguiente nivel si existe en la configuración.

        Argumentos
            - Ninguno
        """
        # 1. Verificar existencia del siguiente nivel y recargar
        if (self.level + 1) in CONF.MAP.LEVELS:
            self.level += 1
            self.load()

    def draw(self, screen: pygame.Surface, camera_x: int, camera_z: int, camera_width: int, camera_height: int) -> None:
        """
        Descripción
            MÉTODO: Dibuja las capas visibles del mapa en la superficie indicada ajustando por la cámara.

        Argumentos
            - screen (pygame.Surface): Superficie de destino donde se dibuja el mapa.
            - camera_x (int): Coordenada X de la cámara (esquina superior izquierda).
            - camera_z (int): Coordenada Z de la cámara (esquina superior izquierda).
            - camera_width (int): Ancho del área visible en píxeles.
            - camera_height (int): Alto del área visible en píxeles.
        """
        # 1. Iterar capas visibles y dibujar tiles que estén dentro del área de la cámara
        for layer in getattr(self.tmx_data, "visible_layers", []):
            if not hasattr(layer, "tiles"):
                continue
            for x, z, tile in layer.tiles():
                tile_img = None
                # 2. Obtener la imagen del tile ya escalada si es necesario
                if isinstance(tile, pygame.Surface):
                    tile_img = pygame.transform.scale(tile, (CONF.MAIN_WIN.RENDER_TILE_SIZE, CONF.MAIN_WIN.RENDER_TILE_SIZE))
                else:
                    tile_img = self.tmx_data.get_tile_image_by_gid(tile)
                    if tile_img:
                        tile_img = pygame.transform.scale(tile_img, (CONF.MAIN_WIN.RENDER_TILE_SIZE, CONF.MAIN_WIN.RENDER_TILE_SIZE))

                # 3. Si existe imagen, calcular posición en pantalla y dibujar si visible
                if tile_img:
                    sx = x * CONF.MAIN_WIN.RENDER_TILE_SIZE - camera_x
                    sz = z * CONF.MAIN_WIN.RENDER_TILE_SIZE - camera_z
                    if -CONF.MAIN_WIN.RENDER_TILE_SIZE < sx < camera_width and -CONF.MAIN_WIN.RENDER_TILE_SIZE < sz < camera_height:
                        screen.blit(tile_img, (sx, sz))

        # 4. Opciones de depuración: dibujar colisiones y navmesh
        if CONF.DEV.DEBUG:
            if CONF.DEV.COLLISION_RECTS:
                self.draw_collision_rects(screen, camera_x, camera_z, camera_width, camera_height)
            if CONF.DEV.NAV_MESH and self.navmesh:
                self.navmesh.draw(screen, camera_x, camera_z)

    def draw_collision_rects(self, screen: pygame.Surface, camera_x: int, camera_z: int, camera_width: int, camera_height: int) -> None:
        """
        Descripción
            MÉTODO: Dibuja los rectángulos de colisión en pantalla para depuración.

        Argumentos
            - screen (pygame.Surface): Superficie de destino donde dibujar.
            - camera_x (int): Coordenada X de la cámara.
            - camera_z (int): Coordenada Z de la cámara.
            - camera_width (int): Ancho del área visible.
            - camera_height (int): Alto del área visible.
        """
        # 1. Preparar una superficie semitransparente para dibujar áreas si se desea
        collider_surface = pygame.Surface((CONF.MAIN_WIN.RENDER_TILE_SIZE, CONF.MAIN_WIN.RENDER_TILE_SIZE), pygame.SRCALPHA)
        collider_surface.fill((255, 0, 0, 100))

        # 2. Iterar rectángulos y dibujar los que están dentro del viewport
        for rect in self.collision_rects:
            sx = rect.x - camera_x
            sz = rect.y - camera_z
            if -CONF.MAIN_WIN.RENDER_TILE_SIZE < sx < camera_width and -CONF.MAIN_WIN.RENDER_TILE_SIZE < sz < camera_height:
                debug_rect = pygame.Rect(sx, sz, rect.width, rect.height)
                # 3. Dibujar borde del rectángulo en rojo
                pygame.draw.rect(screen, (255, 0, 0, 120), debug_rect, 1)
                # 4. Si se quiere ver el área rellena, descomentar la siguiente línea
                # screen.blit(pygame.transform.scale(collider_surface, (rect.width, rect.height)), (sx, sz))