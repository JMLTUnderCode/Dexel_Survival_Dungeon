import os
import pygame
import math
from kinematics.kinematic import Kinematic, SteeringOutput
from characters.attack_wave import AttackWave
from characters.animation import Animation, load_animations, set_animation_state
from configs.package import CONF

class Player(Kinematic):
    """
    Clase que representa al jugador controlado por el usuario.
    Utiliza entrada de teclado para movimiento y mouse para orientación y ataques.
    
    Parámetros:
    - type: tipo de jugador (puede usarse para diferentes sprites)
    - position: posición inicial del jugador (x, z)
    - collider_box: dimensiones de la caja de colisión del jugador (ancho, alto)
    - max_speed: velocidad máxima del jugador
    """
    def __init__(
        self, 
        type: str, 
        position: tuple, 
        collider_box: tuple[int, int],
        max_speed: float = 200
    ) -> None:
        super().__init__(position=position, orientation=0.0, velocity=(0,0), rotation=0.0)
        self.type = type              # Tipo de jugador (puede usarse para diferentes sprites)
        self.max_speed = max_speed      # Velocidad máxima en píxeles/seg
        self.color = (200, 200, 255)  # Color para las ondas de ataque
        self.attack_waves : list[AttackWave] = []  # Lista de ondas de ataque activas
        self._pending_steering = SteeringOutput()  # Entrada de control pendiente

        self.state = CONF.PLAYER.ACTIONS.IDLE
        self.animations : dict[str, Animation] = load_animations(
            CONF.PLAYER.FOLDER,
            self.type, 
            CONF.PLAYER.ACTIONS, 
            CONF.PLAYER.TILE_WIDTH, 
            CONF.PLAYER.TILE_HEIGHT,
            frame_duration=0.12,
            scale=1.25
        )
        self.current_animation : Animation = self.animations[self.state]
        self.collider_box = collider_box

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Maneja eventos puntuales como clics de mouse para ataques.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            set_animation_state(self, CONF.PLAYER.ACTIONS.ATTACK)
            # Crear onda de ataque en la posición actual
            self.attack_waves.append(AttackWave(self.position[0], self.position[1], color=self.color))

    def handle_input(self, camera_x: float, camera_y: float, dt: float) -> None:
        """
        Maneja la entrada del jugador para movimiento.
        Debe llamarse cada frame antes de actualizar la cinemática.
        """
        # --- Lógica de aceleración y fricción para el movimiento del jugador ---
        # 1. Leer el estado del teclado para detectar las teclas WASD
        keys = pygame.key.get_pressed()
        accel = [0, 0]       # Vector de aceleración lineal (x, y)
        accel_value = 600    # Magnitud de aceleración máxima (pixeles/seg^2)
        friction = 800       # Magnitud de fricción (pixeles/seg^2) para frenado rápido
        # 2. Determinar la dirección de la aceleración según las teclas presionadas
        if keys[pygame.K_w]:
            accel[1] -= 1  # Arriba
        if keys[pygame.K_s]:
            accel[1] += 1  # Abajo
        if keys[pygame.K_a]:
            accel[0] -= 1  # Izquierda
        if keys[pygame.K_d]:
            accel[0] += 1  # Derecha
        # 3. Si hay input, normalizar el vector y escalarlo a la aceleración máxima
        mag = math.hypot(accel[0], accel[1])
        if mag > 0:
            accel[0] = accel[0] / mag * accel_value
            accel[1] = accel[1] / mag * accel_value
            set_animation_state(self, CONF.PLAYER.ACTIONS.MOVE)
        else:
            # 4. Si no hay input, aplicar fricción para desacelerar suavemente
            vx, vy = self.velocity
            speed = math.hypot(vx, vy)
            if speed > 0:
                # Calcular fricción en dirección opuesta a la velocidad
                fx = -vx / speed * friction
                fy = -vy / speed * friction
                # Si la fricción aplicada en este frame es suficiente para detener el movimiento, fuerza la velocidad a cero
                if abs(fx * dt) >= abs(vx) and abs(fy * dt) >= abs(vy):
                    set_animation_state(self, CONF.PLAYER.ACTIONS.IDLE)
                    self.velocity = (0.0, 0.0)
                    accel[0] = 0.0
                    accel[1] = 0.0
                else:
                    accel[0] = fx
                    accel[1] = fy

        # --- Lógica de rotación suave hacia el mouse mejorada ---
        # 1. Obtener la posición del mouse en pantalla y la posición del jugador relativa a la cámara
        mx, my = pygame.mouse.get_pos()
        sx = self.position[0] - camera_x
        sy = self.position[1] - camera_y
        # 2. Calcular el ángulo objetivo (target_angle) entre el jugador y el mouse
        target_angle = math.atan2(my - sy, mx - sx)
        current_angle = self.orientation

        # 3. Calcular la diferencia angular mínima entre la orientación actual y la deseada
        #    Esto asegura que el giro siempre sea por el camino más corto (manejo de wrap-around)
        delta = (target_angle - current_angle + math.pi) % (2 * math.pi) - math.pi
        
        # 4. Parámetros de control de rotación
        max_angular_speed = 30.0  # Límite superior de velocidad angular (radianes/seg)
        angular_accel = 100.0     # Límite superior de aceleración angular (radianes/seg^2)

        # 5. Control proporcional-derivativo (PD) para suavizar y estabilizar la rotación
        #    k_p: Ganancia proporcional (qué tan fuerte responde al error angular)
        #    k_d: Ganancia derivativa (qué tan fuerte responde a la velocidad de giro actual)
        k_p = 16.0
        k_d = 6.0
        # 6. Calcular la velocidad de rotación deseada usando PD y limitarla
        desired_rot = max(-max_angular_speed, min(max_angular_speed, k_p * delta - k_d * self.rotation))
        # 7. El steering angular es la diferencia entre la rotación deseada y la actual
        angular = desired_rot - self.rotation

        # 8. Limitar la aceleración angular para evitar cambios bruscos
        if abs(angular) > angular_accel:
            angular = math.copysign(angular_accel, angular)

        self._pending_steering = SteeringOutput(linear=tuple(accel), angular=angular)

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float):
        """
        Dibuja el jugador en pantalla, rotando el sprite hacia el mouse.
        La posición se ajusta por la cámara para renderizar correctamente en el viewport.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        
        # Rotar sprite según orientación (en radianes, sentido antihorario)
        deg = -math.degrees(self.orientation) - 90  # Corrige desfase de 90 grados
        frame = self.current_animation.get_frame()
        rotated = pygame.transform.rotate(frame, deg)
        rect = rotated.get_rect(center=(sx, sz))
        surface.blit(rotated, rect)

        # Dibujar ondas de ataque
        for wave in self.attack_waves:
            wave.draw(surface, camera_x, camera_z)

                # Dibujar barra de vida del jugador (siempre visible)
        try:
            sx = int(self.position[0] - camera_x)
            sz = int(self.position[1] - camera_z)
            bar_w = 52
            bar_h = 8
            bar_x = sx - bar_w // 2
            bar_y = sz - (self.current_animation.get_size()[1] // 2) - 18
            pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
            hp_ratio = max(0.0, min(1.0, getattr(self, "health", 0.0) / getattr(self, "max_health", 100.0)))
            fill_w = int(bar_w * hp_ratio)
            pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, fill_w, bar_h))
            pygame.draw.rect(surface, (0,0,0), (bar_x, bar_y, bar_w, bar_h), 1)
        except Exception:
            pass

        if CONF.DEV.DEBUG:
            self.draw_collision_box(surface, camera_x, camera_z)

    def draw_collision_box(self, surface: pygame.Surface, camera_x: float, camera_z: float):
        """
        Dibuja el cuadro de colisión del jugador para depuración.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        player_box = pygame.Rect(
            int(sx - self.collider_box[0] // 2),
            int(sz - self.collider_box[1] // 2),
            int(self.collider_box[0]),
            int(self.collider_box[1])
        )
        pygame.draw.rect(surface, (0, 255, 0), player_box, 1)  # Verde, grosor 1

    def update(self, collision_rects: list[pygame.Rect], dt: float):
        """
        Actualiza el jugador: cinemática, animación y ataques.
        Debe llamarse cada frame después de manejar la entrada.
        """
        # Actualizar cinemática
        self.update_by_dynamic(self._pending_steering, self.max_speed, dt, collision_rects, self.collider_box, "PLAYER")

        # Actualizar animación
        self.current_animation.update(dt)

        # Actualizar y limpiar ondas de ataque
        for wave in self.attack_waves:
            wave.update()
        self.attack_waves = [w for w in self.attack_waves if w.alive]