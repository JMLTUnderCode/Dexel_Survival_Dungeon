import os
import pygame
import math
from kinematic import Kinematic, SteeringOutput
from attack_wave import AttackWave
from resource_path import resource_path
from animation import Animation
from configs import *

class Player(Kinematic):
    """
    Clase que representa al jugador controlado por el usuario.
    Utiliza entrada de teclado para movimiento y mouse para orientación y ataques.
    Atributos:
        type: tipo de jugador (puede usarse para diferentes sprites o comportamientos)
        position: posición inicial del jugador (x, y)
        maxSpeed: velocidad máxima del jugador
        map_width, map_height: dimensiones del mapa para clamp
        collision_rects: lista de rectángulos para detección de colisiones
    """
    def __init__(self, type, position, maxSpeed=200, map_width=800, map_height=600, collision_rects=None):
        super().__init__(position=position, orientation=0.0, velocity=(0,0), rotation=0.0, map_width=map_width, map_height=map_height, collision_rects=collision_rects)
        self.type = type
        self.maxSpeed = maxSpeed      # Velocidad máxima en píxeles/seg
        self.color = (200, 200, 255)  # Color para las ondas de ataque
        self.attack_waves : list[AttackWave] = []  # Lista de ondas de ataque activas
        self._pending_steering = SteeringOutput()  # Entrada de control pendiente

        self.state = PLAYER_STATES.IDLE
        self.animations : dict[str, Animation] = self.load_animations()
        self.current_animation : Animation = self.animations[self.state]
        self.collider_box = PLAYER_COLLIDER_BOX

    def get_pos(self):
        return self.position

    def load_animations(self):
        """
        Carga las animaciones del jugador desde archivos PNG.
        Retorna un diccionario con las animaciones cargadas.
        Cada animación se espera que esté en un archivo con el formato:
        """
        base = os.path.join("assets", "player")
        anims = {}
        frame_duration = 0.12
        w_tile = PLAYER_TILE_WIDTH
        h_tile = PLAYER_TILE_HEIGHT
        scale = 1.25
        scale_to = (int(w_tile * scale), int(h_tile * scale))
        # Puedes ajustar los frame_count y frame_duration según cada animación
        for state in PLAYER_STATES:
            state_value = state.value
            filename = f"{self.type}-{state_value}.png"
            path = resource_path(os.path.join(base, filename))
            if os.path.exists(path):
                img = pygame.image.load(path)
                frame_count = img.get_width() // w_tile
                if state_value == PLAYER_STATES.ATTACK:
                    frame_duration = 0.1  # Ajuste específico para "attack"
                anims[state_value] = Animation(path, w_tile, h_tile, frame_count, frame_duration, scale_to=scale_to)
            else:
                raise RuntimeError(f"No se encontró la animación '{state}' para el player '{self.type}'. Verifica que exista el archivo 'src/assets/player/{self.type}-{state}.png'.")
        return anims

    def set_state(self, state):
        """
        Cambia el estado actual del jugador y reinicia la animación correspondiente.
        Si el estado no existe en las animaciones cargadas, lanza un error.
        """
        if state != self.state and state in self.animations:
            self.state = state
            self.current_animation = self.animations[state]
            self.current_animation.current_frame = 0
            self.current_animation.time_acc = 0
        if state not in self.animations:
            raise RuntimeError(f"No se encontró la animación '{state}' para el jugador '{self.type}'. Verifica que exista el archivo 'src/assets/player/{self.type}-{state}.png'.")

    def handle_event(self, event):
        """
        Maneja eventos puntuales como clics de mouse para ataques.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.set_state("attack")
            # Crear onda de ataque en la posición actual
            self.attack_waves.append(AttackWave(self.position[0], self.position[1], color=self.color))

    def handle_input(self, camera_x, camera_y, dt):
        """
        Maneja la entrada del jugador para movimiento y ataque.
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
            self.set_state("move")
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

    def check_changes(self, dt=1/60):
        """
        Actualiza la cinemática, animación y ondas de ataque del jugador.
        Debe llamarse cada frame después de manejar la entrada.
        """
        # Actualizar cinemática
        self.updateKinematic(self._pending_steering, self.maxSpeed, dt)

        # Actualizar animación
        self.current_animation.update(dt)

        # Actualizar y limpiar ondas de ataque
        for wave in self.attack_waves:
            wave.update()
        self.attack_waves = [w for w in self.attack_waves if w.alive]
    
    def draw(self, surface, camera_x, camera_z):
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

        if DEVELOPMENT:
            self.draw_collision_box(surface, camera_x, camera_z)

    def draw_collision_box(self, surface, camera_x, camera_z):
        """
        Dibuja el cuadro de colisión del jugador para depuración.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        player_box = pygame.Rect(
            int(sx - self.collider_box // 2),
            int(sz - self.collider_box // 2),
            int(self.collider_box),
            int(self.collider_box)
        )
        pygame.draw.rect(surface, (0, 255, 0), player_box, 1)  # Verde, grosor 1