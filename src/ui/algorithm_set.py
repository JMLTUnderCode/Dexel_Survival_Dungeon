import pygame
from characters.player import Player
from characters.enemy import Enemy
from data.enemies import list_of_enemies_data
from utils.configs import *

# Construcción dinámica de botones según las claves disponibles en data
BUTTON_KEYS = list(list_of_enemies_data.keys())

# --- Inicial create (por defecto ALL) ---
# Helper para crear player y la lista de enemigos desde una key del data set
def create_player_and_enemies(key="ALL"):
    """
    Crea/Resetea globalmente `player` y `enemies` usando list_of_enemies_data[key].
    Si la key no existe, usa "ALL" o la primera disponible.
    """
    if key not in list_of_enemies_data:
        key = "ALL" if "ALL" in list_of_enemies_data else next(iter(list_of_enemies_data.keys()))
    enemy_list = list_of_enemies_data[key]

    # Re-crear player (reset)
    player = Player(
        type="oldman",
        position=(RENDER_TILE_SIZE*30, RENDER_TILE_SIZE*30),
        collider_box=(PLAYER_COLLIDER_BOX_WIDTH, PLAYER_COLLIDER_BOX_HEIGHT),
        maxSpeed=210,
    )

    # Re-crear enemies
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

    return player, enemies

def handle_ui_event(event: pygame.event.Event, player, enemies):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mx, my = event.pos
        for b in UI_BUTTONS:
            if b["rect"].collidepoint((mx, my)):
                # devuelve los nuevos player, enemies y una señal de que hubo cambio
                new_player, new_enemies = create_player_and_enemies(b["key"])
                return new_player, new_enemies, True
    return player, enemies, False

# UI state
def build_ui_buttons():
    UI_BUTTONS.clear()
    y = UI_PADDING + 48
    for k in BUTTON_KEYS:
        rect = pygame.Rect(UI_PADDING, y, UI_PANEL_WIDTH - UI_PADDING*2, UI_BUTTON_HEIGHT)
        UI_BUTTONS.append({"key": k, "rect": rect})
        y += UI_BUTTON_HEIGHT + 8

def draw_ui(surface):
    # Panel con fondo semitransparente
    panel_rect = pygame.Rect(0, 0, UI_PANEL_WIDTH, CAMERA_HEIGHT)
    s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    s.fill((30, 30, 30, 220))
    surface.blit(s, (panel_rect.x, panel_rect.y))

    # Título
    title_surf = UI_TITLE_FONT.render("ENEMY SET", True, UI_TITLE_COLOR)
    surface.blit(title_surf, (UI_PADDING, UI_PADDING))

    # Botones
    mx, my = pygame.mouse.get_pos()
    for b in UI_BUTTONS:
        rect = b["rect"]
        hovered = rect.collidepoint((mx, my))
        color = UI_BUTTON_HOVER if hovered else UI_BUTTON_COLOR
        label = parsing_button.get(str(b["key"]), str(b["key"]))
        pygame.draw.rect(surface, color, rect, border_radius=6)
        txt = UI_FONT.render(label, True, UI_TEXT_COLOR)
        tx = rect.x + 12
        ty = rect.y + (rect.height - txt.get_height()) // 2
        surface.blit(txt, (tx, ty))

def init_ui_fonts(title_font_name: str = "Segoe UI", title_size: int = 20, font_name: str = "Segoe UI", font_size: int = 16) -> None:
    """
    Inicializa las fuentes usadas por la UI. Debe llamarse después de pygame.init().

    Intenta usar SysFont con el nombre indicado y, si falla, usa la fuente por defecto.
    """
    global UI_TITLE_FONT, UI_FONT

    # Asegurar que pygame esté inicializado
    if not pygame.get_init():
        pygame.init()

    try:
        UI_TITLE_FONT = pygame.font.SysFont(title_font_name, title_size, bold=True)
    except Exception:
        UI_TITLE_FONT = pygame.font.Font(None, title_size)
        try:
            UI_TITLE_FONT.set_bold(True)
        except Exception:
            pass

    try:
        UI_FONT = pygame.font.SysFont(font_name, font_size, bold=False)
    except Exception:
        UI_FONT = pygame.font.Font(None, font_size)