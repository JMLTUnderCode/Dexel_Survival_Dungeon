import math
import pygame
from typing import Union, Dict

from entity.kinematic import Kinematic, SteeringOutput, KinematicSteeringOutput
from entity.entity_spec import EntitySpec
from algorithms.kinematic_seek import KinematicSeek
from algorithms.kinematic_flee import KinematicFlee
from algorithms.kinematic_arrive import KinematicArrive
from algorithms.kinematic_wander import KinematicWander
from algorithms.dynamic_seek import DynamicSeek
from algorithms.dynamic_flee import DynamicFlee
from algorithms.dynamic_arrive import DynamicArrive
from algorithms.dynamic_wander import DynamicWander
from algorithms.align import Align
from algorithms.velocity_match import VelocityMatch
from algorithms.pursue import Pursue
from algorithms.evade import Evade
from algorithms.face import Face
from algorithms.look_where_youre_going import LookWhereYoureGoing
from algorithms.path_following import FollowPath
from entity.animation import Animation, load_animations, set_animation_state
from ai.behavior import Behavior
from configs.package import CONF


class Enemy(Kinematic):
    """
    Descripción
        CLASE: Representa un enemigo del juego que combina cinemática, algoritmos de movimiento
        y una máquina de estados de alto nivel (HSM / Behavior).

    Atributos
        - target (Kinematic): referencia al objetivo (normalmente el jugador).
        - behavior (Behavior | None): instancia de la HSM asociada (si existe).
        - animations (dict[str, Animation]): animaciones cargadas por estado.
        - current_animation (Animation): animación actualmente activa.
        - collider_box (tuple[int,int]): dimensiones de la caja de colisión.
        - algorithm (Enum|str): algoritmo de movimiento activo.
        - max_speeds_for_alg (Dict[str, float]): mapeo algoritmo -> max_speed (cuando aplica).
        - propiedades algorítmicas: atributos como kinematic_seek, dynamic_seek, pursue, follow_path, etc.
    
    Métodos y Funciones
        - draw(surface, camera_x, camera_z): renderiza el enemigo y elementos debug.
        - draw_collision_box(surface, camera_x, camera_z): dibuja la caja de colisión para debug.
        - update(collision_rects, dt): actualiza AI, calcula steering y aplica cinemática.
    
    Propósito
        - Encapsular la lógica visual, física y de IA de un enemigo, permitiendo que la HSM
          cambie el algoritmo en tiempo de ejecución y que la entidad tenga instancias
          específicas por algoritmo con sus propias configuraciones.
    """
    def __init__(self, target: Kinematic, spec: EntitySpec) -> None:
        # 1. Inicializar la parte kinemática base usando la spec
        super().__init__(
            position=spec.initial_position,
            orientation=0.0,
            velocity=(0, 0),
            rotation=0.0,
            statistics=spec.statistics,
            spawn_meta=spec.spawn_meta,
        )

        # 2. Guardar referencias y carga de recursos visuales
        self.target: Kinematic = target
        self.state = CONF.ENEMY.ACTIONS.MOVE
        self.animations: Dict[str, Animation] = load_animations(
            dir=CONF.ENEMY.FOLDER,
            type=spec.sprite.name,
            states_anims=CONF.ENEMY.ACTIONS,
            w_tile=CONF.ENEMY.TILE_WIDTH,
            h_tile=CONF.ENEMY.TILE_HEIGHT,
            frame_duration=spec.sprite.frame_duration,
            scale=spec.sprite.scale,
        )
        self.current_animation: Animation = self.animations[self.state]
        self.collider_box = spec.collider_box

        # 3. Preparar HSM/Behavior (se asignará tras la creación por EntityManager si aplica)
        self.behavior: Behavior | None = None

        # 4. Preparar estructura para máximas por algoritmo y registrar algoritmo inicial
        self.max_speeds_for_alg: Dict[str, float] = {}
        self.algorithm = spec.initial_algorithm

        # 5. Instanciar únicamente los algoritmos configurados en la spec
        for alg_name, alg_config in spec.alg_configs.items():
            match alg_name:
                case CONF.ALG.ALGORITHM.SEEK_KINEMATIC:
                    self.kinematic_seek = KinematicSeek(
                        character=self,                               # Kinematic que se mueve
                        target=target,                                # Objetivo a seguir
                        max_speed=alg_config.max_speed,               # Velocidad máxima
                    )
                case CONF.ALG.ALGORITHM.FLEE_KINEMATIC:
                    self.kinematic_flee = KinematicFlee(
                        character=self,                               # Kinematic que se mueve
                        target=target,                                # Objetivo a seguir
                        max_speed=alg_config.max_speed,               # Velocidad máxima
                    )
                case CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC:
                    self.kinematic_arrive = KinematicArrive(
                        character=self,                               # Kinematic que se mueve
                        target=target,                                # Objetivo a seguir
                        max_speed=alg_config.max_speed,               # Velocidad máxima
                        target_radius=alg_config.target_radius_dist,  # Radio de llegada
                        time_to_target=alg_config.time_to_target      # Tiempo para ajustar la velocidad
                    )
                case CONF.ALG.ALGORITHM.WANDER_KINEMATIC:
                    self.kinematic_wander = KinematicWander(
                        character=self,                               # Kinematic que se mueve
                        max_speed=alg_config.max_speed,               # Velocidad máxima
                        max_rotation=alg_config.max_rotation          # Velocidad angular máxima
                    )

                case CONF.ALG.ALGORITHM.SEEK_DYNAMIC:
                    self.max_speeds_for_alg[alg_name] = alg_config.max_speed # Velocidad máxima
                    self.dynamic_seek = DynamicSeek(
                        character=self,                               # Kinematic que se mueve
                        target=target,                                # Objetivo a seguir
                        max_acceleration=alg_config.max_acceleration  # Aceleración máxima
                    )
                case CONF.ALG.ALGORITHM.FLEE_DYNAMIC:
                    self.max_speeds_for_alg[alg_name] = alg_config.max_speed # Velocidad máxima
                    self.dynamic_flee = DynamicFlee(
                        character=self,                               # Kinematic que se mueve
                        target=target,                                # Objetivo a seguir
                        max_acceleration=alg_config.max_acceleration  # Aceleración máxima
                    )
                case CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC:
                    self.max_speeds_for_alg[alg_name] = alg_config.max_speed # Velocidad máxima
                    self.dynamic_arrive = DynamicArrive(
                        character=self,                               # Kinematic que se mueve
                        target=target,                                # Objetivo a seguir
                        max_speed=alg_config.max_speed,               # Velocidad máxima
                        target_radius=alg_config.target_radius_dist,  # Radio de llegada
                        slow_radius=alg_config.slow_radius_dist,      # Radio para empezar a desacelerar
                        time_to_target=alg_config.time_to_target,     # Tiempo para ajustar la velocidad
                        max_acceleration=alg_config.max_acceleration  # Aceleración máxima
                    )
                case CONF.ALG.ALGORITHM.ALIGN:
                    self.align = Align(
                        character=self,                                 # Quien se alinea
                        target=target,                                  # Referencia para alinearse
                        target_radius=alg_config.target_radius_deg,     # Umbral objetivo de aliniación
                        slow_radius=alg_config.slow_radius_deg,         # Umbral de inicio de desaceleración
                        time_to_target=alg_config.time_to_target,       # Tiempo para ajustar la rotación
                        max_rotation=alg_config.max_rotation,           # Velocidad angular máxima
                        max_angular_accel=alg_config.max_angular_accel  # Aceleración angular máxima
                    )
                case CONF.ALG.ALGORITHM.VELOCITY_MATCH:
                    self.max_speeds_for_alg[alg_name] = getattr(target, "max_speed", 100.0)
                    self.velocity_match = VelocityMatch(
                        character=self,                                # Quien iguala velocidad
                        target=target,                                 # Referencia para igualar velocidad
                        time_to_target=alg_config.time_to_target,      # Tiempo para ajustar velocidad
                        max_acceleration=alg_config.max_acceleration   # Aceleración máxima
                    )
                case CONF.ALG.ALGORITHM.PURSUE:
                    self.pursue = Pursue(
                        character=self,                                # Quien persigue
                        target=target,                                 # Referencia a perseguir
                        max_speed=alg_config.max_speed,                # Velocidad máxima
                        target_radius=alg_config.target_radius_dist,   # Radio de llegada
                        slow_radius=alg_config.slow_radius_dist,       # Radio para empezar a desacelerar
                        time_to_target=alg_config.time_to_target,      # Tiempo para ajustar la velocidad
                        max_acceleration=alg_config.max_acceleration,  # Aceleración máxima
                        max_prediction=alg_config.max_prediction       # Tiempo máximo de predicción
                    )
                case CONF.ALG.ALGORITHM.EVADE:
                    self.max_speeds_for_alg[alg_name] = alg_config.max_speed # Velocidad máxima
                    self.evade = Evade(
                        character=self,                                # Quien evade
                        target=target,                                 # Referencia a evadir
                        max_acceleration=alg_config.max_acceleration,  # Aceleración máxima
                        max_prediction=alg_config.max_prediction       # Tiempo máximo de predicción
                    )
                case CONF.ALG.ALGORITHM.FACE:
                    self.face = Face(
                        character=self,                                  # Quien se orienta
                        target=target,                                   # Referencia para orientarse
                        target_radius=alg_config.target_radius_deg,      # Umbral objetivo de aliniación
                        slow_radius=alg_config.slow_radius_deg,          # Umbral de inicio de desaceleración
                        time_to_target=alg_config.time_to_target,        # Tiempo para ajustar aliniación
                        max_rotation=alg_config.max_rotation,            # Máxima rotación
                        max_angular_accel=alg_config.max_angular_accel,  # Aceleración angular máxima
                    )
                case CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING:
                    self.look_where = LookWhereYoureGoing(
                        character=self,                                  # Quien se alinea
                        target=target,                                   # Referencia para alinearse
                        target_radius=alg_config.target_radius_deg,      # Umbral objetivo de aliniación
                        slow_radius=alg_config.slow_radius_deg,          # Umbral de inicio de desaceleración
                        time_to_target=alg_config.time_to_target,        # Tiempo para ajustar la rotación
                        max_rotation=alg_config.max_rotation,            # Velocidad angular máxima
                        max_angular_accel=alg_config.max_angular_accel,  # Ace leración angular máxima
                    )
                case CONF.ALG.ALGORITHM.WANDER_DYNAMIC:
                    self.max_speeds_for_alg[alg_name] = alg_config.max_speed # Velocidad máxima
                    self.dynamic_wander = DynamicWander(
                        character=self,                                   # Kinematic que se mueve
                        target=target,                                    # Objetivo a seguir (no se usa realmente)
                        target_radius=alg_config.target_radius_deg,       # Umbral objetivo de aliniación (para Face interno)
                        slow_radius=alg_config.slow_radius_deg,           # Umbral de inicio de desaceleración (para Face interno)
                        time_to_target=alg_config.time_to_target,         # Tiempo para ajustar la rotación (para Face interno)
                        max_acceleration=alg_config.max_acceleration,     # Aceleración máxima
                        max_rotation=alg_config.max_rotation,             # Velocidad angular máxima (para Face interno)
                        max_angular_accel=alg_config.max_angular_accel,   # Aceleración angular máxima (para Face interno)
                        wander_offset=alg_config.wander_offset,           # Offset del círculo de wander
                        wander_radius=alg_config.wander_radius,           # Radio del círculo de wander
                        wander_rate=alg_config.wander_rate,               # Tasa de cambio de orientación aleatoria
                        wander_orientation=alg_config.wander_orientation  # Orientación inicial del wander
                    )
                case CONF.ALG.ALGORITHM.PATH_FOLLOWING:
                    self.path = alg_config.path_instance.path
                    self.path_offset = alg_config.path_instance.offset
                    self.follow_path = FollowPath(
                        character=self,                                     # Quien sigue el camino
                        path=self.path,                                     # Camino a seguir
                        offset=self.path_offset,                            # Punto de offset para seguir el camino
                        current_param=alg_config.path_instance.curr_param,  # Punto inicial del camino
                        max_acceleration=alg_config.max_acceleration        # Aceleración máxima
                    )
                case CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING:
                    self.path_offset = alg_config.path_offset
                    self.temp_follow_path: FollowPath | None = None         # Para caminos temporales y mantener original.

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja el enemigo en la pantalla aplicando rotación y debug overlays.

        Argumentos
            - surface (pygame.Surface): Superficie destino donde se dibuja.
            - camera_x (float): posición x de la cámara.
            - camera_z (float): posición z/de eje Y de la cámara.
        """
        # 1. Calcular posición en pantalla relativa a la cámara
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z

        # 2. Rotar el frame actual según la orientación del enemigo
        deg = -math.degrees(self.orientation) - 90
        frame = self.current_animation.get_frame()
        rotated = pygame.transform.rotate(frame, deg)
        rect = rotated.get_rect(center=(sx, sz))

        # 3. Dibujar el sprite rotado en la surface
        surface.blit(rotated, rect)

        # 4. Dibujar la barra de vida encima del sprite (método heredado en Kinematic)
        self.draw_life_bar(surface, camera_x, camera_z)

        # 5. Debug overlays condicionales según configuración
        if CONF.DEV.DEBUG:
            if not hasattr(self.__class__, "_dev_font") or self.__class__._dev_font is None:
                self.__class__._dev_font = pygame.font.SysFont("Segoe UI", 20, bold=True)
            font = self.__class__._dev_font
            anim_h = self.current_animation.get_size()[1]
            base_y = sz - (anim_h // 2) - 40
            _, line_h = font.size("Mg")

            # 5.1 Mostrar algoritmo activo si está habilitado
            if CONF.DEV.ACTIVE_ALG:
                start_y = base_y + (line_h * 2)
                alg_text = self.algorithm.value.upper() if hasattr(self.algorithm, "value") else str(self.algorithm).upper()
                ts = font.render(alg_text, True, (0, 255, 0))
                tw, th = ts.get_size()
                y = int(start_y - line_h) - th
                surface.blit(ts, (sx - tw // 2, y))

            # 5.2 Mostrar historial HSM si existe
            if CONF.DEV.HSM and getattr(self, "behavior", None):
                stack = self.behavior.get_active_stack()
                
                start_y = base_y
                if CONF.DEV.HSM_HISTORY and stack:
                    rep = " > ".join(stack)
                    hist = getattr(self, "_hsm_stack_history", [])
                    if not hist or hist[-1] != rep:
                        hist.append(rep)
                        if len(hist) > CONF.DEV.MAX_HSM_HISTORY_SIZE:
                            hist.pop(0)
                        self._hsm_stack_history = hist

                    start_y -= (line_h * (len(self._hsm_stack_history) - 1))
                    for i, line in enumerate(self._hsm_stack_history):
                        ts = font.render(line, True, (255, 255, 255))
                        tw, th = ts.get_size()
                        y = int(start_y + i * line_h) - th
                        surface.blit(ts, (sx - tw // 2, y))

                # 5.2.1 Mostrar comportamiento activo en pantalla si está habilitado
                if CONF.DEV.ACTIVE_BEHAVIOR:
                    behavior_text = self.behavior.get_name().upper()
                    ts = font.render(behavior_text, True, (0, 255, 0))
                    tw, th = ts.get_size()
                    y = int(start_y - line_h) - th
                    surface.blit(ts, (sx - tw // 2, y))

            # 5.3 Opciones de debug adicionales: colisión y paths
            if CONF.DEV.COLLISION_RECTS:
                self.draw_collision_box(surface, camera_x, camera_z)

            if CONF.DEV.PATHFOLLOWER and hasattr(self, "follow_path") and self.follow_path is not None:
                path = getattr(self.follow_path, "path", None)
                if path is not None:
                    path.draw(surface, camera_x, camera_z, color=(0, 255, 0), width=2)

            if CONF.DEV.TEMP_PATHFOLLOWER and getattr(self, "temp_follow_path", None) is not None:
                path = getattr(self.temp_follow_path, "path", None)
                if path is not None:
                    path.draw(surface, camera_x, camera_z, color=(0, 0, 255), width=2)

    def draw_collision_box(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja la caja de colisión del enemigo para depuración.

        Argumentos
            - surface (pygame.Surface): Superficie destino.
            - camera_x (float): posición x de la cámara.
            - camera_z (float): posición z de la cámara.
        """
        # 1. Calcular posición relativa
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z

        # 2. Construir rectángulo de colisión y dibujarlo en verde
        enemy_box = pygame.Rect(
            int(sx - self.collider_box[0] // 2),
            int(sz - self.collider_box[1] // 2),
            int(self.collider_box[0]),
            int(self.collider_box[1]),
        )
        pygame.draw.rect(surface, (0, 255, 0), enemy_box, 1)

    def update(self, collision_rects: list[pygame.Rect], dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la entidad por frame. Ejecuta la HSM (si existe), calcula
            el steering según el algoritmo activo y aplica la cinemática correspondiente.

        Argumentos
            - collision_rects (list[pygame.Rect]): rectángulos de colisión del mapa.
            - dt (float): delta time en segundos desde la última actualización.
        """
        # 1. Ejecutar tick de la HSM si existe (proteger con try/except)
        if getattr(self, "behavior", None) is not None:
            try:
                self.behavior.tick(dt)
            except Exception:
                # 1.1 No permitir que una excepción en la IA rompa el update global
                pass

        # 2. Seleccionar y obtener el steering según el algoritmo activo
        steering: Union[SteeringOutput, KinematicSteeringOutput] = SteeringOutput(linear=(0, 0), angular=0)
        match self.algorithm:
            case CONF.ALG.ALGORITHM.SEEK_KINEMATIC:
                steering = self.kinematic_seek.get_steering()
            case CONF.ALG.ALGORITHM.FLEE_KINEMATIC:
                steering = self.kinematic_flee.get_steering()
            case CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC:
                steering = self.kinematic_arrive.get_steering()
            case CONF.ALG.ALGORITHM.WANDER_KINEMATIC:
                steering = self.kinematic_wander.get_steering()

            case CONF.ALG.ALGORITHM.SEEK_DYNAMIC:
                steering = self.dynamic_seek.get_steering()
            case CONF.ALG.ALGORITHM.FLEE_DYNAMIC:
                steering = self.dynamic_flee.get_steering()
            case CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC:
                steering = self.dynamic_arrive.get_steering()
            case CONF.ALG.ALGORITHM.WANDER_DYNAMIC:
                steering = self.dynamic_wander.get_steering()
            case CONF.ALG.ALGORITHM.ALIGN:
                steering = self.align.get_steering()
            case CONF.ALG.ALGORITHM.VELOCITY_MATCH:
                steering = self.velocity_match.get_steering()
            case CONF.ALG.ALGORITHM.PURSUE:
                steering = self.pursue.get_steering()
            case CONF.ALG.ALGORITHM.EVADE:
                steering = self.evade.get_steering()
            case CONF.ALG.ALGORITHM.FACE:
                steering = self.face.get_steering()
            case CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING:
                steering_lwyg = self.look_where.get_steering()
                steering_evade = self.evade.get_steering()
                steering = SteeringOutput(linear=steering_evade.linear, angular=steering_lwyg.angular)
            case CONF.ALG.ALGORITHM.PATH_FOLLOWING:
                steering = self.follow_path.get_steering()
            case CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING:
                steering = self.temp_follow_path.get_steering()

        # 3. Aplicar el steering resultante y actualizar la cinemática
        if isinstance(steering, SteeringOutput):
            max_speed = self.max_speeds_for_alg.get(self.algorithm, 100.0)
            # 3.1 Algoritmos de orientación aplican sobre angular (ej. Align/Face)
            if self.algorithm in (CONF.ALG.ALGORITHM.ALIGN, CONF.ALG.ALGORITHM.FACE):
                set_animation_state(self, CONF.ENEMY.ACTIONS.ATTACK_WOUNDED)
                if steering.angular != 0.0:
                    self.update_by_dynamic(steering, max_speed, dt, collision_rects, self.collider_box, self.algorithm)
            else:
                # 3.2 Movimiento lineal: animación MOVE o ATTACK según vector linear
                if steering.linear != (0, 0):
                    set_animation_state(self, CONF.ENEMY.ACTIONS.MOVE)
                    self.update_by_dynamic(steering, max_speed, dt, collision_rects, self.collider_box, self.algorithm)
                else:
                    set_animation_state(self, CONF.ENEMY.ACTIONS.ATTACK)

        elif isinstance(steering, KinematicSteeringOutput):
            # 3.3 Salida kinemática: aplicar update_by_kinematic si hay velocidad
            if steering.velocity != (0, 0):
                set_animation_state(self, CONF.ENEMY.ACTIONS.MOVE)
                self.update_by_kinematic(steering, dt, collision_rects, self.collider_box, self.algorithm)
            else:
                set_animation_state(self, CONF.ENEMY.ACTIONS.ATTACK)

        # 4. Actualizar animación actual con el dt
        self.current_animation.update(dt)