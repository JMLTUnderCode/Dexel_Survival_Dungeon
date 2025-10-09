from utils.configs import *

enemy_list = [
    {
        "type": "gargant-soldier", 
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "algorithm": ALGORITHM.ARRIVE,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "algorithm": ALGORITHM.SEEK,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "algorithm": ALGORITHM.WANDER,
        "maxSpeed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_rotation": 1.7,
    },
]