from entity.entity_spec import EntitySpec, Stats, Sprite
from .paths import PathsData
import algorithms.algorithms_configs as ALG_CONF
from configs.package import CONF

# Para Kinematic Seek
# - max_speed: velocidad máxima (float)
enemy_seek_kinematic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.SEEK_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.SEEK_KINEMATIC: ALG_CONF.KinematicSeekConfig(
                max_speed=120.0,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Kinematic Flee
# - max_speed: velocidad máxima (float)
enemy_flee_kinematic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*29, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FLEE_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.FLEE_KINEMATIC: ALG_CONF.KinematicFleeConfig(
                max_speed=100.0,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Kinematic Arrive
# - max_speed: velocidad máxima (float)
# - target_radius_dist: radio de llegada (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
enemy_arrive_kinematic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*20, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC: ALG_CONF.KinematicArriveConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                time_to_target=1.2,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Kinematic Wander
# - max_speed: velocidad máxima (float)
# - max_rotation: velocidad angular máxima (float)
enemy_wander_kinematic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_KINEMATIC: ALG_CONF.KinematicWanderConfig(
                max_speed=60.0,
                max_rotation=5.0,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_KINEMATIC: ALG_CONF.KinematicWanderConfig(
                max_speed=60.0,
                max_rotation=5.0,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=3,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_KINEMATIC: ALG_CONF.KinematicWanderConfig(
                max_speed=60.0,
                max_rotation=5.0,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=4,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_KINEMATIC: ALG_CONF.KinematicWanderConfig(
                max_speed=60.0,
                max_rotation=5.0,
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Dynamic Seek
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_seek_dynamic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.SEEK_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.SEEK_DYNAMIC: ALG_CONF.DynamicSeekConfig(
                max_speed=120.0,
                max_acceleration=300.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Dynamic Flee
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_flee_dynamic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*31),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FLEE_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.FLEE_DYNAMIC: ALG_CONF.DynamicFleeConfig(
                max_speed=100.0,
                max_acceleration=300.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Dynamic Arrive
# - max_speed: velocidad máxima (float)
# - target_radius_dist: radio de llegada (float)
# - slow_radius_dist: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
enemy_arrive_dynamic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC: ALG_CONF.DynamicArriveConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.1,
                max_acceleration=300.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Align
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
enemy_align = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.ALIGN,
        alg_configs={
            CONF.ALG.ALGORITHM.ALIGN: ALG_CONF.AlignConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*34, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.ALIGN,
        alg_configs={
            CONF.ALG.ALGORITHM.ALIGN: ALG_CONF.AlignConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Velocity Match
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
enemy_velocity_match = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.VELOCITY_MATCH,
        alg_configs={
            CONF.ALG.ALGORITHM.VELOCITY_MATCH: ALG_CONF.VelocityMatchConfig(
                time_to_target=0.1,
                max_acceleration=350.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.VELOCITY_MATCH,
        alg_configs={
            CONF.ALG.ALGORITHM.VELOCITY_MATCH: ALG_CONF.VelocityMatchConfig(
                time_to_target=0.1,
                max_acceleration=350.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Pursue
# - max_speed: velocidad máxima (float)
# - target_radius_dist: radio de llegada (float)
# - slow_radius_dist: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
# - max_prediction: tiempo máximo de predicción (float)
enemy_pursue = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PURSUE,
        alg_configs={
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Evade
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
# - max_prediction: tiempo máximo de predicción (float)
enemy_evade = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.EVADE,
        alg_configs={
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Face
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
enemy_face = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=3,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*32, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=4,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=5,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*28),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=6,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*32),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=7,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=8,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*32, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=9,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=10,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=11,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*32),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=12,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*28),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Look Where You're Going (Necesita instanciar Evade)
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
# Para Evade
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
# - max_prediction: tiempo máximo de predicción (float)
enemy_look_where = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*29, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=60 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=2.0,
                max_angular_accel=30.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Dynamic Wander
# - max_speed: velocidad máxima (float)
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_acceleration: aceleración máxima (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
# - wander_offset: offset del círculo de wander (float)
# - wander_radius: radio del círculo de wander (float)
# - wander_rate: tasa de cambio de orientación aleatoria (float)
# - wander_orientation: orientación inicial del wander (float)
enemy_wander_dynamic = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-berserker",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*30, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_DYNAMIC: ALG_CONF.DynamicWanderConfig(
                max_speed=100.0,
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=80 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_rotation=4.0,
                max_angular_accel=40.0,
                wander_offset=80.0,
                wander_radius=30.0,
                wander_rate=0.9,
                wander_orientation=0.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*30, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_DYNAMIC: ALG_CONF.DynamicWanderConfig(
                max_speed=100.0,
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=80 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_rotation=4.0,
                max_angular_accel=40.0,
                wander_offset=80.0,
                wander_radius=30.0,
                wander_rate=0.9,
                wander_orientation=0.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=3,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*30, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_DYNAMIC: ALG_CONF.DynamicWanderConfig(
                max_speed=100.0,
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=80 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_rotation=4.0,
                max_angular_accel=40.0,
                wander_offset=80.0,
                wander_radius=30.0,
                wander_rate=0.9,
                wander_orientation=0.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=4,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*30, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        alg_configs={
            CONF.ALG.ALGORITHM.WANDER_DYNAMIC: ALG_CONF.DynamicWanderConfig(
                max_speed=100.0,
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=80 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_rotation=4.0,
                max_angular_accel=40.0,
                wander_offset=80.0,
                wander_radius=30.0,
                wander_rate=0.9,
                wander_orientation=0.0
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

# Para Path Following
# - max_acceleration: aceleración máxima (float)
# - path_instance: instancia del path (Path)
enemy_path_following = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 31),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 29, CONF.MAIN_WIN.RENDER_TILE_SIZE * 29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=3,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 31, CONF.MAIN_WIN.RENDER_TILE_SIZE * 29),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=4,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 40, CONF.MAIN_WIN.RENDER_TILE_SIZE * 40),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=5,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 16, CONF.MAIN_WIN.RENDER_TILE_SIZE * 28),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=6,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 25),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=7,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 35, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=8,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 35),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=9,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 25, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=10,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 16, CONF.MAIN_WIN.RENDER_TILE_SIZE * 38),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
    EntitySpec(
        id=11,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 44, CONF.MAIN_WIN.RENDER_TILE_SIZE * 22),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL0_1
            ),
        },
        statistics=Stats(alive=True, health=100.0,)
    ),
]

enemy_all = [
    enemy_seek_kinematic[0],
    enemy_seek_dynamic[0],
    enemy_arrive_kinematic[0],
    enemy_arrive_dynamic[0],
    enemy_flee_kinematic[0],
    enemy_flee_dynamic[0],
    enemy_wander_kinematic[0],
    enemy_wander_dynamic[0],
    enemy_align[0],
    enemy_velocity_match[0],
    enemy_pursue[0],
    enemy_evade[0],
    enemy_face[0],
    enemy_look_where[0],
    enemy_path_following[0],
    enemy_path_following[6],
]

ALGORITHM_ENEMIES_DATA = {
    CONF.ALG.ALGORITHM.SEEK_KINEMATIC: enemy_seek_kinematic,
    CONF.ALG.ALGORITHM.FLEE_KINEMATIC: enemy_flee_kinematic,
    CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC: enemy_arrive_kinematic,
    CONF.ALG.ALGORITHM.WANDER_KINEMATIC: enemy_wander_kinematic,
    CONF.ALG.ALGORITHM.SEEK_DYNAMIC: enemy_seek_dynamic,
    CONF.ALG.ALGORITHM.FLEE_DYNAMIC: enemy_flee_dynamic,
    CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC: enemy_arrive_dynamic,
    CONF.ALG.ALGORITHM.ALIGN: enemy_align,
    CONF.ALG.ALGORITHM.VELOCITY_MATCH: enemy_velocity_match,
    CONF.ALG.ALGORITHM.PURSUE: enemy_pursue,
    CONF.ALG.ALGORITHM.EVADE: enemy_evade,
    CONF.ALG.ALGORITHM.FACE: enemy_face,
    CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: enemy_look_where,
    CONF.ALG.ALGORITHM.WANDER_DYNAMIC: enemy_wander_dynamic,
    CONF.ALG.ALGORITHM.PATH_FOLLOWING: enemy_path_following,
    "ALL": enemy_all,
    "NOTHING": [],
}