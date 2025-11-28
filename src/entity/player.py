import math
import pygame
from typing import Tuple, List
from entity.kinematic import Kinematic, SteeringOutput
from entity.attack_wave import AttackWave
from entity.animation import Animation, load_animations, set_animation_state
from configs.package import CONF

class Player(Kinematic):
    """
    Descripción
        CLASE: Representa al jugador controlado por el usuario.

    Atributos
        - type (str): Identificador del sprite/tipo del jugador.
        - max_speed (float): Velocidad máxima en píxeles/segundo.
        - attack_waves (List[AttackWave]): Ondas de ataque generadas por el jugador.
        - state (str|Enum): Estado actual usado para seleccionar animación.
        - animations (dict[str, Animation]): Animaciones cargadas por estado.
        - current_animation (Animation): Animación activa actualmente.
        - collider_box (Tuple[int,int]): Dimensiones de la caja de colisión.
        - _pending_steering (SteeringOutput): Steering acumulado hasta el próximo update.

    Métodos y Funciones
        - handle_event: Maneja eventos puntuales (mouse clicks).
        - handle_input: Procesa entrada de teclado + rotación hacia mouse.
        - draw: Dibuja el jugador y sus efectos (ondas, barra de vida).
        - draw_collision_box: Dibuja la caja de colisión (debug).
        - update: Actualiza cinemática, animaciones y limpia ondas.

    Propósito
        - Permitir control directo del jugador mediante teclado y mouse, con animaciones
          y sistema de ondas de ataque simple.
    """
    def __init__(
        self,
        type: str,
        position: Tuple[float, float],
        collider_box: Tuple[int, int],
        max_speed: float = 200.0,
    ) -> None:
        # 1. Inicializar la cinemática base
        super().__init__(position=position, orientation=0.0, velocity=(0.0, 0.0), rotation=0.0)
        # 2. Propiedades visuales y físicas
        self.type: str = type
        self.max_speed: float = float(max_speed)
        self.collider_box: Tuple[int, int] = collider_box
        # 3. Efectos de ataque y estado interno
        self.attack_waves: List[AttackWave] = []
        self._pending_steering: SteeringOutput = SteeringOutput()
        # 4. Estado y animaciones
        self.state = CONF.PLAYER.ACTIONS.IDLE
        self.animations: dict[str, Animation] = load_animations(
            CONF.PLAYER.FOLDER,
            self.type,
            CONF.PLAYER.ACTIONS,
            CONF.PLAYER.TILE_WIDTH,
            CONF.PLAYER.TILE_HEIGHT,
            frame_duration=0.12,
            scale=1.25,
        )
        self.current_animation: Animation = self.animations[self.state]

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Descripción
            MÉTODO: Maneja eventos puntuales como clics de mouse para ataques.

        Argumentos
            - event (pygame.event.Event): Evento recibido desde la cola de eventos.
        """
        # 1. Si se presiona botón izquierdo, iniciar animación de ataque y crear onda
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            set_animation_state(self, CONF.PLAYER.ACTIONS.ATTACK)
            self.attack_waves.append(AttackWave(self.position[0], self.position[1], color=(200, 200, 255)))

    def handle_input(self, camera_x: float, camera_y: float, dt: float) -> None:
        """
        Descripción
            MÉTODO: Procesa la entrada del jugador para movimiento y orientación.

        Argumentos
            - camera_x (float): Coordenada X de la cámara (para cálculo relativo).
            - camera_y (float): Coordenada Y de la cámara (para cálculo relativo).
            - dt (float): Delta time en segundos.
        """
        # 1. Lectura de teclado para determinar aceleración direccional
        keys = pygame.key.get_pressed()
        accel_x, accel_y = 0.0, 0.0
        accel_value = 600.0
        friction = 800.0

        if keys[pygame.K_w]:
            accel_y -= 1.0
        if keys[pygame.K_s]:
            accel_y += 1.0
        if keys[pygame.K_a]:
            accel_x -= 1.0
        if keys[pygame.K_d]:
            accel_x += 1.0

        # 2. Normalizar y escalar aceleración si hay input, o aplicar fricción si no hay
        mag = math.hypot(accel_x, accel_y)
        if mag > 0.0:
            accel_x = accel_x / mag * accel_value
            accel_y = accel_y / mag * accel_value
            set_animation_state(self, CONF.PLAYER.ACTIONS.MOVE)
        else:
            vx, vy = self.velocity
            speed = math.hypot(vx, vy)
            if speed > 0.0:
                fx = -vx / speed * friction
                fy = -vy / speed * friction
                # Si la fricción detendría en este frame, forzar parada
                if abs(fx * dt) >= abs(vx) and abs(fy * dt) >= abs(vy):
                    set_animation_state(self, CONF.PLAYER.ACTIONS.IDLE)
                    self.velocity = (0.0, 0.0)
                    accel_x, accel_y = 0.0, 0.0
                else:
                    accel_x, accel_y = fx, fy

        # 3. Rotación suave hacia la posición del mouse usando PD control
        mx, my = pygame.mouse.get_pos()
        screen_x = self.position[0] - camera_x
        screen_y = self.position[1] - camera_y
        target_angle = math.atan2(my - screen_y, mx - screen_x)
        current_angle = self.orientation
        delta = (target_angle - current_angle + math.pi) % (2 * math.pi) - math.pi

        max_angular_speed = 30.0
        angular_accel = 100.0
        k_p = 16.0
        k_d = 6.0

        desired_rot = max(-max_angular_speed, min(max_angular_speed, k_p * delta - k_d * self.rotation))
        angular = desired_rot - self.rotation
        if abs(angular) > angular_accel:
            angular = math.copysign(angular_accel, angular)

        # 4. Guardar steering calculado para aplicarlo en update()
        self._pending_steering = SteeringOutput(linear=(accel_x, accel_y), angular=angular)

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja el jugador y sus efectos en la superficie indicada.

        Argumentos
            - surface (pygame.Surface): Superficie destino donde dibujar.
            - camera_x (float): Coordenada X de la cámara.
            - camera_z (float): Coordenada Z de la cámara.
        """
        # 1. Calcular posición en pantalla relativa a la cámara
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z

        # 2. Rotar y dibujar el sprite según la orientación actual
        deg = -math.degrees(self.orientation) - 90.0
        frame = self.current_animation.get_frame()
        rotated = pygame.transform.rotate(frame, deg)
        rect = rotated.get_rect(center=(sx, sz))
        surface.blit(rotated, rect)

        # 3. Dibujar ondas de ataque activas
        for wave in self.attack_waves:
            wave.draw(surface, camera_x, camera_z)

        # 4. Dibujar barra de vida
        self.draw_life_bar(surface, camera_x, camera_z)

        # 5. Opciones de debug: cuadro de colisión
        if CONF.DEV.DEBUG and CONF.DEV.COLLISION_RECTS:
            self.draw_collision_box(surface, camera_x, camera_z)

    def draw_collision_box(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja la caja de colisión del jugador para depuración.

        Argumentos
            - surface (pygame.Surface): Superficie destino.
            - camera_x (float): Coordenada X de la cámara.
            - camera_z (float): Coordenada Z de la cámara.
        """
        # 1. Calcular rectángulo centrado en la posición del jugador
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        player_box = pygame.Rect(
            int(sx - self.collider_box[0] // 2),
            int(sz - self.collider_box[1] // 2),
            int(self.collider_box[0]),
            int(self.collider_box[1]),
        )
        # 2. Dibujar rectángulo verde de borde 1
        pygame.draw.rect(surface, (0, 255, 0), player_box, 1)

    def update(self, collision_rects: List[pygame.Rect], dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la cinemática, animaciones y mantiene las ondas de ataque.

        Argumentos
            - collision_rects (List[pygame.Rect]): Rectángulos del mapa usados para colisión.
            - dt (float): Delta time en segundos.
        """
        # 1. Aplicar física dinámica usando el steering calculado previamente
        self.update_by_dynamic(self._pending_steering, self.max_speed, dt, collision_rects, self.collider_box, "PLAYER")
        # 2. Actualizar animación con el delta time
        self.current_animation.update(dt)
        # 3. Actualizar ondas de ataque y limpiar las inactivas
        for wave in self.attack_waves:
            wave.update()
        self.attack_waves = [w for w in self.attack_waves if getattr(w, "alive", True)]