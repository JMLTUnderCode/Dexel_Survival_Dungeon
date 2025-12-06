import math
import pygame
from typing import Optional, Union, Dict, Tuple

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
from entity.animation import Animation, load_animations, load_attack_effects, set_animation_state
from ai.behavior import Behavior
import helper.debugging  as DEBUG
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
        - effects (dict[str, Animation]): animaciones de efectos de ataque.
        - current_animation (Animation): animación actualmente activa.
        - current_effect (Optional[Animation]): efecto visual activo.
        - collider_box (tuple[int,int]): dimensiones de la caja de colisión.
        - algorithm (Enum|str): algoritmo de movimiento activo.
        - max_speeds_for_alg (Dict[str, float]): mapeo algoritmo -> max_speed (cuando aplica).
        - magic_start_pos (Tuple[float, float]): inicio de efecto mágico.
        - magic_target_pos (Tuple[float, float]): destino de efecto mágico.
    
    Métodos y Funciones
        - draw(surface, camera_x, camera_z): renderiza el enemigo y elementos debug.
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
        self.state = CONF.ENEMY.ACTIONS.IDLE
        self.animations: Dict[str, Animation] = load_animations(
            dir=CONF.ENEMY.FOLDER_ANIM,
            type=spec.sprite.name,
            states_anims=CONF.ENEMY.ACTIONS,
            w_tile=CONF.ENEMY.TILE_WIDTH,
            h_tile=CONF.ENEMY.TILE_HEIGHT,  
            frame_duration=spec.sprite.frame_duration,
            scale=spec.sprite.scale,
        )
        self.current_animation: Animation = self.animations[self.state]
        self.collider_box = spec.collider_box

        # 2.1. Configurar animaciones específicas (One-Shot vs Loop)
        if CONF.ENEMY.ACTIONS.ATTACK in self.animations:
            self.animations[CONF.ENEMY.ACTIONS.ATTACK].loop = False

        # 2.2 Cargar efectos visuales
        self.effects: Dict[str, Animation] = load_attack_effects(
            entity=self,
            dir=CONF.ENEMY.FOLDER_EFFECTS,
            effects=CONF.ENEMY.EFFECTS,
            scale=spec.sprite.scale
        )
        self.current_effect: Optional[Animation] = None
        self.current_effect_type: Optional[str] = None
        
        # 2.3 Variables para efectos proyectiles (Magic)
        self.magic_start_pos: Tuple[float, float] = (0.0, 0.0)
        self.magic_target_pos: Tuple[float, float] = (0.0, 0.0)

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
            MÉTODO: Dibuja el enemigo y sus efectos en la superficie indicada.

        Argumentos
            - surface (pygame.Surface): Superficie de destino.
            - camera_x (float): Posición X de la cámara.
            - camera_z (float): Posición Z (Y en 2D) de la cámara.
        """
        # 1. Calcular posición en pantalla relativa a la cámara
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z

        # 2. Rotar el frame actual según la orientación del enemigo
        deg = -math.degrees(self.orientation) - 90.0
        frame = self.current_animation.get_frame()
        rotated = pygame.transform.rotate(frame, deg)
        rect = rotated.get_rect(center=(sx, sz))
        surface.blit(rotated, rect)

        # 3. Dibujar efecto visual activo (método heredado en Kinematic)
        self.draw_attack_effect(surface, camera_x, camera_z, sx, sz, deg)

        # 4. Dibujar la barra de vida encima del sprite (método heredado en Kinematic)
        self.draw_life_bar(surface, camera_x, camera_z)

        # 5. Debug overlays condicionales según configuración
        if CONF.DEV.DEBUG:
            DEBUG.draw_enemy_overlays(self, surface, sx, sz, camera_x, camera_z)

    def update(self, collision_rects: list[pygame.Rect], dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualiza la entidad por frame. Ejecuta la HSM (si existe), calcula
            el steering según el algoritmo activo y aplica la cinemática correspondiente.
            Gestiona el estado de animación de forma reactiva.

        Argumentos
            - collision_rects (list[pygame.Rect]): rectángulos de colisión del mapa.
            - dt (float): delta time en segundos desde la última actualización.
        """
        # 1. Actualizar cooldowns
        self.update_cooldowns(dt)

        # 2. Ejecutar tick de la HSM si existe (proteger con try/except)
        if getattr(self, "behavior", None) is not None:
            try:
                self.behavior.tick(dt)
            except Exception:
                pass

        # 3. Seleccionar y obtener el steering según el algoritmo activo
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
                steering_lwyg = self.look_where.get_steering()
                steering_pursue = self.pursue.get_steering()
                steering = SteeringOutput(linear=steering_pursue.linear, angular=steering_lwyg.angular)
            case CONF.ALG.ALGORITHM.EVADE:
                steering = self.evade.get_steering()
            case CONF.ALG.ALGORITHM.FACE:
                steering = self.face.get_steering()
            case CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING:
                steering_lwyg = self.look_where.get_steering()
                steering_evade = self.evade.get_steering()
                steering = SteeringOutput(linear=steering_evade.linear, angular=steering_lwyg.angular)
            case CONF.ALG.ALGORITHM.PATH_FOLLOWING:
                steering_lwyg = self.look_where.get_steering()
                steering_path = self.follow_path.get_steering()
                steering = SteeringOutput(linear=steering_path.linear, angular=steering_lwyg.angular)
            case CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING:
                steering_lwyg = self.look_where.get_steering()
                steering_tpath = self.temp_follow_path.get_steering()
                steering = SteeringOutput(linear=steering_tpath.linear, angular=steering_lwyg.angular)

        # 4. Aplicar el steering resultante y actualizar la cinemática
        if isinstance(steering, SteeringOutput):
            max_speed = self.max_speeds_for_alg.get(self.algorithm, 100.0)
            # 4.1 Algoritmos de orientación aplican sobre angular (ej. Align/Face)
            if self.algorithm in (CONF.ALG.ALGORITHM.ALIGN, CONF.ALG.ALGORITHM.FACE):
                if steering.angular != 0.0:
                    self.update_by_dynamic(steering, max_speed, dt, collision_rects, self.collider_box, self.algorithm)
            else:
                # 4.2 Movimiento lineal
                if steering.linear != (0, 0):
                    self.update_by_dynamic(steering, max_speed, dt, collision_rects, self.collider_box, self.algorithm)

        elif isinstance(steering, KinematicSteeringOutput):
            # 4.3 Salida kinemática: aplicar update_by_kinematic si hay velocidad
            if steering.velocity != (0, 0):
                self.update_by_kinematic(steering, dt, collision_rects, self.collider_box, self.algorithm)

        # 5. GESTOR DE ESTADOS REACTIVO (Animaciones)
        is_attacking = (self.state == CONF.ENEMY.ACTIONS.ATTACK) or (self.state == CONF.ENEMY.ACTIONS.ATTACK_WOUNDED)
        
        if is_attacking:
            # 5.1 Verificar si TANTO la animación COMO el efecto han terminado
            anim_finished = self.current_animation.is_finished
            effect_finished = True
            if self.current_effect:
                effect_finished = self.current_effect.is_finished
            
            # 5.2 Solo salir del estado de ataque si AMBOS han terminado
            if anim_finished and effect_finished:
                self.current_effect = None
                self.current_effect_type = None
                
                # Decidir si IDLE o MOVE basado en velocidad
                if math.hypot(self.velocity[0], self.velocity[1]) > 1.0:
                    set_animation_state(self, CONF.ENEMY.ACTIONS.MOVE)
                else:
                    set_animation_state(self, CONF.ENEMY.ACTIONS.IDLE)
            # Si no ha terminado alguno, NO cambiar estado (bloqueo visual)
        else:
            # 5.3 Comportamiento normal: MOVE si hay velocidad, IDLE si no
            if math.hypot(self.velocity[0], self.velocity[1]) > 1.0:
                set_animation_state(self, CONF.ENEMY.ACTIONS.MOVE)
            else:
                set_animation_state(self, CONF.ENEMY.ACTIONS.IDLE)

        # 6. Actualizar animación actual y efecto
        self.current_animation.update(dt)
        if self.current_effect:
            self.current_effect.update(dt)