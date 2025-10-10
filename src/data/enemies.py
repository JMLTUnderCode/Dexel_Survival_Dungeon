from utils.configs import *

# Para Kinematic Seek
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
enemy_seek_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_KINEMATIC,
        "maxSpeed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.7,
    },
]

# Para Dynamic Seek
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_seek_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.SEEK_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
]

# Para Kinematic Arrive
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
# - target_radius: radio de llegada (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
enemy_arrive_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_KINEMATIC,
        "maxSpeed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.7,
    },
]

# Para Dynamic Arrive
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
# - target_radius: radio de llegada (float)
# - slow_radius: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
enemy_arrive_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.ARRIVE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
]

# Para Kinematic Flee
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
enemy_flee_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_KINEMATIC,
        "maxSpeed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.7,
    },
]

# Para Dynamic Flee
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_flee_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.FLEE_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
]

# Para Kinematic Wander
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
# - max_rotation: velocidad angular máxima (float)
enemy_wander_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_KINEMATIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_KINEMATIC,
        "maxSpeed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.7,
    },
]

# Para Dynamic Wander
# Atributos relevantes:
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - algorithm: algoritmo de movimiento (ALGORITHM.SEEK_KINEMATIC)
# - maxSpeed: velocidad máxima (float)
# - max_rotation: velocidad angular máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_wander_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*26),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (RENDER_TILE_SIZE*26, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_DYNAMIC,
        "maxSpeed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (RENDER_TILE_SIZE*40, RENDER_TILE_SIZE*40),
        "collider_box": (ENEMY_COLLIDER_BOX_WIDTH, ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": ALGORITHM.WANDER_DYNAMIC,
        "maxSpeed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.7,
    },
]

enemy_all = [
    enemy_seek_kinematic[0],
    enemy_seek_dynamic[1],
    enemy_arrive_kinematic[2],
    enemy_arrive_dynamic[3],
    enemy_flee_kinematic[0],
    enemy_flee_dynamic[1],
    enemy_wander_kinematic[2],
    #enemy_wander_dynamic[1]
]

list_of_enemies_data = {
    ALGORITHM.SEEK_KINEMATIC: enemy_seek_kinematic,
    ALGORITHM.SEEK_DYNAMIC: enemy_seek_dynamic,
    ALGORITHM.ARRIVE_KINEMATIC: enemy_arrive_kinematic,
    ALGORITHM.ARRIVE_DYNAMIC: enemy_arrive_dynamic,
    ALGORITHM.FLEE_KINEMATIC: enemy_flee_kinematic,
    ALGORITHM.FLEE_DYNAMIC: enemy_flee_dynamic,
    ALGORITHM.WANDER_KINEMATIC: enemy_wander_kinematic,
    ALGORITHM.WANDER_DYNAMIC: enemy_wander_dynamic,
    "ALL": enemy_all
}