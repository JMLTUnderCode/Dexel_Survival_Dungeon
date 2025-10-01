import pygame
import sys
import os
from pytmx.util_pygame import load_pygame
from player import Player

# Configuración
GAME_TITLE = "Dexel Survival Dungeon"
FPS = 60
TILE_SIZE = 16
ZOOM = 2
RENDER_TILE_SIZE = TILE_SIZE * ZOOM  # 2x, cada tile se verá de 32x32
CAMERA_WIDTH = 1200
CAMERA_HEIGHT = 800

# --- Inicializar pygame y ventana principal ---
pygame.init()  # Inicializa todos los módulos de pygame
screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))  # Crea la ventana principal del juego
pygame.display.set_caption(GAME_TITLE)  # Establece el título de la ventana

# --- Cargar el mapa TMX usando pytmx ---
tmx_path = os.path.join(os.path.dirname(__file__), "maps/map.tmx")  # Ruta al archivo TMX del mapa
# Carga el mapa de Tiled (formato TMX) y lo adapta para usar con pygame
# tmx_data contiene todas las capas, tiles y objetos del mapa
# Es importante que el archivo .tmx y los tilesets estén en la ruta correcta
# pytmx permite acceder a las capas, tiles y propiedades del mapa fácilmente
# Ejemplo: tmx_data.width, tmx_data.height, tmx_data.visible_layers
# Cada tile es una Surface de pygame
# El mapa puede tener varias capas (background, colisiones, decoraciones, etc)
tmx_data = load_pygame(tmx_path)

# --- Calcular el tamaño del mapa en píxeles (ya escalado) ---
map_width = tmx_data.width * RENDER_TILE_SIZE   # Ancho total del mapa en píxeles
map_height = tmx_data.height * RENDER_TILE_SIZE # Alto total del mapa en píxeles

clock = pygame.time.Clock()  # Reloj para controlar el framerate

# --- Función para dibujar el mapa en pantalla ---
def draw_map(camera_x, camera_z):
    # Itera sobre todas las capas visibles del mapa
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'tiles'):
            # Itera sobre todos los tiles de la capa
            for x, z, tile in layer.tiles():
                # tile puede ser una Surface o un GID
                if isinstance(tile, pygame.Surface):
                    tile_img = pygame.transform.scale(tile, (RENDER_TILE_SIZE, RENDER_TILE_SIZE))
                else:
                    tile_img = tmx_data.get_tile_image_by_gid(tile)
                    if tile_img:
                        tile_img = pygame.transform.scale(tile_img, (RENDER_TILE_SIZE, RENDER_TILE_SIZE))
                # Si hay imagen de tile, calcular su posición en pantalla
                if tile_img:
                    sx = x * RENDER_TILE_SIZE - camera_x  # Posición X en pantalla (ajustada por la cámara)
                    sz = z * RENDER_TILE_SIZE - camera_z  # Posición Y en pantalla (ajustada por la cámara)
                    # Solo dibuja el tile si está dentro de la cámara/ventana
                    if -RENDER_TILE_SIZE < sx < CAMERA_WIDTH and -RENDER_TILE_SIZE < sz < CAMERA_HEIGHT:
                        screen.blit(tile_img, (sx, sz))


# --- Inicializar jugador ---
player = Player(
    position=(map_width // 2, map_height // 2),
    maxSpeed=250,
    map_width=map_width,
    map_height=map_height,
)

def main():
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0  # segundos

        # --- Manejar eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_event(event)

        # --- Obtener posición del jugador ---
        px, pz = player.get_pos()

        # --- Cámara ---
        camera_x = px - CAMERA_WIDTH // 2
        camera_z = pz - CAMERA_HEIGHT // 2
        # Limitar cámara a los bordes del mapa
        camera_x = max(0, min(camera_x, map_width - CAMERA_WIDTH))
        camera_z = max(0, min(camera_z, map_height - CAMERA_HEIGHT))
        
        # --- Actualizar jugador ---
        player.handle_input(camera_x, camera_z) # Actualizar entrada de control
        player.check_changes(dt)                # Actualizar estado del jugador

        # --- Dibujar ---
        screen.fill((30, 30, 30))
        draw_map(camera_x, camera_z)
        player.draw(screen, camera_x, camera_z)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    pygame.display.flip()
    clock.tick(FPS)