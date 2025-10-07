import pygame
import sys
from player import Player
from enemy import Enemy
from map import Map
from configs import *

# --- Inicializar pygame y ventana principal ---
pygame.init()  # Inicializa todos los módulos de pygame
screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))  # Crea la ventana principal del juego
pygame.display.set_caption(GAME_TITLE)  # Establece el título de la ventana

clock = pygame.time.Clock()  # Reloj para controlar el framerate

# --- Cargar el mapa ---
game_map = Map("map.tmx")

# --- Inicializar jugador ---
player = Player(
    type="oldman",
    position=(RENDER_TILE_SIZE*14, RENDER_TILE_SIZE*10),
    maxSpeed=200,
    map_width=game_map.width,
    map_height=game_map.height,
    collision_rects=game_map.collision_rects,
)

# --- Inicializar enemigo (bot que sigue al jugador) ---
enemy_configs = [
    {"type": "gargant-soldier", "target": player, "position": (RENDER_TILE_SIZE*3, RENDER_TILE_SIZE*3)},
    {"type": "gargant-berserker", "target": player, "position": (RENDER_TILE_SIZE*42, RENDER_TILE_SIZE*7)},
    {"type": "gargant-berserker", "target": player, "position": (RENDER_TILE_SIZE*36, RENDER_TILE_SIZE*19)},
    {"type": "gargant-berserker", "target": player, "position": (RENDER_TILE_SIZE*42, RENDER_TILE_SIZE*19)},
    {"type": "gargant-berserker", "target": player, "position": (RENDER_TILE_SIZE*54, RENDER_TILE_SIZE*19)},
    {"type": "gargant-lord", "target": player, "position": (RENDER_TILE_SIZE*52, RENDER_TILE_SIZE*33)},
    {"type": "gargant-lord", "target": player, "position": (RENDER_TILE_SIZE*14, RENDER_TILE_SIZE*33)},
    {"type": "gargant-boss", "target": player, "position": (RENDER_TILE_SIZE*45, RENDER_TILE_SIZE*49)},
]

enemies = [
    Enemy(
        type=cfg["type"],
        position=cfg["position"],
        target=cfg["target"],
        maxSpeed=190,
        map_width=game_map.width,
        map_height=game_map.height,
        collision_rects=game_map.collision_rects,
    )
    for cfg in enemy_configs
]

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
        camera_x = max(0, min(camera_x, game_map.width - CAMERA_WIDTH))
        camera_z = max(0, min(camera_z, game_map.height - CAMERA_HEIGHT))
        
        screen.fill((30, 30, 30))

        game_map.draw(screen, camera_x, camera_z)

        # --- Actualizar jugador
        player.draw(screen, camera_x, camera_z)
        player.handle_input(camera_x, camera_z, dt)
        player.check_changes(dt)
        
        # --- Actualizar enemigo
        for enemy in enemies:
            enemy.update(dt)
            enemy.draw(screen, camera_x, camera_z)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()