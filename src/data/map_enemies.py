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
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 4, CONF.MAIN_WIN.RENDER_TILE_SIZE * 15),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
        statistics=Stats(alive=True, health=100.0,),
        behavior=BehaviorsData.HUNTER,
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-lord",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 28, CONF.MAIN_WIN.RENDER_TILE_SIZE * 49),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
        statistics=Stats(alive=True, health=100.0,),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=2,
        sprite=Sprite(name="gargant-berserker",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 10, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
        statistics=Stats(alive=True, health=100.0,),
        behavior=BehaviorsData.GUARDIAN,
    ),
    EntitySpec(
        id=4,
        sprite=Sprite(name="gargant-boss",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 55, CONF.MAIN_WIN.RENDER_TILE_SIZE * 47),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.FACE,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                time_to_target=0.1,
                max_rotation=3.0,
                max_angular_accel=35.0
            ),
            CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
        statistics=Stats(alive=True, health=500.0,),
        behavior=BehaviorsData.INVOKER_BOSS,
    ),
    EntitySpec(
        id=5,
        sprite=Sprite(name="gargant-soldier",),
        initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 57, CONF.MAIN_WIN.RENDER_TILE_SIZE * 57),
        collider_box=(CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        initial_algorithm=CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        alg_configs={
            CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING: ALG_CONF.LookWhereYouAreGoingConfig(
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
                target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
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
        statistics=Stats(alive=True, health=100.0,),
        behavior=BehaviorsData.HUNTER,
    ),
]

MAP_ENEMIES_DATA = {
    1 : map_1_group,
    2 : map_2_group,
}
