import pygame
from typing import Tuple

class FloatingText:
    """
    Descripción
        CLASE: Representa un efecto visual de texto flotante (burbuja de daño)
        que aparece en una posición y se desplaza hacia arriba mientras se desvanece.

    Atributos
        - position (list[float, float]): Posición actual (x, z) en el mundo.
        - text (str): Texto a mostrar (ej. "-15").
        - lifetime (float): Tiempo de vida restante en segundos.
        - max_lifetime (float): Duración total del efecto.
        - speed (float): Velocidad de ascenso en px/s.
        - font (pygame.font.Font): Fuente para renderizar el texto.
        - color (tuple): Color del texto (RGB).

    Métodos y Funciones
        - update(dt): Actualiza la posición y el tiempo de vida.
        - draw(surface, cx, cz): Dibuja el texto en pantalla relativo a la cámara.
        - is_alive(): Retorna True si el efecto aún debe existir.

    Propósito
        - Proporcionar feedback visual inmediato al jugador sobre el daño infligido/recibido.
    """
    def __init__(self, position: Tuple[float, float], value: int) -> None:
        # 1. Inicializar posición y valor
        self.position = [float(position[0]), float(position[1])]
        self.text = f"-{int(value)}"
        
        # 2. Configuración de movimiento y vida
        self.max_lifetime = 1.0  # Duración de 1 segundo
        self.lifetime = self.max_lifetime
        distance_to_travel = 64.0 # Desplazamiento total hacia arriba
        self.speed = distance_to_travel / self.max_lifetime
        
        # 3. Configuración visual
        # Usamos SysFont por simplicidad, idealmente cargar desde recursos
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.color = (255, 255, 255) # Blanco

    def update(self, dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la física del texto flotante.

        Argumentos
            - dt (float): Delta time en segundos.
        """
        # 1. Reducir tiempo de vida
        self.lifetime -= dt

        # 2. Mover hacia arriba (en coordenadas de mundo, Z disminuye hacia "arriba" visualmente en top-down 2D)
        # Nota: Dependiendo del sistema de coordenadas, restar a Y/Z mueve hacia arriba en pantalla.
        self.position[1] -= self.speed * dt

    def is_alive(self) -> bool:
        """
        Descripción
            MÉTODO: Verifica si el efecto sigue activo.

        Retorno
            - bool: True si lifetime > 0.
        """
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Renderiza el texto en la superficie de juego.

        Argumentos
            - surface (pygame.Surface): Superficie destino.
            - camera_x (float): Posición X de la cámara.
            - camera_z (float): Posición Z de la cámara.
        """
        if not self.is_alive():
            return

        # 1. Renderizar texto
        text_surf = self.font.render(self.text, True, self.color)
        
        # 2. Calcular posición en pantalla
        screen_x = self.position[0] - camera_x
        screen_y = self.position[1] - camera_z
        
        # 3. Centrar y dibujar
        rect = text_surf.get_rect(center=(screen_x, screen_y))
        surface.blit(text_surf, rect)