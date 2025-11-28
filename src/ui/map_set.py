import pygame
from typing import Any, List
from data.map_enemies import MAP_ENEMIES_DATA
from configs.package import CONF

class MapSet:
    """
    Descripción
        CLASE: Gestiona la interfaz de selección y carga de niveles del juego.

    Atributos
        - game_instance (Any): Instancia principal del juego que provee load_level().
        - entity_manager (Any): Gestor de entidades usado para crear enemigos/recursos.
    
    Métodos y Funciones
        - handle_event: Maneja eventos de Pygame relacionados con la UI de niveles.
        - draw: Dibuja el panel de selección de niveles en pantalla.
        - _build_buttons: Construye los rectángulos para los botones del panel.
    
    Propósito
        - Ofrecer una UI lateral para seleccionar niveles y disparar la carga correspondiente
          en la instancia principal del juego.
    """
    def __init__(self, game_instance: Any, entity_manager: Any) -> None:
        # 1. Guardar referencias a la instancia principal del juego y al EntityManager
        self.game_instance = game_instance
        self.entity_manager = entity_manager

        # 2. Construir los botones iniciales del panel
        self._build_buttons()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Descripción
            MÉTODO: Maneja un evento de Pygame. Procesa clics en los botones del panel
            y solicita la carga del nivel seleccionado.

        Argumentos
            - event (pygame.event.Event) : Evento recibido desde la cola de eventos.

        Retorno
            - bool: True si el evento fue consumido por la UI, False en caso contrario.
        """
        # 1. Procesar únicamente clics con botón izquierdo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # 2. Iterar los botones configurados y comprobar colisión con el cursor
            for b in CONF.MAP_UI.BUTTONS:
                if b["rect"].collidepoint((mx, my)):
                    # 3. Actualizar selección y solicitar carga del nivel a la instancia del juego
                    CONF.MAP_UI.SELECTED = b["key"]
                    # 3.1 Llamar al método público de la instancia para cargar el nivel
                    self.game_instance.load_level(b["key"], b["key"], "map")
                    return True  # Evento manejado por la UI

        # 4. Si no fue manejado, retornar False
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Descripción
            MÉTODO: Dibuja el panel de selección de niveles en la superficie proporcionada.

        Argumentos
            - surface (pygame.Surface) : Superficie destino donde dibujar la UI.

        Retorno
            - Ninguno
        """
        # 1. Calcular dimensiones del panel y rectángulo base
        ui_width = CONF.MAP_UI.PANEL_WIDTH
        ui_height = surface.get_height()
        panel_rect = pygame.Rect(0, 0, ui_width, ui_height)

        # 2. Dibujar fondo semitransparente del panel
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        s.fill(CONF.MAP_UI.BG_COLOR)
        surface.blit(s, (panel_rect.x, panel_rect.y))

        # 3. Dibujar título del panel
        title_surf = CONF.MAP_UI.TITLE_FONT.render(CONF.MAP_UI.TITLE, True, CONF.MAP_UI.TITLE_COLOR)
        surface.blit(title_surf, (CONF.MAP_UI.PADDING, CONF.MAP_UI.PADDING))

        # 4. Dibujar botones con estado hovered / active
        mx, my = pygame.mouse.get_pos()
        for b in CONF.MAP_UI.BUTTONS:
            rect = b["rect"]
            hovered = rect.collidepoint((mx, my))

            # 4.1 Seleccionar color según estado
            if b["key"] == CONF.MAP_UI.SELECTED:
                color = CONF.MAP_UI.BUTTON_ACTIVE
            else:
                color = CONF.MAP_UI.BUTTON_HOVER if hovered else CONF.MAP_UI.BUTTON_COLOR

            # 4.2 Obtener etiqueta y dibujar botón
            label = CONF.MAP_UI.PARSING_BUTTONS.get(str(b["key"]), str(b["key"]))
            pygame.draw.rect(surface, color, rect, border_radius=6)
            txt = CONF.MAP_UI.FONT.render(label, True, CONF.MAP_UI.TEXT_COLOR)
            tx = rect.x + 12
            ty = rect.y + (rect.height - txt.get_height()) // 2
            surface.blit(txt, (tx, ty))

    def _build_buttons(self) -> None:
        """
        Descripción
            MÉTODO: Construye la lista de rectángulos para los botones de selección de nivel.

        Argumentos
            - Ninguno

        Retorno
            - Ninguno
        """
        # 1. Obtener las claves disponibles desde los datos de configuración de niveles
        button_keys: List[str] = list(MAP_ENEMIES_DATA.keys())

        # 2. Reiniciar la lista de botones en la configuración compartida
        CONF.MAP.UI = getattr(CONF, "MAP", getattr(CONF, "MAP", CONF))  # asegurar que MAP exista (silencioso)
        CONF.MAP_UI.BUTTONS.clear()

        # 3. Calcular posición inicial y construir rect para cada botón
        y = CONF.MAP_UI.PADDING + 48
        for k in button_keys:
            rect = pygame.Rect(
                CONF.MAP_UI.PADDING,
                y,
                CONF.MAP_UI.PANEL_WIDTH - CONF.MAP_UI.PADDING * 2,
                CONF.MAP_UI.BUTTON_HEIGHT,
            )
            CONF.MAP_UI.BUTTONS.append({"key": k, "rect": rect})
            y += CONF.MAP_UI.BUTTON_HEIGHT + 8