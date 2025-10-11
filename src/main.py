import pygame
import sys
from map.map import Map
from utils.configs import *
from ui.algorithm_set import *

# --- Inicializar pygame y ventana principal ---
pygame.init()  # Inicializa todos los módulos de pygame
screen = pygame.display.set_mode((CAMERA_WIDTH + UI_PANEL_WIDTH, CAMERA_HEIGHT))  # Crea la ventana principal del juego
game_surface = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT)) # Surface donde se renderiza la escena de juego (sin UI)
pygame.display.set_caption(GAME_TITLE)  # Establece el título de la ventana

# --- Reloj para controlar el framerate ---
clock = pygame.time.Clock()

# --- Cargar el mapa ---
#game_map = Map("map.tmx") # Principal
game_map = Map("presentacion-1.tmx") # Presentacion 1

# --- Inicializar UI ---
init_ui_fonts()
build_ui_buttons()

# --- Inicializar jugador y enemigos ---
player, enemies = create_player_and_enemies("ALL")

def main():
    global player, enemies
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # segundos

        # --- Manejar eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            player, enemies, changed = handle_ui_event(event, player, enemies)
            if not changed:
                # Si el evento es del mouse y está dentro del área de juego, ajustar la posición X para que
                # sea relativa al game_surface antes de pasarlo a player.handle_event
                if hasattr(event, "pos"):
                    ex, ey = event.pos
                    if ex > UI_PANEL_WIDTH:
                        # crear un evento "game_event" con pos ajustada y pasar a player
                        adjusted_event = event
                        # Pygame Event is mutable on some attributes; safer to create a new event for mouse positions
                        try:
                            adjusted_event = pygame.event.Event(event.type, {**event.__dict__, "pos": (ex - UI_PANEL_WIDTH, ey)})
                        except Exception:
                            adjusted_event = event
                        player.handle_event(adjusted_event)
                    else:
                        # click on UI left panel (already handled by handle_ui_event), ignore for player
                        pass
                else:
                    player.handle_event(event)

        # --- Obtener posición del jugador ---
        px, pz = player.get_pos()

        # --- Cámara ---
        camera_x = px - CAMERA_WIDTH // 2
        camera_z = pz - CAMERA_HEIGHT // 2
        # Limitar cámara a los bordes del mapa
        camera_x = max(0, min(camera_x, game_map.width - CAMERA_WIDTH))
        camera_z = max(0, min(camera_z, game_map.height - CAMERA_HEIGHT))
        
        # --- Render: dibujar todo en game_surface (área de juego) y luego blittear a screen desplazado ---
        game_surface.fill((30, 30, 30))

        game_map.draw(game_surface, camera_x, camera_z)

        # --- Actualizar jugador (player.update internamente usa pygame.mouse.get_pos -> ajustado en player.handle_input) 
        player.update(game_surface, camera_x, camera_z, game_map.collision_rects, dt)
        
        # --- Actualizar enemigos (se dibujan dentro de game_surface)
        for enemy in enemies:
            enemy.update(game_surface, camera_x, camera_z, game_map.collision_rects, dt)

        # --- Blit del area de juego en la pantalla principal, desplazada a la derecha por UI_PANEL_WIDTH ---
        screen.fill((0, 0, 0))  # fondo detrás del panel (opcional)
        screen.blit(game_surface, (UI_PANEL_WIDTH, 0))

        # --- Dibujar UI (panel izquierdo) encima de todo (UI dibuja en coordenadas de pantalla)
        draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()