import math
import os
import pygame
from typing import Tuple, List, Dict, Optional
from algorithms.dynamic_arrive import DynamicArrive
from algorithms.face import Face
from entity.kinematic import Kinematic, SteeringOutput
from entity.entity_spec import EntitySpec
from entity.animation import Animation, load_animations, load_attack_effects, set_animation_state
from utils.resource_path_dir import resource_path_dir
import helper.debugging as DEBUG
from configs.package import CONF

class Player(Kinematic):
    """
    Descripción
        CLASE: Representa al jugador controlado por el usuario.

    Atributos
        - state (str|Enum): Estado actual usado para seleccionar animación.
        - animations (dict[str, Animation]): Animaciones del personaje cargadas por estado.
        - effects (dict[str, Animation]): Animaciones de efectos visuales (mele, magic).
        - current_animation (Animation): Animación del personaje activa actualmente.
        - current_effect (Optional[Animation]): Efecto visual activo actualmente (si hay).
        - current_effect_type (Optional[str]): Tipo de efecto activo ("mele" o "magic").
        - magic_start_pos (Tuple[float, float]): Posición de inicio del proyectil mágico.
        - magic_target_pos (Tuple[float, float]): Posición de destino del proyectil mágico.
        - collider_box (Tuple[int,int]): Dimensiones de la caja de colisión.
        - pivot_max_radius: (float): Radio máximo permitido para el pivot de movimiento.
        - max_speed (float): Velocidad máxima en píxeles/segundo.
        - pivot_point_move (Kinematic): Punto pivot usado para movimiento.
        - pivot_point_mouse (Kinematic): Punto pivot usado para orientación hacia mouse.
        - dynamic_arrive (DynamicArrive): Algoritmo de llegada dinámica para movimiento.
        - face (Face): Algoritmo Face para orientación hacia el mouse.
        
    Métodos y Funciones
        - handle_event: Maneja eventos puntuales (mouse clicks) para iniciar ataques.
        - handle_input: Procesa entrada de teclado + rotación hacia mouse.
        - update_pivot_mouse: Actualiza la posición del pivot del mouse.
        - draw: Dibuja el jugador y sus efectos (con lógica de offset y proyectil).
        - update: Actualiza cinemática, animaciones y cooldowns.

    Propósito
        - Permitir control directo del jugador mediante teclado y mouse, con animaciones
          de ataque y gestión de estados.
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

        # 2. Cargar animaciones del personaje (IDLE, MOVE, ATTACK)
        self.state = CONF.PLAYER.ACTIONS.IDLE
        self.animations: Dict[str, Animation] = load_animations(
            dir=CONF.PLAYER.FOLDER_ANIM,
            type=spec.sprite.name,
            states_anims=CONF.PLAYER.ACTIONS,
            w_tile=CONF.PLAYER.TILE_WIDTH,
            h_tile=CONF.PLAYER.TILE_HEIGHT,
            frame_duration=spec.sprite.frame_duration,
            scale=spec.sprite.scale,
        )
        self.current_animation: Animation = self.animations[self.state]
        self.collider_box: Tuple[int, int] = spec.collider_box

        # 2.1. Configurar animaciones específicas (One-Shot vs Loop)
        if CONF.PLAYER.ACTIONS.ATTACK in self.animations:
            self.animations[CONF.PLAYER.ACTIONS.ATTACK].loop = False
        
        # 3. Cargar efectos visuales
        self.effects: Dict[str, Animation] = load_attack_effects(
            entity=self,
            dir=CONF.PLAYER.FOLDER_EFFECTS,
            effects=CONF.PLAYER.EFFECTS,
            scale=spec.sprite.scale
        )
        self.current_effect: Optional[Animation] = None
        self.current_effect_type: Optional[str] = None
        
        # 3.1. Variables para la lógica del proyectil mágico
        self.magic_start_pos: Tuple[float, float] = (0.0, 0.0)
        self.magic_target_pos: Tuple[float, float] = (0.0, 0.0)

        # 4. Configurar algoritmos y parámetros por defecto
        self.algorithm = spec.initial_algorithm
        self.max_speed = 120.0 
        for alg_name, alg_config in spec.alg_configs.items():
            match alg_name:
                case CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC:
                    self.max_speed = alg_config.max_speed
                    self.pivot_max_radius = max(alg_config.target_radius_dist, 2.0 * alg_config.slow_radius_dist)                
                    self.pivot_point_move: Kinematic = Kinematic(position=spec.initial_position, orientation=0.0, velocity=(0.0,0.0), rotation=0.0)
                    self.dynamic_arrive = DynamicArrive(
                        character=self,
                        target=self.pivot_point_move,
                        max_speed=alg_config.max_speed,
                        target_radius=alg_config.target_radius_dist,
                        slow_radius=alg_config.slow_radius_dist,
                        time_to_target=alg_config.time_to_target,
                        max_acceleration=alg_config.max_acceleration
                    )
                case CONF.ALG.ALGORITHM.FACE:
                    pivot_pos = (spec.initial_position[0]+10.0, spec.initial_position[1]+10.0)
                    self.pivot_point_mouse: Kinematic = Kinematic(position=pivot_pos, orientation=0.0, velocity=(0.0,0.0), rotation=0.0)
                    self.face = Face(
                        character=self,
                        target=self.pivot_point_mouse,
                        target_radius=alg_config.target_radius_deg,
                        slow_radius=alg_config.slow_radius_deg,
                        time_to_target=alg_config.time_to_target,
                        max_rotation=alg_config.max_rotation,
                        max_angular_accel=alg_config.max_angular_accel,
                    )

        # 5. Ancho UI activo
        self.width_ui = CONF.MAP_UI.PANEL_WIDTH if CONF.MAP_UI.ACTIVE else 0.0
        self.width_ui = CONF.ALG_UI.PANEL_WIDTH if CONF.ALG_UI.ACTIVE and not CONF.MAP_UI.ACTIVE else self.width_ui

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Descripción
            MÉTODO: Maneja eventos puntuales como clics de mouse para iniciar ataques.
            Activa el estado ATTACK y asigna el efecto visual correspondiente.

        Argumentos
            - event (pygame.event.Event): Evento recibido desde la cola de eventos.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1. Click Izquierdo -> Ataque Mele
            if event.button == 1:
                if self.curr_mele_cooldown <= 0:
                    set_animation_state(self, CONF.PLAYER.ACTIONS.ATTACK)
                    self.current_animation.reset()
                    self.curr_mele_cooldown = self.mele_cooldown
                    
                    # Asignar y resetear efecto mele
                    if "mele" in self.effects:
                        self.current_effect = self.effects["mele"]
                        self.current_effect_type = "mele"
                        self.current_effect.reset()
            
            # 2. Click Derecho -> Ataque Mágico
            elif event.button == 3:
                if self.curr_magic_cooldown <= 0:
                    set_animation_state(self, CONF.PLAYER.ACTIONS.ATTACK)
                    self.current_animation.reset()
                    self.curr_magic_cooldown = self.magic_cooldown
                    
                    # Asignar y resetear efecto magic
                    if "magic" in self.effects:
                        self.current_effect = self.effects["magic"]
                        self.current_effect_type = "magic"
                        self.current_effect.reset()
                        
                        # Calcular posiciones para el proyectil
                        mx, my = pygame.mouse.get_pos()
                        # Usamos la posición del pivot_mouse que ya está en 
                        # coordenadas de mundo y se actualiza cada frame.
                        self.magic_target_pos = self.pivot_point_mouse.position
                        self.magic_start_pos = self.position

    def _clamp_pivot_move_distance(self, pivot_x: float, pivot_y: float) -> Tuple[float, float]:
        """
        Descripción
            FUNCIÓN: Clampa la posición del pivot_move para que su distancia al jugador esté
                     entre pivot_target_radius y pivot_max_radius.
        
        Argumentos
            - pivot_x (float): Coordenada X deseada del pivot.
            - pivot_y (float): Coordenada Y deseada del pivot.

        Retorno
            - Tuple[float, float]: Coordenadas (x, y) ajustadas dentro del radio permitido.
        """
        # 1. Calcular distancia actual al jugador
        px, py = self.position
        dx = pivot_x - px
        dy = pivot_y - py
        dist = math.hypot(dx, dy)

        # 2. Si excede el radio máximo, escalar el vector para que quede en el borde
        if dist > self.pivot_max_radius:
            scale = self.pivot_max_radius / dist
            return (px + dx * scale, py + dy * scale)
        else:
            return (pivot_x, pivot_y)

    def handle_input(self, camera_x: float, camera_y: float, dt: float) -> None:
        """
        Descripción
            MÉTODO: Procesa la entrada para mover el pivot_move con WASD y actualizar pivot_mouse.
            NOTA: La actualización del estado de animación (MOVE/IDLE) se delega al update().

        Argumentos
            - camera_x (float): Posición X de la cámara.
            - camera_y (float): Posición Y de la cámara.
            - dt (float): Delta time en segundos.
        """
        # 1. Leer teclado y construir dirección [-1,1]
        keys = pygame.key.get_pressed()
        dir_x, dir_y = 0.0, 0.0
        if keys[pygame.K_w]: dir_y -= 1.0
        if keys[pygame.K_s]: dir_y += 1.0
        if keys[pygame.K_a]: dir_x -= 1.0
        if keys[pygame.K_d]: dir_x += 1.0

        # 2. Configurar velocidades
        pivot_speed = float(getattr(CONF.PLAYER, "PIVOT_MOVE_SPEED", 600.0))
        pivot_return_speed = float(getattr(CONF.PLAYER, "PIVOT_RETURN_SPEED", 800.0))
        eps = getattr(CONF.PLAYER, "PIVOT_EPS", 1e-3)

        # 3. Mover el pivot según input
        if abs(dir_x) > 0.0 or abs(dir_y) > 0.0:
            mag = math.hypot(dir_x, dir_y)
            nx, ny = (dir_x / mag, dir_y / mag) if mag > 0.0 else (0.0, 0.0)
            px, py = self.pivot_point_move.position
            new_px = px + nx * pivot_speed * dt
            new_py = py + ny * pivot_speed * dt

            clamped_x, clamped_y = self._clamp_pivot_move_distance(new_px, new_py)
            self.pivot_point_move.position = (clamped_x, clamped_y)
        else:
            # 4. Sin input: devolver pivot hacia el jugador
            px, py = self.pivot_point_move.position
            player_x, player_y = self.position
            dx = player_x - px
            dy = player_y - py
            dist = math.hypot(dx, dy)

            if dist <= eps:
                self.pivot_point_move.position = (player_x, player_y)
            else:
                dir_to_player_x = dx / dist
                dir_to_player_y = dy / dist
                step = min(pivot_return_speed * dt, dist)
                new_px = px + dir_to_player_x * step
                new_py = py + dir_to_player_y * step
                self.pivot_point_move.position = (new_px, new_py)

        # 5. Actualizar pivot mouse
        self.update_pivot_mouse(camera_x, camera_y)

    def update_pivot_mouse(self, camera_x: float, camera_y: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la posición del pivot del mouse en coordenadas de mundo.

        Argumentos
            - camera_x (float): Posición X de la cámara.
            - camera_y (float): Posición Y de la cámara.
        """
        # 1. Obtener posición del mouse y convertir a coordenadas de mundo
        mx, my = pygame.mouse.get_pos()
        world_mx = mx + camera_x - self.width_ui
        world_my = my + camera_y
        self.pivot_point_mouse.position = (world_mx, world_my)

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja el jugador y sus efectos en la superficie indicada.

        Argumentos
            - surface (pygame.Surface): Superficie de destino.
            - camera_x (float): Posición X de la cámara.
            - camera_z (float): Posición Z (Y en 2D) de la cámara.
        """
        # 1. Calcular posición en pantalla del jugador
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z

        # 2. Rotar y dibujar el sprite del jugador
        deg = -math.degrees(self.orientation) - 90.0
        frame = self.current_animation.get_frame()
        rotated = pygame.transform.rotate(frame, deg)
        rect = rotated.get_rect(center=(sx, sz))
        surface.blit(rotated, rect)

        # 3. Dibujar efecto visual activo (si existe y no ha terminado)
        self.draw_attack_effect(surface, camera_x, camera_z, sx, sz, deg)

        # 4. Dibujar barra de vida
        self.draw_life_bar(surface, camera_x, camera_z)

        # 5. Debug overlays
        if CONF.DEV.DEBUG:
            DEBUG.draw_player_overlays(self, surface, sx, sz, camera_x, camera_z)
            
    def update(self, collision_rects: List[pygame.Rect], dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la cinemática, animaciones y cooldowns.
            Gestiona la prioridad de estados de animación (Ataque > Movimiento > Idle).

        Argumentos
            - collision_rects (List[pygame.Rect]): Lista de rectángulos de colisión.
            - dt (float): Delta time en segundos.
        """
        # 1. Actualizar cooldowns
        self.update_cooldowns(dt)

        # 2. Cinemática (Steering)
        LINEAR_EPS = 1e-9
        ANGULAR_EPS = 1e-9
        linear = (0.0, 0.0)
        angular = 0.0

        if hasattr(self, "dynamic_arrive"):
            try:
                d_steer = self.dynamic_arrive.get_steering()
                linear = d_steer.linear
            except Exception:
                linear = (0.0, 0.0)

        if hasattr(self, "face"):
            try:
                f_steer = self.face.get_steering()
                angular = f_steer.angular
            except Exception:
                angular = 0.0

        if math.hypot(linear[0], linear[1]) < LINEAR_EPS:
            linear = (0.0, 0.0)
            self.velocity = (0.0, 0.0)
        if abs(angular) < ANGULAR_EPS:
            angular = 0.0
            self.rotation = 0.0

        steering = SteeringOutput(linear=linear, angular=angular)
        self.update_by_dynamic(steering, self.max_speed, dt, collision_rects, self.collider_box, "PLAYER")

        # 3. GESTOR DE ESTADOS REACTIVO
        is_attacking = (self.state == CONF.PLAYER.ACTIONS.ATTACK)
        
        if is_attacking:
            # 4. Verificar si TANTO la animación del personaje COMO el efecto han terminado
            anim_finished = self.current_animation.is_finished
            effect_finished = True
            if self.current_effect:
                effect_finished = self.current_effect.is_finished

            # 5. Solo salir del estado de ataque si AMBOS han terminado
            if anim_finished and effect_finished:
                self.current_effect = None
                self.current_effect_type = None
                
                # Decidir si IDLE o MOVE basado en velocidad
                if math.hypot(self.velocity[0], self.velocity[1]) > 1.0:
                    set_animation_state(self, CONF.PLAYER.ACTIONS.MOVE)
                else:
                    set_animation_state(self, CONF.PLAYER.ACTIONS.IDLE)
            # Si no ha terminado alguno, NO cambiar estado (bloqueo visual)
        else:
            # Comportamiento normal: MOVE si hay velocidad, IDLE si no
            if math.hypot(self.velocity[0], self.velocity[1]) > 1.0:
                set_animation_state(self, CONF.PLAYER.ACTIONS.MOVE)
            else:
                set_animation_state(self, CONF.PLAYER.ACTIONS.IDLE)

        # 6. Actualizar animación actual y efecto
        self.current_animation.update(dt)
        if self.current_effect:
            self.current_effect.update(dt)