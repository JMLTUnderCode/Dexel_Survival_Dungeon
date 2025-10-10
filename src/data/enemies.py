import pygame
from utils.configs import *

enemy_list = [
    {
        "type": "gargant-berserker",                                            # *
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),                 # *
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),  # *
        "algorithm": ALGORITHM.SEEK,                                            # *
        "maxSpeed": 180.0,                                                      # *
        "target_radius": 40.0,                                                  # *
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",                                              # *
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),                 # *
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),  # *
        "algorithm": ALGORITHM.ARRIVE_KINEMATIC,                                # *
        "maxSpeed": 180.0,                                                      # *
        "target_radius": 40.0,                                                  # *
        "slow_radius": 180.0,
        "time_to_target": 0.15,                                                 # *
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",                                              # *
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),                 # *
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),  # *
        "algorithm": ALGORITHM.ARRIVE_DINAMIC,                                  # *
        "maxSpeed": 180.0,                                                      # *
        "target_radius": 40.0,                                                  # *
        "slow_radius": 180.0,                                                   # *
        "time_to_target": 0.15,                                                 # *
        "max_acceleration": 300.0,                                              # *
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),                 # *
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),  # *
        "algorithm": ALGORITHM.WANDER,                                          # *
        "maxSpeed": 120.0,                                                      # *
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.7,                                                    # *
    },
]