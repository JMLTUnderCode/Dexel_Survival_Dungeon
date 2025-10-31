import pygame
from data.enemies import list_of_enemies_data
from configs.package import CONF
from helper.entity_manager import EntityManager

class EnemySet:
    """
    Gestiona la interfaz de usuario para seleccionar y mostrar conjuntos de enemigos.
    
    Encapsula la lógica de dibujado, manejo de eventos y estado de la UI del panel
    de algoritmos.
    """
    def __init__(self, entity_manager: EntityManager):
        """
        Inicializa la UI.
        
        Args:
            entity_manager: El gestor de entidades del juego, usado para recrear
                            escenas cuando el usuario selecciona un nuevo conjunto.
        """
        self.entity_manager = entity_manager
        self._init_fonts()
        self._build_buttons()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Maneja un evento de Pygame. Si el evento es un clic en un botón de la UI,
        actualiza el estado del juego y devuelve True.
        
        Returns:
            True si el evento fue manejado por la UI, False en caso contrario.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for b in CONF.ALG_UI.BUTTONS:
                if b["rect"].collidepoint((mx, my)):
                    CONF.ALG_UI.SELECTED = b["key"]
                    self.entity_manager.create_enemy_group(b["key"], "alg")
                    return True  # Evento manejado
        return False  # Evento no manejado

    def draw(self, surface: pygame.Surface):
        """Dibuja el panel completo de la UI en la superficie dada."""
        ui_width = CONF.ALG_UI.PANEL_WIDTH
        ui_height = surface.get_height()

        # Panel con fondo semitransparente
        panel_rect = pygame.Rect(0, 0, ui_width, ui_height)
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        s.fill(CONF.ALG_UI.BG_COLOR)
        surface.blit(s, (panel_rect.x, panel_rect.y))

        # Título
        title_surf = CONF.ALG_UI.TITLE_FONT.render(CONF.ALG_UI.TITLE, True, CONF.ALG_UI.TITLE_COLOR)
        surface.blit(title_surf, (CONF.ALG_UI.PADDING, CONF.ALG_UI.PADDING))

        # Botones
        mx, my = pygame.mouse.get_pos()
        for b in CONF.ALG_UI.BUTTONS:
            rect = b["rect"]
            hovered = rect.collidepoint((mx, my))
            
            if b["key"] == CONF.ALG_UI.SELECTED:
                color = CONF.ALG_UI.BUTTON_ACTIVE
            else:
                color = CONF.ALG_UI.BUTTON_HOVER if hovered else CONF.ALG_UI.BUTTON_COLOR
            
            label = CONF.ALG_UI.PARSING_BUTTONS.get(str(b["key"]), str(b["key"]))
            pygame.draw.rect(surface, color, rect, border_radius=6)
            txt = CONF.ALG_UI.FONT.render(label, True, CONF.ALG_UI.TEXT_COLOR)
            tx = rect.x + 12
            ty = rect.y + (rect.height - txt.get_height()) // 2
            surface.blit(txt, (tx, ty))

    def _build_buttons(self):
        """Construye la lista de rectángulos para los botones de la UI."""
        button_keys = list(list_of_enemies_data.keys())
        CONF.ALG_UI.BUTTONS.clear()
        y = CONF.ALG_UI.PADDING + 48
        for k in button_keys:
            rect = pygame.Rect(CONF.ALG_UI.PADDING, y, CONF.ALG_UI.PANEL_WIDTH - CONF.ALG_UI.PADDING*2, CONF.ALG_UI.BUTTON_HEIGHT)
            CONF.ALG_UI.BUTTONS.append({"key": k, "rect": rect})
            y += CONF.ALG_UI.BUTTON_HEIGHT + 8

    def _init_fonts(self, title_font_name: str = "Segoe UI", title_size: int = 20, font_name: str = "Segoe UI", font_size: int = 16):
        """Inicializa las fuentes usadas por la UI."""
        if not pygame.get_init():
            pygame.init()

        try:
            CONF.ALG_UI.TITLE_FONT = pygame.font.SysFont(title_font_name, title_size, bold=True)
        except Exception:
            CONF.ALG_UI.TITLE_FONT = pygame.font.Font(None, title_size + 4) # Fallback con más tamaño
        
        try:
            CONF.ALG_UI.FONT = pygame.font.SysFont(font_name, font_size, bold=False)
        except Exception:
            CONF.ALG_UI.FONT = pygame.font.Font(None, font_size)