import math
import pygame
from kinematics.kinematic import Kinematic, SteeringOutput
from kinematics.kinematic_arrive import KinematicArrive
from kinematics.kinematic_seek import KinematicSeek
from kinematics.kinematic_wandering import KinematicWander
from characters.animation import Animation, load_animations, set_animation_state
from utils.configs import *

class Enemy(Kinematic):
    """
    Clase que representa un enemigo que persigue al jugador.
    Utiliza el algoritmo KinematicArrive para moverse suavemente hacia el objetivo.
    Atributos:
        type: tipo de enemigo (puede usarse para diferentes sprites o comportamientos)
        position: posición inicial del enemigo (x, y)
        target: referencia al objeto target (objetivo a seguir)
        algorithm: algoritmo de búsqueda cinemática ("ARRIVE" o "SEEK")
        maxSpeed: velocidad máxima del enemigo
        target_radius: radio de llegada al objetivo
        slow_radius: radio de desaceleración
        time_to_target: tiempo para alcanzar el objetivo
    """
    def __init__(
        self, 
        type: str, 
        position: tuple, 
        target: Kinematic, 
        algorithm: str, 
        maxSpeed: float = 200.0, 
        target_radius: float = 40.0, 
        slow_radius: float = 150.0, 
        time_to_target: float = 0.15,
        max_rotation: float = 1.0
    ) -> None:
        super().__init__(
            position=position, 
            orientation=0.0, 
            velocity=(0,0), 
            rotation=0.0
        )
        self.type = type
        self.target = target
        self.algorithm = algorithm
        self.maxSpeed = maxSpeed

        # Instanciar atributos de animación
        self.state = ENEMY_STATES.MOVE
        self.animations : dict[str, Animation] = load_animations(
            ENEMY, 
            self.type, 
            ENEMY_STATES, 
            ENEMY_TILE_WIDTH, 
            ENEMY_TILE_HEIGHT,
            frame_duration=0.12,
            scale=1.25
        )
        self.current_animation : Animation = self.animations[self.state]
        self.collider_box = ENEMY_COLLIDER_BOX

        # Instanciar el algoritmo de búsqueda cinemática: Seek
        self.seek = KinematicSeek(
            character=self,
            target=target,
            max_speed=maxSpeed
        )

        # Instanciar el algoritmo de búsqueda cinemática: Arrive
        self.arrive = KinematicArrive(
            character=self,
            target=target,
            max_speed=maxSpeed,
            target_radius=target_radius,     # Radio de llegada
            slow_radius=slow_radius,         # Radio para empezar a desacelerar
            time_to_target=time_to_target,   # Tiempo para ajustar la velocidad
        )
        
        # Instanciar el algoritmo de vagar: Wander
        self.wander = KinematicWander(
            character=self,
            max_speed=maxSpeed,
            max_rotation=max_rotation
        )

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float):
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
            # Mostrar arriba del sprite el algoritmo activo en VERDE, NEGRITA y MAYÚSCULAS
            # Cachear la fuente en la clase para no recrearla cada frame
            if not hasattr(self.__class__, "_dev_font") or self.__class__._dev_font is None:
                try:
                    self.__class__._dev_font = pygame.font.SysFont(None, 18, bold=True)
                except Exception:
                    # Fallback si SysFont falla
                    self.__class__._dev_font = pygame.font.Font(None, 18)
                    self.__class__._dev_font.set_bold(True)

            font = self.__class__._dev_font
            # self.algorithm puede ser un Enum o string; obtener representación en mayúsculas
            alg_text = (
                self.algorithm.value.upper()
                if hasattr(self.algorithm, "value")
                else str(self.algorithm).upper()
            )
            text_surf = font.render(alg_text, True, (0, 255, 0))
            # Posicionar el texto justo encima del sprite (ajustar offset si es necesario)
            text_rect = text_surf.get_rect(center=(sx, sz - rect.height // 2))
            surface.blit(text_surf, text_rect)

            self.draw_collision_box(surface, camera_x, camera_z)

    def draw_collision_box(self, surface: pygame.Surface, camera_x: float, camera_z: float):
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

    def update(self, surface: pygame.Surface, camera_x: float, camera_z: float, collision_rects: list[pygame.Rect], dt: float):
        """
        Actualiza la posición, velocidad y orientación del enemigo para perseguir al jugador.
        Utiliza el algoritmo de movimiento especificado en "algorithm" para calcular el steering adecuado.
        """
        # Calcular el steering según el algoritmo seleccionado
        steering: SteeringOutput = SteeringOutput((0, 0), 0.0)
        if self.algorithm == ALGORITHM.ARRIVE:
            steering = self.arrive.get_steering()
        elif self.algorithm == ALGORITHM.SEEK:
            steering = self.seek.get_steering()
        elif self.algorithm == ALGORITHM.WANDER:
            steering = self.wander.get_steering()

        # Aplicar el steering y actualizar la cinemática
        if steering.linear != (0, 0):
            set_animation_state(self, ENEMY_STATES.MOVE)
            self.updateKinematic(steering, self.maxSpeed, dt, collision_rects)
        else:
            set_animation_state(self, ENEMY_STATES.ATTACK)

        self.current_animation.update(dt)      # Actualizar animación
        self.draw(surface, camera_x, camera_z) # Dibujar enemigo