import pygame
from data.enemies import list_of_enemies_data
from utils.create_characters import create_player_and_enemies
import utils.configs as configs

# Construcción dinámica de botones según las claves disponibles en data
BUTTON_KEYS = list(list_of_enemies_data.keys())

def handle_ui_event(event: pygame.event.Event, player, enemies):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mx, my = event.pos
        for b in configs.UI_BUTTONS:
            if b["rect"].collidepoint((mx, my)):
                # marcar el botón seleccionado (desmarca el anterior)
                configs.SELECTED_KEY = b["key"]
                # devuelve los nuevos player, enemies y una señal de que hubo cambio
                new_player, new_enemies = create_player_and_enemies(b["key"])
                return new_player, new_enemies, True
    return player, enemies, False

# UI state
def build_ui_buttons():
    configs.UI_BUTTONS.clear()
    y = configs.UI_PADDING + 48
    for k in BUTTON_KEYS:
        rect = pygame.Rect(configs.UI_PADDING, y, configs.UI_PANEL_WIDTH - configs.UI_PADDING*2, configs.UI_BUTTON_HEIGHT)
        configs.UI_BUTTONS.append({"key": k, "rect": rect})
        y += configs.UI_BUTTON_HEIGHT + 8

def draw_ui(surface: pygame.Surface, ui_width: int, ui_height: int):
    # Panel con fondo semitransparente
    panel_rect = pygame.Rect(0, 0, ui_width, ui_height)
    s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    s.fill((30, 30, 30, 220))
    surface.blit(s, (panel_rect.x, panel_rect.y))

    # Título
    title_surf = configs.UI_TITLE_FONT.render("ENEMY SET", True, configs.UI_TITLE_COLOR)
    surface.blit(title_surf, (configs.UI_PADDING, configs.UI_PADDING))

    # Botones
    mx, my = pygame.mouse.get_pos()
    for b in configs.UI_BUTTONS:
        rect = b["rect"]
        hovered = rect.collidepoint((mx, my))
        # Button color precedence: seleccionado -> hover -> normal
        if b["key"] == configs.SELECTED_KEY:
            color = configs.UI_BUTTON_ACTIVE
        else:
            color = configs.UI_BUTTON_HOVER if hovered else configs.UI_BUTTON_COLOR
        label = configs.parsing_button.get(str(b["key"]), str(b["key"]))
        pygame.draw.rect(surface, color, rect, border_radius=6)
        txt = configs.UI_FONT.render(label, True, configs.UI_TEXT_COLOR)
        tx = rect.x + 12
        ty = rect.y + (rect.height - txt.get_height()) // 2
        surface.blit(txt, (tx, ty))

def init_ui_fonts(title_font_name: str = "Segoe UI", title_size: int = 20, font_name: str = "Segoe UI", font_size: int = 16) -> None:
    """
    Inicializa las fuentes usadas por la UI. Debe llamarse después de pygame.init().

    Intenta usar SysFont con el nombre indicado y, si falla, usa la fuente por defecto.
    """

    # Asegurar que pygame esté inicializado
    if not pygame.get_init():
        pygame.init()

    try:
        configs.UI_TITLE_FONT = pygame.font.SysFont(title_font_name, title_size, bold=True)
    except Exception:
        configs.UI_TITLE_FONT = pygame.font.Font(None, title_size)
        try:
            configs.UI_TITLE_FONT.set_bold(True)
        except Exception:
            pass

    try:
        configs.UI_FONT = pygame.font.SysFont(font_name, font_size, bold=False)
    except Exception:
        configs.UI_FONT = pygame.font.Font(None, font_size)