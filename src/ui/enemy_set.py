import pygame
from typing import List
from entity.entity_manager import EntityManager
from data.algorithm_enemies import ALGORITHM_ENEMIES_DATA
from configs.package import CONF

class EnemySet:
    """
    Descripción
        CLASE: Gestiona la interfaz de usuario para seleccionar y mostrar conjuntos de enemigos.

    Atributos
        - entity_manager (EntityManager): referencia al gestor de entidades del juego.
        - _buttons (List[dict]): lista interna de descriptores de botones (clave y rect).
    
    Métodos y Funciones
        - handle_event: Maneja eventos de Pygame relacionados con la UI.
        - draw: Dibuja el panel de selección en la superficie provista.
        - _build_buttons: Construye la lista de rectángulos para los botones de la UI.
    
    Propósito
        - Permitir al usuario seleccionar conjuntos de enemigos (algoritmos) desde un panel lateral
          y recrear la escena mediante el EntityManager.
    """
    def __init__(self, entity_manager: EntityManager) -> None:
        # 1. Guardar la referencia al EntityManager para poder crear grupos al seleccionar botones
        self.entity_manager: EntityManager = entity_manager

        # 2. Construir la lista de botones a partir de los datos de enemigos por algoritmo
        self._build_buttons()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Descripción
            MÉTODO: Maneja un evento de Pygame. Si el evento corresponde a un clic en un botón
            del panel, actualiza la selección y recrea el grupo de enemigos.

        Argumentos
            - event (pygame.event.Event) : Evento recibido desde la cola de eventos.

        Retorno
            - bool: True si el evento fue consumido por la UI, False si no.
        """
        # 1. Procesar solo clics de botón izquierdo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # 2. Iterar botones definidos en la configuración y comprobar colisión con el cursor
            for b in CONF.ALG_UI.BUTTONS:
                if b["rect"].collidepoint((mx, my)):
                    # 3. Actualizar selección global y reconstruir enemigos usando EntityManager
                    CONF.ALG_UI.SELECTED = b["key"]
                    self.entity_manager.create_enemy_group(b["key"], "alg")
                    return True  # Evento manejado por la UI

        # 4. Evento no relacionado con la UI
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Descripción
            MÉTODO: Dibuja el panel completo de la UI en la superficie indicada.

        Argumentos
            - surface (pygame.Surface) : Superficie destino donde dibujar la UI.

        Retorno
            - Ninguno
        """
        # 1. Parámetros y rectángulo del panel
        ui_width = CONF.ALG_UI.PANEL_WIDTH
        ui_height = surface.get_height()
        panel_rect = pygame.Rect(0, 0, ui_width, ui_height)

        # 2. Dibujar fondo semitransparente del panel
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        s.fill(CONF.ALG_UI.BG_COLOR)
        surface.blit(s, (panel_rect.x, panel_rect.y))

        # 3. Dibujar título del panel
        title_surf = CONF.ALG_UI.TITLE_FONT.render(CONF.ALG_UI.TITLE, True, CONF.ALG_UI.TITLE_COLOR)
        surface.blit(title_surf, (CONF.ALG_UI.PADDING, CONF.ALG_UI.PADDING))

        # 4. Dibujar botones interactivos con estado hovered/active
        mx, my = pygame.mouse.get_pos()
        for b in CONF.ALG_UI.BUTTONS:
            rect = b["rect"]
            hovered = rect.collidepoint((mx, my))

            # 4.1 Seleccionar color según estado (activo / hover / normal)
            if b["key"] == CONF.ALG_UI.SELECTED:
                color = CONF.ALG_UI.BUTTON_ACTIVE
            else:
                color = CONF.ALG_UI.BUTTON_HOVER if hovered else CONF.ALG_UI.BUTTON_COLOR

            # 4.2 Etiqueta del botón (resolver mapeo de parsing si existe)
            label = CONF.ALG_UI.PARSING_BUTTONS.get(str(b["key"]), str(b["key"]))

            # 4.3 Dibujar rectángulo del botón y renderizar texto alineado
            pygame.draw.rect(surface, color, rect, border_radius=6)
            txt = CONF.ALG_UI.FONT.render(label, True, CONF.ALG_UI.TEXT_COLOR)
            tx = rect.x + 12
            ty = rect.y + (rect.height - txt.get_height()) // 2
            surface.blit(txt, (tx, ty))

    def _build_buttons(self) -> None:
        """
        Descripción
            MÉTODO: Construye la lista de rectángulos para los botones de la UI basándose en
            las claves definidas en ALGORITHM_ENEMIES_DATA y actualiza CONF.ALG_UI.BUTTONS.

        Argumentos
            - Ninguno

        Retorno
            - Ninguno
        """
        # 1. Obtener las claves disponibles desde los datos de configuración de enemigos
        button_keys: List[str] = list(ALGORITHM_ENEMIES_DATA.keys())

        # 2. Reiniciar la lista de botones en la configuración compartida
        CONF.ALG_UI.BUTTONS.clear()

        # 3. Calcular posición vertical inicial y crear rects para cada clave
        y = CONF.ALG_UI.PADDING + 48
        for k in button_keys:
            rect = pygame.Rect(
                CONF.ALG_UI.PADDING,
                y,
                CONF.ALG_UI.PANEL_WIDTH - CONF.ALG_UI.PADDING * 2,
                CONF.ALG_UI.BUTTON_HEIGHT,
            )
            CONF.ALG_UI.BUTTONS.append({"key": k, "rect": rect})
            y += CONF.ALG_UI.BUTTON_HEIGHT + 8