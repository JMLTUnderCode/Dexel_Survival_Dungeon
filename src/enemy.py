import os
import pygame
import math
from kinematic import Kinematic
from kinematic_arrive import KinematicArrive
from resource_path import resource_path
from animation import Animation
from configs import *

class Enemy(Kinematic):
    """
    Clase que representa un enemigo que persigue al jugador.
    Utiliza el algoritmo KinematicArrive para moverse suavemente hacia el objetivo.
    Atributos:
        type: tipo de enemigo (puede usarse para diferentes sprites o comportamientos)
        position: posición inicial del enemigo (x, y)
        target: referencia al objeto target (objetivo a seguir)
        maxSpeed: velocidad máxima del enemigo
        map_width, map_height: dimensiones del mapa para clamp
        collision_rects: lista de rectángulos para detección de colisiones
    """
    def __init__(self, type, position, target, maxSpeed=180):
        super().__init__(position=position, orientation=0.0, velocity=(0,0), rotation=0.0)
        self.type = type
        self.target = target
        self.maxSpeed = maxSpeed

        self.state = ENEMY_STATES.MOVE
        self.animations : dict[str, Animation] = self.load_animations()
        if "move" not in self.animations:
            raise RuntimeError(f"No se encontró la animación 'move' para el enemigo '{self.type}'. Verifica que exista el archivo 'src/assets/enemies/{self.type}-move.png'.")
        self.current_animation : Animation = self.animations[self.state]
        self.collider_box = ENEMY_COLLIDER_BOX

        # Instanciar el algoritmo de llegada cinemática
        self.arrive = KinematicArrive(
            character=self,
            target=target,
            max_speed=self.maxSpeed,
            target_radius=40,    # Radio de llegada
            slow_radius=150,     # Radio para empezar a desacelerar
            time_to_target=0.15, # Tiempo para ajustar la velocidad
            max_accel=300        # Aceleración máxima
        )

    def load_animations(self):
        """
        Carga las animaciones del enemigo desde archivos PNG.
        Retorna un diccionario con las animaciones cargadas.
        Cada animación se espera que esté en un archivo con el formato:
        """
        base = os.path.join("assets", "enemies")
        anims = {}
        frame_duration = 0.12
        w_tile = ENEMY_TILE_WIDTH
        h_tile = ENEMY_TILE_HEIGHT
        scale = 1.25
        scale_to = (int(w_tile * scale), int(h_tile * scale))
        # Ajustar los frame_count y frame_duration según cada animación
        for state in ENEMY_STATES:
            state_value = state.value
            filename = f"{self.type}-{state_value}.png"
            path = resource_path(os.path.join(base, filename))
            if os.path.exists(path):
                img = pygame.image.load(path)
                frame_count = img.get_width() // w_tile
                if state_value == ENEMY_STATES.ATTACK:
                    frame_duration = 0.15  # Ajuste específico para "attack"
                anims[state_value] = Animation(path, w_tile, h_tile, frame_count, frame_duration, scale_to=scale_to)
            else:
                raise RuntimeError(f"No se encontró la animación '{state}' para el enemigo '{self.type}'. Verifica que exista el archivo 'src/assets/enemies/{self.type}-{state}.png'.")
        return anims

    def set_state(self, state):
        """
        Cambia el estado actual del enemigo y reinicia la animación correspondiente.
        Si el estado no existe en las animaciones cargadas, lanza un error.
        """
        if state != self.state and state in self.animations:
            self.state = state
            self.current_animation = self.animations[state]
            self.current_animation.current_frame = 0
            self.current_animation.time_acc = 0
        if state not in self.animations:
            raise RuntimeError(f"No se encontró la animación '{state}' para el enemigo '{self.type}'. Verifica que exista el archivo 'src/assets/enemies/{self.type}-{state}.png'.")

    def draw(self, surface, camera_x, camera_z):
        """
        Dibuja el enemigo en pantalla, rotando el sprite hacia el jugador.
        La posición se ajusta por la cámara para renderizar correctamente en el viewport.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        deg = -math.degrees(self.orientation) - 90
        frame = self.current_animation.get_frame()
        rotated = pygame.transform.rotate(frame, deg)
        rect = rotated.get_rect(center=(sx, sz))
        surface.blit(rotated, rect)

        if DEVELOPMENT:
            self.draw_collision_box(surface, camera_x, camera_z)
            
    def draw_collision_box(self, surface, camera_x, camera_z):
        """
        Dibuja el cuadro de colisión del enemigo para depuración.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        enemy_box = pygame.Rect(
            int(sx - self.collider_box // 2),
            int(sz - self.collider_box // 2),
            int(self.collider_box),
            int(self.collider_box)
        )
        pygame.draw.rect(surface, (0, 255, 0), enemy_box, 1)  # Verde, grosor 1

    def update(self, surface, camera_x, camera_z, collision_rects , dt):
        """
        Actualiza la posición, velocidad y orientación del enemigo para perseguir al jugador.
        Utiliza el algoritmo KinematicArrive para calcular el steering adecuado.
        """
        if self.state.startswith(ENEMY_STATES.DEATH_0):
            pass
        # Calcular vector y distancia al objetivo
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        dist = math.hypot(dx, dy)
        # Orientar el sprite hacia el jugador
        self.orientation = math.atan2(dy, dx)
        # Si está dentro del radio objetivo, detenerse completamente
        if dist < self.arrive.target_radius:
            self.set_state(ENEMY_STATES.ATTACK)
            self.velocity = (0, 0)
        else:
            self.set_state(ENEMY_STATES.MOVE)
            # Calcular y aplicar el steering usando KinematicArrive
            steering = self.arrive.get_steering(dx, dy, dist)
            self.updateKinematic(steering, self.maxSpeed, dt, collision_rects)
        self.current_animation.update(dt)

        self.draw(surface, camera_x, camera_z)