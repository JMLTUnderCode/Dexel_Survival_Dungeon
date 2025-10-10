import pygame
import sys
from characters.player import Player
from characters.enemy import Enemy
from data.enemies import list_of_enemies_data
from map.map import Map
from utils.configs import *

# --- Inicializar pygame y ventana principal ---
pygame.init()  # Inicializa todos los módulos de pygame
screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))  # Crea la ventana principal del juego
pygame.display.set_caption(GAME_TITLE)  # Establece el título de la ventana

clock = pygame.time.Clock()  # Reloj para controlar el framerate

# --- Cargar el mapa ---
#game_map = Map("map.tmx") # Principal
game_map = Map("presentacion-1.tmx") # Presentacion 1

# --- Inicializar jugador ---
player = Player(
    type="oldman",
    position=(RENDER_TILE_SIZE*30, RENDER_TILE_SIZE*30),
    collider_box=(PLAYER_COLLIDER_BOX_WIDTH, PLAYER_COLLIDER_BOX_HEIGHT),
    maxSpeed=210,
)

# --- Inicializar enemigo (bot que sigue al jugador) ---
enemy_list = list_of_enemies_data["ALL"]  # Cambiar aquí para probar diferentes algoritmos
enemies = [
    Enemy(
        type=enemy["type"],
        position=enemy["position"],
        collider_box=enemy["collider_box"],
        target=player,
        algorithm=enemy["algorithm"],
        maxSpeed=enemy["maxSpeed"],
        target_radius=enemy["target_radius"],
        slow_radius=enemy["slow_radius"],
        time_to_target=enemy["time_to_target"],
        max_acceleration=enemy["max_acceleration"],
        max_rotation=enemy["max_rotation"],
    )
    for enemy in enemy_list
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
        player.update(screen, camera_x, camera_z, game_map.collision_rects, dt)
        
        # --- Actualizar enemigo
        for enemy in enemies:
            enemy.update(screen, camera_x, camera_z, game_map.collision_rects, dt)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()