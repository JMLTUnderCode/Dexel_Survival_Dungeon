import math
import pygame
from typing import Tuple, List, Dict
from algorithms.dynamic_arrive import DynamicArrive
from algorithms.face import Face
from entity.kinematic import Kinematic, SteeringOutput
from entity.entity_spec import EntitySpec
from entity.attack_wave import AttackWave
from entity.animation import Animation, load_animations, set_animation_state
import helper.debugging as DEBUG
from configs.package import CONF

class Player(Kinematic):
    """
    Descripción
        CLASE: Representa al jugador controlado por el usuario.

    Atributos
        - state (str|Enum): Estado actual usado para seleccionar animación.
        - animations (dict[str, Animation]): Animaciones cargadas por estado.
        - current_animation (Animation): Animación activa actualmente.
        - collider_box (Tuple[int,int]): Dimensiones de la caja de colisión.
        - pivot_max_radius: (float): Radio máximo permitido para el pivot de movimiento.
        - max_speed (float): Velocidad máxima en píxeles/segundo.
        - pivot_point_move (Kinematic): Punto pivot usado para movimiento.
        - pivot_point_mouse (Kinematic): Punto pivot usado para orientación hacia mouse.
        - dynamic_arrive (DynamicArrive): Algoritmo de llegada dinámica para movimiento.
        - face (Face): Algoritmo Face para orientación hacia el mouse.
        - attack_waves (List[AttackWave]): Ondas de ataque generadas por el jugador.

    Métodos y Funciones
        - handle_event: Maneja eventos puntuales (mouse clicks).
        - handle_input: Procesa entrada de teclado + rotación hacia mouse.
        - update_pivot_mouse: Actualiza la posición del pivot del mouse.
        - draw: Dibuja el jugador y sus efectos (ondas, barra de vida).
        - draw_collision_box: Dibuja la caja de colisión (debug).
        - update: Actualiza cinemática, animaciones y limpia ondas.

    Propósito
        - Permitir control directo del jugador mediante teclado y mouse, con animaciones
          y sistema de ondas de ataque simple.
    """
    def __init__(self, spec: EntitySpec) -> None:
        # 1. Inicializar la parte kinemática base usando la spec
        super().__init__(
            position=spec.initial_position,
            orientation=0.0,
            velocity=(0, 0),
            rotation=0.0,
            statistics=spec.statistics,
            spawn_meta=spec.spawn_meta,
        )
        
        # 2. Estado y animaciones
        self.state = CONF.PLAYER.ACTIONS.IDLE
        self.animations: Dict[str, Animation] = load_animations(
            dir=CONF.PLAYER.FOLDER,
            type=spec.sprite.name,
            states_anims=CONF.PLAYER.ACTIONS,
            w_tile=CONF.PLAYER.TILE_WIDTH,
            h_tile=CONF.PLAYER.TILE_HEIGHT,
            frame_duration=spec.sprite.frame_duration,
            scale=spec.sprite.scale,
        )
        self.current_animation: Animation = self.animations[self.state]
        self.collider_box: Tuple[int, int] = spec.collider_box

        # 3. Configurar algoritmos y parámetros por defecto
        self.algorithm = spec.initial_algorithm
        self.max_speed = 120.0 
        for alg_name, alg_config in spec.alg_configs.items():
            match alg_name:
                case CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC:
                    self.max_speed = alg_config.max_speed # Velocidad máxima ajustable por algoritmo
                    # Pivot máximo para el movimiento (mayor que target_radius y slow_radius)
                    self.pivot_max_radius = max(alg_config.target_radius_dist, 2.0 * alg_config.slow_radius_dist)                
                    self.pivot_point_move: Kinematic = Kinematic(position=spec.initial_position, orientation=0.0, velocity=(0.0,0.0), rotation=0.0)
                    self.dynamic_arrive = DynamicArrive(
                        character=self,                               # Kinematic que se mueve
                        target=self.pivot_point_move,                 # Objetivo a seguir
                        max_speed=alg_config.max_speed,               # Velocidad máxima
                        target_radius=alg_config.target_radius_dist,  # Radio de llegada
                        slow_radius=alg_config.slow_radius_dist,      # Radio para empezar a desacelerar
                        time_to_target=alg_config.time_to_target,     # Tiempo para ajustar la velocidad
                        max_acceleration=alg_config.max_acceleration  # Aceleración máxima
                    )
                case CONF.ALG.ALGORITHM.FACE:
                    # Pivot para la orientación (usualmente la posición del mouse)
                    pivot_pos = (spec.initial_position[0]+10.0, spec.initial_position[1]+10.0)
                    self.pivot_point_mouse: Kinematic = Kinematic(position=pivot_pos, orientation=0.0, velocity=(0.0,0.0), rotation=0.0)
                    self.face = Face(
                        character=self,                                  # Quien se orienta
                        target=self.pivot_point_mouse,                   # Referencia para orientarse
                        target_radius=alg_config.target_radius_deg,      # Umbral objetivo de aliniación
                        slow_radius=alg_config.slow_radius_deg,          # Umbral de inicio de desaceleración
                        time_to_target=alg_config.time_to_target,        # Tiempo para ajustar aliniación
                        max_rotation=alg_config.max_rotation,            # Máxima rotación
                        max_angular_accel=alg_config.max_angular_accel,  # Aceleración angular máxima
                    )

        # 4. Efectos de ataque
        self.attack_waves: List[AttackWave] = []

        # 5. Ancho UI activo para ajustar cálculo de posición del mouse
        self.width_ui = CONF.MAP_UI.PANEL_WIDTH if CONF.MAP_UI.ACTIVE else 0.0
        self.width_ui = CONF.ALG_UI.PANEL_WIDTH if CONF.ALG_UI.ACTIVE and not CONF.MAP_UI.ACTIVE else self.width_ui

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

    def _clamp_pivot_move_distance(self, pivot_x: float, pivot_y: float) -> Tuple[float, float]:
        """
        Descripción
            FUNCIÓN: Clampa la posición del pivot_move para que su distancia al jugador esté
                     entre pivot_target_radius y pivot_max_radius.

        Argumentos
            - pivot_x (float) : Coordenada X propuesta del pivot.
            - pivot_y (float) : Coordenada Y propuesta del pivot.

        Retorno
            Tupla con las coordenadas (x, y) clamped del pivot.
        """
        # 1. Calcular vector desde el jugador hasta el pivot propuesto
        px, py = self.position
        dx = pivot_x - px
        dy = pivot_y - py
        dist = math.hypot(dx, dy)

        # 2. Si excede el radio máximo, escalar el vector para ajustarlo
        if dist > self.pivot_max_radius:
            scale = self.pivot_max_radius / dist
            return (px + dx * scale, py + dy * scale)
        else:
            # 3. Devolver la posición original si está dentro del rango permitido
            return (pivot_x, pivot_y)


    def handle_input(self, camera_x: float, camera_y: float, dt: float) -> None:
        """
        Descripción
            MÉTODO:  Procesa la entrada para mover el pivot_move con WASD y actualizar pivot_mouse
            a la posición world del mouse. No calcula steering directo: los algoritmos
            (DynamicArrive y Face) se encargan en update().

        Argumentos
            - camera_x (float): Coordenada X de la cámara (para cálculo relativo).
            - camera_y (float): Coordenada Y de la cámara (para cálculo relativo).
            - dt (float): Delta time en segundos.
        """
        # 1. Leer teclado y construir dirección [-1,1]
        keys = pygame.key.get_pressed()
        dir_x, dir_y = 0.0, 0.0
        if keys[pygame.K_w]:
            dir_y -= 1.0
        if keys[pygame.K_s]:
            dir_y += 1.0
        if keys[pygame.K_a]:
            dir_x -= 1.0
        if keys[pygame.K_d]:
            dir_x += 1.0

        # 2. Configurar velocidades de pivot y tolerancia
        pivot_speed = float(getattr(CONF.PLAYER, "PIVOT_MOVE_SPEED", 600.0))
        pivot_return_speed = float(getattr(CONF.PLAYER, "PIVOT_RETURN_SPEED", 800.0))
        eps = getattr(CONF.PLAYER, "PIVOT_EPS", 1e-3)

        # 3. Si hay input, desplazar el pivot en la dirección normalizada y clamar el radio
        if abs(dir_x) > 0.0 or abs(dir_y) > 0.0:
            mag = math.hypot(dir_x, dir_y)
            nx, ny = (dir_x / mag, dir_y / mag) if mag > 0.0 else (0.0, 0.0)
            px, py = self.pivot_point_move.position
            new_px = px + nx * pivot_speed * dt
            new_py = py + ny * pivot_speed * dt

            # 4. Clamp relativo al player para mantener el pivot dentro de los radios permitidos
            clamped_x, clamped_y = self._clamp_pivot_move_distance(new_px, new_py)
            self.pivot_point_move.position = (clamped_x, clamped_y)
            set_animation_state(self, CONF.PLAYER.ACTIONS.MOVE)
        else:
            # 5. Sin input: devolver pivot hacia la posición exacta del jugador (snap hacia centro)
            px, py = self.pivot_point_move.position
            player_x, player_y = self.position
            dx = player_x - px
            dy = player_y - py
            dist = math.hypot(dx, dy)

            if dist <= eps:
                # 6. Centrar pivot exactamente en la posición del jugador
                self.pivot_point_move.position = (player_x, player_y)
                set_animation_state(self, CONF.PLAYER.ACTIONS.IDLE)
            else:
                # 7. Mover el pivot hacia la posición del jugador sin quedarse en un "radio mínimo"
                dir_to_player_x = dx / dist
                dir_to_player_y = dy / dist
                step = min(pivot_return_speed * dt, dist)
                new_px = px + dir_to_player_x * step
                new_py = py + dir_to_player_y * step
                # 8. Snap si tras el paso quedamos dentro de eps
                if math.hypot(new_px - player_x, new_py - player_y) <= eps:
                    self.pivot_point_move.position = (player_x, player_y)
                    set_animation_state(self, CONF.PLAYER.ACTIONS.IDLE)
                else:
                    self.pivot_point_move.position = (new_px, new_py)
                    # 9. Si aún nos movemos, mantener estado MOVE
                    set_animation_state(self, CONF.PLAYER.ACTIONS.MOVE)

        # 10. Actualizar pivot mouse a la posición world del mouse
        self.update_pivot_mouse(camera_x, camera_y)

    def update_pivot_mouse(self, camera_x: float, camera_y: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la posición del pivot_point_mouse a la posición world del mouse.

        Argumentos
            - camera_x (float): Coordenada X de la cámara.
            - camera_y (float): Coordenada Y de la cámara.
        """
        mx, my = pygame.mouse.get_pos()
        world_mx = mx + camera_x - self.width_ui
        world_my = my + camera_y
        self.pivot_point_mouse.position = (world_mx, world_my)

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

        # 5. Debug overlays condicionales según configuración
        if CONF.DEV.DEBUG:
            DEBUG.draw_player_overlays(self, surface, sx, sz, camera_x, camera_z)
            
    def update(self, collision_rects: List[pygame.Rect], dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la cinemática, animaciones y mantiene las ondas de ataque.

        Argumentos
            - collision_rects (List[pygame.Rect]): Rectángulos del mapa usados para colisión.
            - dt (float): Delta time en segundos.
        """
        # 1. Tolerancias para evitar jitter numérico
        LINEAR_EPS = 1e-9
        ANGULAR_EPS = 1e-9

        # 2. Inicializar steering
        linear = (0.0, 0.0)
        angular = 0.0

        # 3. Movimiento: DynamicArrive sobre pivot_move
        if hasattr(self, "dynamic_arrive"):
            try:
                d_steer = self.dynamic_arrive.get_steering()
                linear = d_steer.linear
            except Exception:
                linear = (0.0, 0.0)

        # 4. Orientación: Face sobre pivot_mouse
        if hasattr(self, "face"):
            try:
                f_steer = self.face.get_steering()
                angular = f_steer.angular
            except Exception:
                angular = 0.0

        # 5. Eliminar componentes muy pequeñas para evitar drift / oscilación
        if math.hypot(linear[0], linear[1]) < LINEAR_EPS:
            linear = (0.0, 0.0)
            # asegurar que la velocidad física quede a cero
            self.velocity = (0.0, 0.0)
        if abs(angular) < ANGULAR_EPS:
            angular = 0.0
            # opcional: estabilizar rotación residual
            self.rotation = 0.0

        # 6. Combinar y aplicar steering como input dinámico
        steering = SteeringOutput(linear=linear, angular=angular)
        self.update_by_dynamic(steering, self.max_speed, dt, collision_rects, self.collider_box, "PLAYER")

        # 7. Actualizar animación y ondas
        self.current_animation.update(dt)
        for wave in self.attack_waves:
            wave.update()
        self.attack_waves = [w for w in self.attack_waves if getattr(w, "alive", True)]