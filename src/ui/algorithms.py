import pygame
from data.enemies import list_of_enemies_data
from helper.player import create_player
from helper.enemies import create_enemies
from configs.package import CONF

# Construcción dinámica de botones según las claves disponibles en data


def handle_ui_event(event: pygame.event.Event, player, enemies):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mx, my = event.pos
        for b in CONF.ALG_UI.BUTTONS:
            if b["rect"].collidepoint((mx, my)):
                # marcar el botón seleccionado (desmarca el anterior)
                CONF.ALG_UI.SELECTED_ALGORITHM = b["key"]
                # devuelve los nuevos player, enemies y una señal de que hubo cambio
                new_player = create_player()
                new_enemies = create_enemies(algorithm=b["key"], target=new_player)
                return new_player, new_enemies, True
    return player, enemies, False

# UI state
def build_ui_buttons():
    button_keys = list(list_of_enemies_data.keys())
    CONF.ALG_UI.BUTTONS.clear()
    y = CONF.ALG_UI.PADDING + 48
    for k in button_keys:
        rect = pygame.Rect(CONF.ALG_UI.PADDING, y, CONF.ALG_UI.PANEL_WIDTH - CONF.ALG_UI.PADDING*2, CONF.ALG_UI.BUTTON_HEIGHT)
        CONF.ALG_UI.BUTTONS.append({"key": k, "rect": rect})
        y += CONF.ALG_UI.BUTTON_HEIGHT + 8

def draw_ui(surface: pygame.Surface, ui_width: int, ui_height: int):
    # Panel con fondo semitransparente
    panel_rect = pygame.Rect(0, 0, ui_width, ui_height)
    s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    s.fill((30, 30, 30, 220))
    surface.blit(s, (panel_rect.x, panel_rect.y))

    # Título
    title_surf = CONF.ALG_UI.TITLE_FONT.render("ENEMY SET", True, CONF.ALG_UI.TITLE_COLOR)
    surface.blit(title_surf, (CONF.ALG_UI.PADDING, CONF.ALG_UI.PADDING))

    # Botones
    mx, my = pygame.mouse.get_pos()
    for b in CONF.ALG_UI.BUTTONS:
        rect = b["rect"]
        hovered = rect.collidepoint((mx, my))
        # Button color precedence: seleccionado -> hover -> normal
        if b["key"] == CONF.ALG_UI.SELECTED_ALGORITHM:
            color = CONF.ALG_UI.BUTTON_ACTIVE
        else:
            color = CONF.ALG_UI.BUTTON_HOVER if hovered else CONF.ALG_UI.BUTTON_COLOR
        label = CONF.ALG_UI.PARSING_BUTTONS.get(str(b["key"]), str(b["key"]))
        pygame.draw.rect(surface, color, rect, border_radius=6)
        txt = CONF.ALG_UI.FONT.render(label, True, CONF.ALG_UI.TEXT_COLOR)
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
        CONF.ALG_UI.TITLE_FONT = pygame.font.SysFont(title_font_name, title_size, bold=True)
    except Exception:
        CONF.ALG_UI.TITLE_FONT = pygame.font.Font(None, title_size)
        try:
            CONF.ALG_UI.TITLE_FONT.set_bold(True)
        except Exception:
            pass

    try:
        CONF.ALG_UI.FONT = pygame.font.SysFont(font_name, font_size, bold=False)
    except Exception:
        CONF.ALG_UI.FONT = pygame.font.Font(None, font_size)