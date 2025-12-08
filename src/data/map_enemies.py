from entity.entity_spec import EntitySpec, Stats, Sprite
from .behaviors import BehaviorsData
from .paths import PathsData
import algorithms.algorithms_configs as ALG_CONF
from configs.package import CONF

map_1_group = [

]

map_2_group = [
    EntitySpec(
        id=1,
        sprite=Sprite(name="gargant-lord", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 20, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_1
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-lord", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 33, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_2
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=3,
        sprite=Sprite(name="gargant-lord", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 52, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_3
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=4,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 27, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_4
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=5,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 17, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=6,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 7, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_6
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=7,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 37, CONF.MAIN_WIN.RENDER_TILE_SIZE * 41),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL2_1
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=8,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 37, CONF.MAIN_WIN.RENDER_TILE_SIZE * 58),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL2_1
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=9,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 13, CONF.MAIN_WIN.RENDER_TILE_SIZE * 58),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL2_1
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=10,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 13, CONF.MAIN_WIN.RENDER_TILE_SIZE * 41),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.CIRCLE_ZONE_LEVEL2_1
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=11,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 64, CONF.MAIN_WIN.RENDER_TILE_SIZE * 47),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_7
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=12,
        sprite=Sprite(name="gargant-berserker", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 44, CONF.MAIN_WIN.RENDER_TILE_SIZE * 47),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.PATH_FOLLOWING: ALG_CONF.PathFollowingConfig(
                max_acceleration=200.0,
                path_instance=PathsData.RECT_ZONE_LEVEL2_7
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=13,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 52, CONF.MAIN_WIN.RENDER_TILE_SIZE * 6),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=14,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 62, CONF.MAIN_WIN.RENDER_TILE_SIZE * 32),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=15,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 15, CONF.MAIN_WIN.RENDER_TILE_SIZE * 20),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=16,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 4, CONF.MAIN_WIN.RENDER_TILE_SIZE * 42),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=17,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 65, CONF.MAIN_WIN.RENDER_TILE_SIZE * 55),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=18,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 15, CONF.MAIN_WIN.RENDER_TILE_SIZE * 67),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=19,
        sprite=Sprite(name="gargant-soldier", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 15, CONF.MAIN_WIN.RENDER_TILE_SIZE * 77),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.EVADE: ALG_CONF.EvadeConfig(
                max_speed=100.0,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=100.0, mele_dmg=10.0, mele_cooldown=1.4),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=20,
        sprite=Sprite(name="gargant-boss", frame_duration=0.11,),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 48, CONF.MAIN_WIN.RENDER_TILE_SIZE * 68),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=1 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.PURSUE: ALG_CONF.PursueConfig(
                max_speed=120.0,
                target_radius_dist=40.0,
                slow_radius_dist=160.0,
                time_to_target=0.15,
                max_acceleration=300.0,
                max_prediction=0.5
            ),
            CONF.ALG.ALGORITHM.TEMP_PATH_FOLLOWING: ALG_CONF.TempPathFollowingConfig(
                path_offset=1.0
            )
        },
        statistics=Stats(alive=True, health=500.0, mele_dmg=30.0, mele_cooldown=1.4, magic_dmg=35.0, magic_cooldown=1.6),
        behavior=BehaviorsData.INVOKER_BOSS,
    ),
]

MAP_ENEMIES_DATA = {
    1 : map_1_group,
    2 : map_2_group,
}
