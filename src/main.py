import pygame
import sys

# Configuración inicial
GAME_TITLE = "Dexel Survival Dungeon"
FPS = 60

# Inicializar pygame
pygame.init()

# Obtener tamaño de pantalla y reducir al 95%
info = pygame.display.Info()
SCREEN_WIDTH = int(info.current_w * 0.95)
SCREEN_HEIGHT = int(info.current_h * 0.95)

# Crear ventana en modo ventana (no redimensionable), 95% de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# Fuente para el texto
font = pygame.font.SysFont(None, 80)
text = font.render(GAME_TITLE, True, (255, 255, 255))
text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

clock = pygame.time.Clock()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(FPS)
