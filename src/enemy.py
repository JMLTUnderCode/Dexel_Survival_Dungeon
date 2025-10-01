import os
import pygame
import math
from kinematic import Kinematic
from kinematic_arrive import KinematicArrive

class Enemy(Kinematic):
    """
    Clase Enemy: NPC que persigue al jugador usando el algoritmo KinematicArrive.
    Utiliza el mismo sprite que el jugador y se mueve de forma suave y natural por el mapa.
    """
    def __init__(self, position, player, maxSpeed=180, map_width=800, map_height=600):
        """
        position: posición inicial del enemigo (x, y)
        player: referencia al objeto Player (objetivo a seguir)
        maxSpeed: velocidad máxima del enemigo
        map_width, map_height: dimensiones del mapa para clamp
        """
        super().__init__(position=position, orientation=0.0, velocity=(0,0), rotation=0.0, map_width=map_width, map_height=map_height)
        self.maxSpeed = maxSpeed
        self.player = player  # Referencia al objetivo
        # Cargar el mismo sprite que el jugador y escalarlo
        knight_img_path = os.path.join(os.path.dirname(__file__), "knight", "Knight.png")
        sprite_raw = pygame.image.load(knight_img_path).convert_alpha()
        self.sprite = pygame.transform.scale(sprite_raw, (sprite_raw.get_width()*1.5, sprite_raw.get_height()*1.5))
        self.size = self.sprite.get_width()
        # Instanciar el algoritmo de llegada cinemática
        self.arrive = KinematicArrive(
            character=self,
            target=player,
            max_speed=self.maxSpeed,
            target_radius=40,    # Radio de llegada
            slow_radius=150,     # Radio para empezar a desacelerar
            time_to_target=0.15, # Tiempo para ajustar la velocidad
            max_accel=300        # Aceleración máxima
        )

    def update(self, dt):
        """
        Actualiza la posición, velocidad y orientación del enemigo para perseguir al jugador.
        Utiliza el algoritmo KinematicArrive para calcular el steering adecuado.
        """
        # Calcular vector y distancia al objetivo
        dx = self.player.position[0] - self.position[0]
        dy = self.player.position[1] - self.position[1]
        dist = math.hypot(dx, dy)
        # Orientar el sprite hacia el jugador
        self.orientation = math.atan2(dy, dx)
        # Si está dentro del radio objetivo, detenerse completamente
        if dist < self.arrive.target_radius:
            self.velocity = (0, 0)
            return
        # Calcular y aplicar el steering usando KinematicArrive
        steering = self.arrive.get_steering()
        self.updateKinematic(steering, self.maxSpeed, dt)

    def draw(self, surface, camera_x, camera_z):
        """
        Dibuja el enemigo en pantalla, rotando el sprite hacia el jugador.
        La posición se ajusta por la cámara para renderizar correctamente en el viewport.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        deg = -math.degrees(self.orientation) - 90
        rotated = pygame.transform.rotate(self.sprite, deg)
        rect = rotated.get_rect(center=(sx, sz))
        surface.blit(rotated, rect)