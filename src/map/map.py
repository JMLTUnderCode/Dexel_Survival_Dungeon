import os
import pygame
from pytmx.util_pygame import load_pygame
from utils.resource_path import resource_path
from utils.configs import *

class Map:
    """
    Clase que representa el mapa del juego cargado desde un archivo TMX.
    Atributos:
        tmx_data: datos del mapa cargados con pytmx
        width: ancho del mapa en píxeles (ya escalado)
        height: alto del mapa en píxeles (ya escalado)
        collision_rects: lista de pygame.Rect que representan las áreas de colisión
    """
    def __init__(self, tmx_file):
        # --- Cargar el mapa TMX usando pytmx ---
        tmx_path = resource_path(os.path.join("..", "assets", "maps", tmx_file))  # Ruta al archivo TMX del mapa
        # Carga el mapa de Tiled (formato TMX) y lo adapta para usar con pygame
        # tmx_data contiene todas las capas, tiles y objetos del mapa
        # Es importante que el archivo .tmx y los tilesets estén en la ruta correcta
        # pytmx permite acceder a las capas, tiles y propiedades del mapa fácilmente
        # Ejemplo: tmx_data.width, tmx_data.height, tmx_data.visible_layers
        # Cada tile es una Surface de pygame
        # El mapa puede tener varias capas (background, colisiones, decoraciones, etc)
        self.tmx_data = load_pygame(tmx_path)

        # --- Calcular el tamaño del mapa en píxeles (ya escalado) ---
        self.width = self.tmx_data.width * RENDER_TILE_SIZE   # Ancho total del mapa en píxeles
        self.height = self.tmx_data.height * RENDER_TILE_SIZE # Alto total del mapa en píxeles

        # --- Procesar colisionadores ---
        # Busca el índice de la capa llamada "walls" (donde están los tiles de colisión)
        walls_layer = None
        for i, layer in enumerate(self.tmx_data.layers):
            if hasattr(layer, 'name') and layer.name == "walls":
                walls_layer = i

        if walls_layer is None:
            raise Exception("No se encontró la capa 'walls' en el mapa.")

        # Inicializa la lista de rectángulos de colisión
        self.collision_rects = []

        # Obtiene todos los colisionadores definidos en el tileset (como objectgroup en Tiled)
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
                            gid = self.tmx_data.get_tile_gid(x, y, walls_layer)
                            # Si el GID del tile en el mapa coincide con el tile_id_local del colisionador
                            if gid == tile_id_local:
                                # Crea un rectángulo de colisión en coordenadas absolutas del mapa
                                rect = pygame.Rect(
                                    int(x * RENDER_TILE_SIZE + obj.x),
                                    int(y * RENDER_TILE_SIZE + obj.y),
                                    int(obj.width * ZOOM),
                                    int(obj.height * ZOOM)
                                )
                                self.collision_rects.append(rect)
        print(f"[Map] Cargado mapa '{tmx_file}' con {len(self.collision_rects)} colisionadores.")

    def draw(self, screen, camera_x, camera_z):
        """
        Dibuja todas las capas visibles del mapa en la superficie 'screen',
        ajustando la posición según la cámara (camera_x, camera_z).
        """
        # Itera sobre todas las capas visibles del mapa
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                # Itera sobre todos los tiles de la capa
                for x, z, tile in layer.tiles():
                    # tile puede ser una Surface o un GID
                    if isinstance(tile, pygame.Surface):
                        tile_img = pygame.transform.scale(tile, (RENDER_TILE_SIZE, RENDER_TILE_SIZE))
                    else:
                        tile_img = self.tmx_data.get_tile_image_by_gid(tile)
                        if tile_img:
                            tile_img = pygame.transform.scale(tile_img, (RENDER_TILE_SIZE, RENDER_TILE_SIZE))
                    # Si hay imagen de tile, calcular su posición en pantalla
                    if tile_img:
                        sx = x * RENDER_TILE_SIZE - camera_x  # Posición X en pantalla (ajustada por la cámara)
                        sz = z * RENDER_TILE_SIZE - camera_z  # Posición Y en pantalla (ajustada por la cámara)
                        # Solo dibuja el tile si está dentro de la cámara/ventana
                        if -RENDER_TILE_SIZE < sx < CAMERA_WIDTH and -RENDER_TILE_SIZE < sz < CAMERA_HEIGHT:
                            screen.blit(tile_img, (sx, sz))

        if DEVELOPMENT:
            self.draw_collision_rects(screen, camera_x, camera_z)

    def draw_collision_rects(self, screen, camera_x, camera_z):
        """
        Dibuja los rectángulos de colisión en la pantalla para depuración.
        Los rectángulos se dibujan en rojo semi-transparente.
        """
        collider_surface = pygame.Surface((RENDER_TILE_SIZE, RENDER_TILE_SIZE), pygame.SRCALPHA)
        collider_surface.fill((255, 0, 0, 100))  # Rojo semi-transparente
        for rect in self.collision_rects:
            sx = rect.x - camera_x
            sz = rect.y - camera_z
            if -RENDER_TILE_SIZE < sx < CAMERA_WIDTH and -RENDER_TILE_SIZE < sz < CAMERA_HEIGHT:
                # Dibuja el rectángulo del colisionador con el tamaño real
                debug_rect = pygame.Rect(sx, sz, rect.width, rect.height)
                pygame.draw.rect(screen, (255, 0, 0, 120), debug_rect, 1)  # Borde rojo
                # Si quieres ver el área rellena, descomenta la siguiente línea:
                # screen.blit(pygame.transform.scale(collider_surface, (rect.width, rect.height)), (sx, sz))