import pygame
from data.enemies import map_levels_enemies_data
from configs.package import CONF

class MapSet:
    """
    Gestiona la interfaz de usuario para seleccionar y cargar los niveles del juego.
    
    Se encarga de dibujar los botones de selección de nivel y de invocar la
    lógica de carga de nivel en la clase principal del juego.
    """
    def __init__(self, game_instance, entity_manager):
        """
        Inicializa la UI de selección de nivel.
        
        Args:
            game_instance: La instancia principal de la clase Game.
            entity_manager: El gestor de entidades del juego.
        """
        self.game_instance = game_instance
        self.entity_manager = entity_manager
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
            for b in CONF.MAP_UI.BUTTONS:
                if b["rect"].collidepoint((mx, my)):
                    CONF.MAP_UI.SELECTED = b["key"]
                    self.game_instance.load_level(b["key"], b["key"], "map")
                    return True  # Evento manejado
        return False  # Evento no manejado

    def draw(self, surface: pygame.Surface):
        """Dibuja el panel completo de la UI en la superficie dada."""
        ui_width = CONF.MAP_UI.PANEL_WIDTH
        ui_height = surface.get_height()

        # Panel con fondo semitransparente
        panel_rect = pygame.Rect(0, 0, ui_width, ui_height)
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        s.fill(CONF.MAP_UI.BG_COLOR)
        surface.blit(s, (panel_rect.x, panel_rect.y))

        # Título
        title_surf = CONF.MAP_UI.TITLE_FONT.render(CONF.MAP_UI.TITLE, True, CONF.MAP_UI.TITLE_COLOR)
        surface.blit(title_surf, (CONF.MAP_UI.PADDING, CONF.MAP_UI.PADDING))

        # Botones
        mx, my = pygame.mouse.get_pos()
        for b in CONF.MAP_UI.BUTTONS:
            rect = b["rect"]
            hovered = rect.collidepoint((mx, my))
            
            if b["key"] == CONF.MAP_UI.SELECTED:
                color = CONF.MAP_UI.BUTTON_ACTIVE
            else:
                color = CONF.MAP_UI.BUTTON_HOVER if hovered else CONF.MAP_UI.BUTTON_COLOR
            
            label = CONF.MAP_UI.PARSING_BUTTONS.get(str(b["key"]), str(b["key"]))
            pygame.draw.rect(surface, color, rect, border_radius=6)
            txt = CONF.MAP_UI.FONT.render(label, True, CONF.MAP_UI.TEXT_COLOR)
            tx = rect.x + 12
            ty = rect.y + (rect.height - txt.get_height()) // 2
            surface.blit(txt, (tx, ty))

    def _build_buttons(self):
        """Construye la lista de rectángulos para los botones de la UI."""
        button_keys = list(map_levels_enemies_data.keys())
        CONF.MAP_UI.BUTTONS.clear()
        y = CONF.MAP_UI.PADDING + 48
        for k in button_keys:
            rect = pygame.Rect(CONF.MAP_UI.PADDING, y, CONF.MAP_UI.PANEL_WIDTH - CONF.MAP_UI.PADDING*2, CONF.MAP_UI.BUTTON_HEIGHT)
            CONF.MAP_UI.BUTTONS.append({"key": k, "rect": rect})
            y += CONF.MAP_UI.BUTTON_HEIGHT + 8