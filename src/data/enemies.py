import math
import utils.configs as configs

# Todos los atributos obligatorios para crear un enemigo
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento

# Atributos algoritmicos
# - max_speed: velocidad máxima (float)
# - target_radius: radio de llegada (float)
# - slow_radius: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
# - max_rotation: rotación máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
# - "max_prediction": máxima predicción (float)  --- SOLO PARA PURSUE Y EVADE ---

# --- Para Kinematic Seek ---
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
enemy_seek_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# --- Para Dynamic Seek ---
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_seek_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.SEEK_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Kinematic Arrive
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - target_radius: radio de llegada (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
enemy_arrive_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_KINEMATIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Dynamic Arrive
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - target_radius: radio de llegada (float)
# - slow_radius: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
enemy_arrive_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Kinematic Flee
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
enemy_flee_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_KINEMATIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_KINEMATIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_KINEMATIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_KINEMATIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Dynamic Flee
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
enemy_flee_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_DYNAMIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_DYNAMIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_DYNAMIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.FLEE_DYNAMIC,
        "max_speed": 100.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Kinematic Wander
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - max_rotation: velocidad angular máxima (float)
enemy_wander_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Dynamic Wander
# Atributos relevantes:

enemy_wander_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 120.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 15.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Align
# Atributos relevantes:
# - target_radius: umbral de orientación (float)
# - slow_radius: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
enemy_align = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius": 5 * (math.pi / 180),  # 5 grados en radianes
        "slow_radius": 45 * (math.pi / 180),   # 45 grados en radianes
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 6.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius": 5 * (math.pi / 180),  # 5 grados en radianes
        "slow_radius": 45 * (math.pi / 180),   # 45 grados en radianes
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 6.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius": 5 * (math.pi / 180),  # 5 grados en radianes
        "slow_radius": 45 * (math.pi / 180),   # 45 grados en radianes
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 6.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius": 5 * (math.pi / 180),  # 5 grados en radianes
        "slow_radius": 45 * (math.pi / 180),   # 45 grados en radianes
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 6.0,
        "max_prediction": 1.0,
    },
]

# Para Velocity Match
# Atributos relevantes:
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
enemy_velocity_match = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.VELOCITY_MATCH,
        "max_speed": 210.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.VELOCITY_MATCH,
        "max_speed": 210.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-lord",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.VELOCITY_MATCH,
        "max_speed": 210.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-boss",
        "position": (configs.RENDER_TILE_SIZE*40, configs.RENDER_TILE_SIZE*40),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.VELOCITY_MATCH,
        "max_speed": 210.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Pursue
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - target_radius: radio de llegada (float)
# - slow_radius: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
# - max_prediction: tiempo máximo de predicción (float)
enemy_pursue = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.PURSUE,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 0.5,
    },
]

# Para Evade
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - max_acceleration: aceleración máxima (float)
# - max_prediction: tiempo máximo de predicción (float)
enemy_evade = [
    {
        "type": "gargant-berserker",
        "position": (configs.RENDER_TILE_SIZE*26, configs.RENDER_TILE_SIZE*26),
        "collider_box": (configs.ENEMY_COLLIDER_BOX_WIDTH, configs.ENEMY_COLLIDER_BOX_HEIGHT),
        "algorithm": configs.ALGORITHM.EVADE,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 0.5,
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
    #enemy_wander_dynamic[3],
    enemy_align[0],
    enemy_velocity_match[1],
    enemy_pursue[0],
    enemy_evade[0],
]

list_of_enemies_data = {
    configs.ALGORITHM.SEEK_KINEMATIC: enemy_seek_kinematic,
    configs.ALGORITHM.FLEE_KINEMATIC: enemy_flee_kinematic,
    configs.ALGORITHM.ARRIVE_KINEMATIC: enemy_arrive_kinematic,
    configs.ALGORITHM.WANDER_KINEMATIC: enemy_wander_kinematic,
    configs.ALGORITHM.SEEK_DYNAMIC: enemy_seek_dynamic,
    configs.ALGORITHM.FLEE_DYNAMIC: enemy_flee_dynamic,
    configs.ALGORITHM.ARRIVE_DYNAMIC: enemy_arrive_dynamic,
    configs.ALGORITHM.WANDER_DYNAMIC: enemy_wander_dynamic,
    configs.ALGORITHM.ALIGN: enemy_align,
    configs.ALGORITHM.VELOCITY_MATCH: enemy_velocity_match,
    configs.ALGORITHM.PURSUE: enemy_pursue,
    configs.ALGORITHM.EVADE: enemy_evade,
    "ALL": enemy_all,
    "EMPTY": [],
}