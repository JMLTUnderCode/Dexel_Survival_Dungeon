import pygame
from typing import Tuple

class UIButton:
    """
    Descripción
        CLASE: Representa un botón de la interfaz con efecto de hover (escalado).

    Atributos
        - image (pygame.Surface): Imagen base del botón.
        - rect (pygame.Rect): Rectángulo de colisión y posición base.
        - hover_scale (float): Factor de escala al pasar el mouse (ej. 1.05).
        - is_hovered (bool): Estado actual del hover.

    Métodos y Funciones
        - draw: Dibuja el botón aplicando el efecto de escala si es necesario.
        - handle_event: Verifica si se hizo clic en el botón.
        - update: Actualiza el estado de hover basado en la posición del mouse.

    Propósito
        - Proveer un elemento interactivo estándar para el menú.
    """
    def __init__(self, image: pygame.Surface, center_pos: Tuple[int, int], hover_scale: float = 1.05) -> None:
        """{SIN DOCSTRING PARA __init__}"""
        # 1. Guardar imagen original y crear rectángulo centrado
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.hover_scale = hover_scale
        self.is_hovered = False
        
        # 2. Pre-calcular imagen escalada para rendimiento
        w = int(self.rect.width * self.hover_scale)
        h = int(self.rect.height * self.hover_scale)
        self.hover_image = pygame.transform.smoothscale(self.image, (w, h))
        self.hover_rect = self.hover_image.get_rect(center=center_pos)

    def update(self, mouse_pos: Tuple[int, int], audio_manager) -> None:
        """
        Descripción
            MÉTODO: Actualiza el estado interno (hover) según la posición del mouse.

        Argumentos
            - mouse_pos (Tuple[int, int]) : Coordenadas (x, y) del mouse.
        """
        curr = self.is_hovered
        # 1. Verificar colisiónaudio_manager.play_sfx("hover")
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if (curr == False) and (self.is_hovered == True):
            audio_manager.play_sfx("hover")
        elif (curr == True) and (self.is_hovered == False):
            audio_manager.stop_sfx("hover")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Descripción
            MÉTODO: Dibuja el botón en la superficie.

        Argumentos
            - surface (pygame.Surface) : Superficie de destino.
        """
        # 1. Dibujar la versión escalada o normal según el estado
        if self.is_hovered:
            surface.blit(self.hover_image, self.hover_rect)
        else:
            surface.blit(self.image, self.rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Descripción
            MÉTODO: Detecta si el botón fue presionado.

        Argumentos
            - event (pygame.event.Event) : Evento de Pygame.

        Retorno
            - bool: True si se hizo clic izquierdo sobre el botón.
        """
        # 1. Verificar clic izquierdo y colisión
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

class UIIconToggle:
    """
    Descripción
        CLASE: Representa un icono que alterna entre dos estados (ej. Sonido On/Off).

    Atributos
        - image_on (pygame.Surface): Imagen para el estado activo.
        - image_off (pygame.Surface): Imagen para el estado inactivo.
        - rect (pygame.Rect): Rectángulo de posición.
        - state (bool): Estado actual (True=On, False=Off).

    Métodos y Funciones
        - draw: Dibuja el icono correspondiente al estado.
        - handle_event: Alterna el estado al hacer clic.

    Propósito
        - Controlar configuraciones binarias rápidas en la UI.
    """
    def __init__(self, img_on: pygame.Surface, img_off: pygame.Surface, top_right_pos: Tuple[int, int]) -> None:
        """{SIN DOCSTRING PARA __init__}"""
        # 1. Configurar imágenes y posición (alineado a la esquina superior derecha)
        self.image_on = img_on
        self.image_off = img_off
        self.state = True # Default ON
        
        # Usamos el rect de la imagen ON como referencia
        self.rect = self.image_on.get_rect(topright=top_right_pos)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Descripción
            MÉTODO: Dibuja el icono actual.

        Argumentos
            - surface (pygame.Surface) : Superficie de destino.
        """
        # 1. Seleccionar imagen según estado
        img = self.image_on if self.state else self.image_off
        surface.blit(img, self.rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Descripción
            MÉTODO: Gestiona el clic para alternar estado.

        Argumentos
            - event (pygame.event.Event) : Evento de Pygame.

        Retorno
            - bool: True si el estado cambió.
        """
        # 1. Verificar clic
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                return True
        return False

class UISlider:
    """
    Descripción
        CLASE: Barra deslizante horizontal para controlar valores numéricos (0.0 a 1.0).
        Utilizada para control de volumen.

    Atributos
        - rect (pygame.Rect): Área total de la barra.
        - knob_rect (pygame.Rect): Área del indicador móvil (perilla).
        - value (float): Valor actual entre 0.0 y 1.0.
        - dragging (bool): Indica si el usuario está arrastrando la perilla.
        - color_bg (tuple): Color de fondo de la barra.
        - color_fill (tuple): Color de la parte llena de la barra.
        - color_knob (tuple): Color de la perilla.

    Métodos y Funciones
        - draw: Renderiza la barra y la perilla.
        - handle_event: Gestiona clics y arrastre del mouse.
        - get_value: Retorna el valor actual.

    Propósito
        - Permitir al usuario ajustar configuraciones continuas como el volumen.
    """
    def __init__(self, center_pos: Tuple[int, int], width: int, initial_value: float) -> None:
        """{SIN DOCSTRING PARA __init__}"""
        # 1. Configurar dimensiones
        height = 10
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center_pos
        
        # 2. Configurar valor inicial y estado
        self.value = max(0.0, min(1.0, initial_value))
        self.dragging = False
        
        # 3. Configurar perilla (knob)
        knob_size = 20
        self.knob_rect = pygame.Rect(0, 0, knob_size, knob_size)
        self._update_knob_position()

        # 4. Colores (Hardcoded por ahora, podrían ir a config)
        self.color_bg = (100, 100, 100)
        self.color_fill = (200, 200, 200)
        self.color_knob = (255, 255, 255)

    def _update_knob_position(self) -> None:
        """
        Descripción
            MÉTODO PRIVADO: Actualiza la posición visual de la perilla basada en self.value.
        """
        # 1. Calcular posición X relativa al ancho
        x = self.rect.x + (self.rect.width * self.value)
        self.knob_rect.centerx = int(x)
        self.knob_rect.centery = self.rect.centery

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Descripción
            MÉTODO: Procesa eventos de mouse para ajustar el valor.

        Argumentos
            - event (pygame.event.Event): Evento de Pygame.

        Retorno
            - bool: True si el valor cambió, False en caso contrario.
        """
        change = False
        
        # 1. Iniciar arrastre
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.knob_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value_from_mouse(event.pos[0])
                change = True

        # 2. Terminar arrastre
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        # 3. Mover arrastre
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value_from_mouse(event.pos[0])
                change = True
                
        return change

    def _update_value_from_mouse(self, mouse_x: int) -> None:
        """
        Descripción
            MÉTODO PRIVADO: Calcula el valor (0.0-1.0) basado en la posición X del mouse.
        """
        # 1. Calcular proporción
        relative_x = mouse_x - self.rect.x
        val = relative_x / self.rect.width
        
        # 2. Clampar y actualizar
        self.value = max(0.0, min(1.0, val))
        self._update_knob_position()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Descripción
            MÉTODO: Dibuja el slider en la pantalla.

        Argumentos
            - surface (pygame.Surface): Superficie de destino.
        """
        # 1. Dibujar fondo (barra vacía)
        pygame.draw.rect(surface, self.color_bg, self.rect, border_radius=5)
        
        # 2. Dibujar relleno (barra llena hasta el valor)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.width * self.value), self.rect.height)
        pygame.draw.rect(surface, self.color_fill, fill_rect, border_radius=5)
        
        # 3. Dibujar perilla
        pygame.draw.rect(surface, self.color_knob, self.knob_rect, border_radius=10)

    def get_value(self) -> float:
        """
        Descripción
            MÉTODO: Obtiene el valor actual del slider.

        Retorno
            - float: Valor entre 0.0 y 1.0.
        """
        return self.value