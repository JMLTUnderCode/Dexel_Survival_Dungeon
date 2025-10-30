import math
import pygame
from typing import Union
from kinematics.kinematic import Kinematic, SteeringOutput, KinematicSteeringOutput
from kinematics.kinematic_seek import KinematicSeek
from kinematics.kinematic_flee import KinematicFlee
from kinematics.kinematic_arrive import KinematicArrive
from kinematics.kinematic_wander import KinematicWander
from kinematics.dynamic_seek import DynamicSeek
from kinematics.dynamic_flee import DynamicFlee
from kinematics.dynamic_arrive import DynamicArrive
from kinematics.dynamic_wander import DynamicWander
from kinematics.align import Align
from kinematics.velocity_match import VelocityMatch
from kinematics.pursue import Pursue
from kinematics.evade import Evade
from kinematics.face import Face
from kinematics.look_where_youre_going import LookWhereYoureGoing
from kinematics.path_following import FollowPath
from helper.paths import make_circle_path, make_rectangle_path
from characters.animation import Animation, load_animations, set_animation_state
from configs.package import CONF

class Enemy(Kinematic):
    """
    Clase que representa un enemigo que persigue al jugador.
    Atributos:
        type: tipo de enemigo (puede usarse para diferentes sprites o comportamientos)
        position: posición inicial del enemigo (x, y)
        collider_box: dimensiones de la caja de colisión del enemigo (ancho, alto)
        target: referencia al objeto target (objetivo a seguir)
        algorithm: algoritmo de búsqueda cinemática ("ARRIVE" o "SEEK")
        max_speed: velocidad máxima del enemigo
        target_radius: radio de llegada al objetivo
        slow_radius: radio de desaceleración
        time_to_target: tiempo para alcanzar el objetivo
        max_acceleration: aceleración máxima permitida (unidades/segundo²)
        max_rotation: velocidad angular máxima (radianes/segundo)
        max_angular_accel: aceleración angular máxima (radianes/segundo²)

    Algoritmos:
        - KinematicSeek: Persigue al objetivo de manera directa.
        - KinematicFlee: Huye del objetivo.
        - KinematicArrive: Llega suavemente al objetivo.
        - KinematicWander: Se mueve aleatoriamente.
        - DynamicSeek: Persigue al objetivo con aceleración.
        - DynamicFlee: Huye del objetivo con aceleración.
        - DynamicArrive: Llega suavemente al objetivo con aceleración.
        - DynamicWander: Se mueve aleatoriamente con aceleración.
        - Align: Alinea la orientación con el objetivo.
        - VelocityMatch: Igualar la velocidad con el objetivo.
        - Pursue: Persigue al objetivo anticipando su movimiento.
        - Evade: Huye del objetivo anticipando su movimiento.
        - Face: Gira para mirar al objetivo.
        - LookWhereYoureGoing: Gira en la dirección del movimiento.
    """
    def __init__(
        self, 
        type: str, 
        position: tuple,
        collider_box: tuple[int, int],
        target: Kinematic, 
        algorithm: str, 
        max_speed: float = 200.0, 
        target_radius: float = 40.0, 
        slow_radius: float = 150.0, 
        time_to_target: float = 0.15,
        max_acceleration: float = 300.0,
        max_rotation: float = 1.0,
        max_angular_accel: float = 8.0,
        max_prediction: float = 1.0, 
        path_type: str = None,
        path_params: dict = None,
        path_offset: float = 12.0,
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
        self.max_speed = max_speed

        # Instanciar atributos de animación
        self.state = CONF.ENEMY.ACTIONS.MOVE
        self.animations : dict[str, Animation] = load_animations(
            dir=CONF.ENEMY.FOLDER, 
            type=self.type, 
            states_anims=CONF.ENEMY.ACTIONS, 
            w_tile=CONF.ENEMY.TILE_WIDTH, 
            h_tile=CONF.ENEMY.TILE_HEIGHT,
            frame_duration=0.12,
            scale=1.25
        )
        self.current_animation : Animation = self.animations[self.state]
        self.collider_box = collider_box

        # Instanciar algoritmos cinemáticos.
        self.kinematic_seek = KinematicSeek(
            character=self,                    # Kinematic que se mueve
            target=target,                     # Objetivo a seguir
            max_speed=max_speed                # Velocidad máxima
        )
        self.kinematic_flee = KinematicFlee(
            character=self,                    # Kinematic que se mueve
            target=target,                     # Objetivo a seguir
            max_speed=max_speed                # Velocidad máxima
        )
        self.kinematic_arrive = KinematicArrive(
            character=self,                    # Kinematic que se mueve
            target=target,                     # Objetivo a seguir
            max_speed=max_speed,               # Velocidad máxima
            target_radius=target_radius,       # Radio de llegada
            time_to_target=time_to_target      # Tiempo para ajustar la velocidad
        )
        self.kinematic_wander = KinematicWander(
            character=self,                    # Kinematic que se mueve
            max_speed=max_speed,               # Velocidad máxima
            max_rotation=max_rotation          # Velocidad angular máxima
        )

        # Instanciar el algoritmos dinámicos.
        self.dynamic_seek = DynamicSeek(
            character=self,                    # Kinematic que se mueve
            target=target,                     # Objetivo a seguir
            max_acceleration=max_acceleration  # Aceleración máxima
        )
        self.dynamic_flee = DynamicFlee(
            character=self,                    # Kinematic que se mueve
            target=target,                     # Objetivo a seguir
            max_acceleration=max_acceleration  # Aceleración máxima
        )
        self.dynamic_arrive = DynamicArrive(
            character=self,                    # Kinematic que se mueve
            target=target,                     # Objetivo a seguir
            max_speed=max_speed,               # Velocidad máxima
            target_radius=target_radius,       # Radio de llegada
            slow_radius=slow_radius,           # Radio para empezar a desacelerar
            time_to_target=time_to_target,     # Tiempo para ajustar la velocidad
            max_acceleration=max_acceleration  # Aceleración máxima
        )
        self.dynamic_wander = DynamicWander(
            character=self,                      # Kinematic que se mueve
            target=target,                       # Objetivo a seguir (no se usa realmente)
            target_radius=target_radius,         # Radio de llegada (para Face interno)
            slow_radius=slow_radius,             # Radio para empezar a girar (para Face interno)
            time_to_target=time_to_target,       # Tiempo para ajustar la rotación (para Face interno)
            max_acceleration=max_acceleration,   # Aceleración máxima
            max_rotation=max_rotation,           # Velocidad angular máxima (para Face interno)
            max_angular_accel=max_angular_accel, # Aceleración angular máxima (para Face interno)
            wander_offset=80.0,                  # Offset del círculo de wander
            wander_radius=20.0,                  # Radio del círculo de wander
            wander_rate=0.9,                     # Tasa de cambio de orientación aleatoria
            wander_orientation=0.0               # Orientación inicial del wander
        )

        # Instanciar el algoritmo de alineación
        self.align = Align(
            character=self,                     # Quien se alinea
            target=target,                      # Referencia para alinearse
            target_radius=target_radius,        # Radio de llegada
            slow_radius=slow_radius,            # Radio para empezar a girar
            time_to_target=time_to_target,      # Tiempo para ajustar la rotación
            max_rotation=max_rotation,          # Velocidad angular máxima
            max_angular_accel=max_angular_accel # Aceleración angular máxima
        )

        # Instanciar el algoritmo de velocity matching
        self.velocity_match = VelocityMatch(
            character=self,
            target=target,
            max_acceleration=max_acceleration,
            time_to_target=time_to_target
        )

        # Instanciar el algoritmo de persecución
        self.pursue = Pursue(
            character=self,
            target=target,
            max_speed=max_speed,
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_acceleration=max_acceleration,
            max_prediction=max_prediction
        )

        # Instanciar el algoritmo de evasión
        self.evade = Evade(
            character=self,
            target=target,
            max_acceleration=max_acceleration,
            max_prediction=max_prediction
        )

        # Instanciar el algoritmo de Face
        self.face = Face(
            character=self,
            target=target,
            target_radius=target_radius,
            slow_radius=slow_radius,
            time_to_target=time_to_target,
            max_rotation=max_rotation,
            max_angular_accel=max_angular_accel,
        )

        # Instanciar el algoritmo de Look Where You're Going
        self.look_where = LookWhereYoureGoing(
            character=self,                      # Quien se alinea
            target=target,                       # Referencia para alinearse
            target_radius=target_radius,         # Radio de llegada
            slow_radius=slow_radius,             # Radio para empezar a girar
            time_to_target=time_to_target,       # Tiempo para ajustar la rotación
            max_rotation=max_rotation,           # Velocidad angular máxima
            max_angular_accel=max_angular_accel, # Aceleración angular máxima
        )

        # FOLLOW_PATH: build Path (if requested in preset) and FollowPath delegate
        self.follow_path = None
        if algorithm == CONF.ALG.ALGORITHM.PATH_FOLLOWING:
            # build path based on descriptor passed in preset (safe defaults)
            try:
                if path_type == "circle":
                    center = tuple(path_params.get("center", self.position))
                    radius = float(path_params.get("radius", 100.0))
                    segments = int(path_params.get("segments", 48))
                    path = make_circle_path(radius=radius, center=center, segments=segments)
                elif path_type == "rectangle" or path_type == "rect":
                    center = tuple(path_params.get("center", self.position))
                    width = float(path_params.get("width", 100.0))
                    height = float(path_params.get("height", 100.0))
                    segments = int(path_params.get("segments", 48))
                    path = make_rectangle_path(width=width, height=height, center=center, segments=segments)
                else:
                    # fallback: single-point circle around spawn
                    path = make_circle_path(radius=float(path_params.get("radius", 100.0)) if path_params else 100.0, center=self.position)
            except Exception:
                path = make_circle_path(radius=100.0, center=self.position)

            # instantiate FollowPath delegate
            self.follow_path = FollowPath(
                character=self, 
                path=path, 
                path_offset=path_offset, 
                current_param=0.0,
                max_acceleration=max_acceleration
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

        if CONF.DEV.DEBUG:
            # Mostrar arriba del sprite el algoritmo activo en VERDE, NEGRITA y MAYÚSCULAS
            # Cachear la fuente en la clase para no recrearla cada frame
            if not hasattr(self.__class__, "_dev_font") or self.__class__._dev_font is None:
                try:
                    self.__class__._dev_font = pygame.font.SysFont(None, 18, bold=True)
                except pygame.error:
                    # Fallback si SysFont falla (no se puede poner en negrita con Font)
                    self.__class__._dev_font = pygame.font.Font(None, 18)

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

            if hasattr(self, "follow_path") and self.follow_path is not None:
                path = getattr(self.follow_path, "path", None)
                if path is not None:
                    # Path.draw espera surface, camera_x, camera_z, opcionales...
                    path.draw(surface, camera_x, camera_z, color=(255,200,0), width=2)

    def draw_collision_box(self, surface: pygame.Surface, camera_x: float, camera_z: float):
        """
        Dibuja el cuadro de colisión del enemigo para depuración.
        """
        sx = self.position[0] - camera_x
        sz = self.position[1] - camera_z
        enemy_box = pygame.Rect(
            int(sx - self.collider_box[0] // 2),
            int(sz - self.collider_box[1] // 2),
            int(self.collider_box[0]),
            int(self.collider_box[1])
        )
        pygame.draw.rect(surface, (0, 255, 0), enemy_box, 1)  # Verde, grosor 1

    def update(self, collision_rects: list[pygame.Rect], dt: float):
        """
        Actualiza la posición, velocidad y orientación del enemigo para perseguir al jugador.
        Utiliza el algoritmo de movimiento especificado en "algorithm" para calcular el steering adecuado.
        """
        # Calcular el steering según el algoritmo seleccionado
        steering: Union[SteeringOutput, KinematicSteeringOutput] = SteeringOutput(linear=(0, 0), angular=0)
        match (self.algorithm):
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
                # Combinar ambos steerings: usar linear de evade y angular de lwyg
                steering = SteeringOutput(
                    linear=steering_evade.linear,
                    angular=steering_lwyg.angular
                )
            case CONF.ALG.ALGORITHM.PATH_FOLLOWING:
                steering = self.follow_path.get_steering()

        # Aplicar el steering y actualizar la cinemática
        if isinstance(steering, SteeringOutput):
            if self.algorithm in (CONF.ALG.ALGORITHM.ALIGN, CONF.ALG.ALGORITHM.FACE):
                set_animation_state(self, CONF.ENEMY.ACTIONS.ATTACK_WOUNDED)
                # Align devuelve angular steering; para align la parte linear suele ser (0,0)
                if steering.angular != 0.0:
                    # aplicar como aceleración angular
                    self.update_by_dynamic(steering, self.max_speed, dt, collision_rects, self.collider_box, self.algorithm)
            else:
                if steering.linear != (0, 0):
                    set_animation_state(self, CONF.ENEMY.ACTIONS.MOVE)
                    self.update_by_dynamic(steering, self.max_speed, dt, collision_rects, self.collider_box, self.algorithm)
                else:
                    set_animation_state(self, CONF.ENEMY.ACTIONS.ATTACK)

        elif isinstance(steering, KinematicSteeringOutput):
            if steering.velocity != (0, 0):
                set_animation_state(self, CONF.ENEMY.ACTIONS.MOVE)
                self.update_by_kinematic(steering, dt, collision_rects, self.collider_box, self.algorithm)
            else:
                set_animation_state(self, CONF.ENEMY.ACTIONS.ATTACK)

        self.current_animation.update(dt)      # Actualizar animación