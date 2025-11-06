import pygame

if not pygame.get_init():
    pygame.init()

ACTIVE = True
PANEL_WIDTH = 200
PADDING = 12
BUTTON_HEIGHT = 36
BG_COLOR = (20, 20, 20, 220)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (70, 70, 70)
BUTTON_ACTIVE = (132, 87, 69)
TEXT_COLOR = (230, 230, 230)
TITLE = "MAP LEVELS"
TITLE_COLOR = (180, 220, 255)
TITLE_FONT = pygame.font.SysFont("Segoe UI", 20, bold=True)
FONT = pygame.font.SysFont("Segoe UI", 16)

BUTTONS = []
PARSING_BUTTONS = {
    "1" : "Level 1",
    "2" : "Level 2",
}
SELECTED = 2