from configs.package import CONF
from helper.paths import make_circle_path, make_rectangle_path

# Todos los atributos obligatorios para crear un enemigo
# - type: tipo de enemigo (string)
# - position: posición inicial (x, y)
# - collider_box: dimensiones de la caja de colisión (width, height)
# - target: referencia al objeto target (Kinematic)
# - algorithm: algoritmo de movimiento

# Atributos algoritmicos
# - max_speed: velocidad máxima (float)
# - target_radius_dist: radio de llegada (float)
# - slow_radius_dist: radio de desaceleración (float)
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
# - max_rotation: rotación máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
# - max_prediction: máxima predicción (float)  --- SOLO PARA PURSUE Y EVADE ---
# - wander_offset: offset del círculo de wander (float)  --- SOLO PARA WANDER ---
# - wander_radius: radio del círculo de wander (float)  --- SOLO PARA WANDER ---
# - wander_rate: tasa de cambio de orientación aleatoria (float)  --- SOLO PARA WANDER ---
# - wander_orientation: orientación inicial del wander (float)  --- SOLO PARA WANDER ---

# --- Para Kinematic Seek ---
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
enemy_seek_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.SEEK_KINEMATIC,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*29, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FLEE_KINEMATIC,
        "max_speed": 140.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
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
# - target_radius_dist: radio de llegada (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
enemy_arrive_kinematic = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*20, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 1,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*29, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 60.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 5.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
        {
        "type": "gargant-soldier",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 60.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 5.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
        {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 60.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 5.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
        {
        "type": "gargant-boss",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 60.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 5.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
        {
        "type": "gargant-boss",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_KINEMATIC,
        "max_speed": 60.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 5.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.SEEK_DYNAMIC,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*31),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FLEE_DYNAMIC,
        "max_speed": 140.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
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
# - target_radius_dist: radio de llegada (float)
# - slow_radius_dist: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
enemy_arrive_dynamic = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Align
# Atributos relevantes:
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
enemy_align = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*34, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.VELOCITY_MATCH,
        "max_speed": 250.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 550.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-soldier",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.VELOCITY_MATCH,
        "max_speed": 250.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 550.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 1.0,
    },
]

# Para Pursue
# Atributos relevantes:
# - max_speed: velocidad máxima (float)
# - target_radius_dist: radio de llegada (float)
# - slow_radius_dist: radio de desaceleración (float)
# - time_to_target: tiempo para alcanzar el objetivo (float)
# - max_acceleration: aceleración máxima (float)
# - max_prediction: tiempo máximo de predicción (float)
enemy_pursue = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*32, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PURSUE,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 0.5,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*31),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.EVADE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.1,
    },
]

# Para Face
# Atributos relevantes:
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
enemy_face = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*32, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*24),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*28),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*32),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*36, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*32, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*36),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*32),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*24, CONF.MAIN_WIN.RENDER_TILE_SIZE*28),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FACE,
        "max_speed": 180.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
]

# Para Look Where You're Going (junto a Evade)
# Atributos relevantes:
# - target_radius_deg: umbral de orientación (float)
# - slow_radius_deg: umbral de desaceleración (float)
# - time_to_target: tiempo para alcanzar la rotación objetivo (float)
# - max_rotation: velocidad angular máxima (float)
# - max_angular_accel: aceleración angular máxima (float)
enemy_look_where = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*29, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.LOOK_WHERE_YOURE_GOING,
        "max_speed": 200.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
]

# Para Dynamic Wander
# Atributos relevantes:
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
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
    {
        "type": "gargant-soldier",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
    {
        "type": "gargant-boss",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
    {
        "type": "gargant-boss",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*16, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.WANDER_DYNAMIC,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
]

PATH_CONFIGS = {
    "circle" : {
        "type": "circle",
        "params": {"radius": 300.0, "segments": 48, "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30)},
        "offset": 2,
    },
    "rectangle" : {
        "type": "rectangle",
        "params": {"width": 700.0, "height": 700.0, "segments": 70, "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30)},
        "offset": 3,
    },
}

paths_configs = {
    "zone 1" : {
        "radius": 300, 
        "segments": 48, 
        "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        "offset": 2,
    },
    "zone 2" : {
        "width": 700.0, 
        "height": 700.0, 
        "segments": 70, 
        "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        "offset": 3,
    }
}

path_circle = make_circle_path(
   radius=paths_configs["zone 1"]["radius"], 
   center=paths_configs["zone 1"]["center"], 
   segments=paths_configs["zone 1"]["segments"]
)

enemy_follow_path_circle = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 31),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_circle,
        "path_offset": paths_configs["zone 1"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 29, CONF.MAIN_WIN.RENDER_TILE_SIZE * 29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_circle,
        "path_offset": paths_configs["zone 1"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 31, CONF.MAIN_WIN.RENDER_TILE_SIZE * 29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_circle,
        "path_offset": paths_configs["zone 1"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 40, CONF.MAIN_WIN.RENDER_TILE_SIZE * 40),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_circle,
        "path_offset": paths_configs["zone 1"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 16, CONF.MAIN_WIN.RENDER_TILE_SIZE * 28),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_circle,
        "path_offset": paths_configs["zone 1"]["offset"],
    },
]

path_rectangle = make_rectangle_path(
    width=paths_configs["zone 2"]["width"], 
    height=paths_configs["zone 2"]["height"],
    center=paths_configs["zone 2"]["center"], 
    segments=paths_configs["zone 2"]["segments"]
)

enemy_follow_path_rect = [
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 25),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_rectangle,
        "path_offset": paths_configs["zone 2"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 35, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_rectangle,
        "path_offset": paths_configs["zone 2"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 35),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_rectangle,
        "path_offset": paths_configs["zone 2"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 25, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_rectangle,
        "path_offset": paths_configs["zone 2"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 16, CONF.MAIN_WIN.RENDER_TILE_SIZE * 38),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_rectangle,
        "path_offset": paths_configs["zone 2"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 44, CONF.MAIN_WIN.RENDER_TILE_SIZE * 22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_rectangle,
        "path_offset": paths_configs["zone 2"]["offset"],
    },
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
    enemy_follow_path_circle[0],
    enemy_follow_path_rect[0],
]

list_of_enemies_data = {
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
    CONF.ALG.ALGORITHM.PATH_FOLLOWING: enemy_follow_path_circle + enemy_follow_path_rect,
    "ALL": enemy_all,
    "NOTHING": [],
}

paths_1_group = {
    "zone 1" : {
        "radius": 260, 
        "segments": 35, 
        "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 15, 
                   CONF.MAIN_WIN.RENDER_TILE_SIZE * 49 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2),
        "offset": 1,
    },
    "zone 2" : {
        "width": 540.0, 
        "height": 320.0, 
        "segments": 30, 
        "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 9 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                   CONF.MAIN_WIN.RENDER_TILE_SIZE * 6 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
        "offset": 1,
    }
}

path_zone_1 = make_circle_path(
   radius=paths_1_group["zone 1"]["radius"], 
   center=paths_1_group["zone 1"]["center"], 
   segments=paths_1_group["zone 1"]["segments"]
)
path_zone_2 = make_rectangle_path(
    width=paths_1_group["zone 2"]["width"], 
    height=paths_1_group["zone 2"]["height"],
    center=paths_1_group["zone 2"]["center"], 
    segments=paths_1_group["zone 2"]["segments"]
)

HUNTER_BEHAVIOR = {
    "name": "hunter",
    "debug": {
        "show_state_over_entity": True,   # renderer will draw active HSM stack above enemy
        "color_by_level": True
    },
    "params": {
        "vision_range": 400.0,        # px
        "vision_fov_deg": 120.0,      # if your LOS uses FOV
        "attack_range": 48.0,         # px, melee threshold
        "flee_threshold": 0.30,       # health fraction -> enter Huyendo
        "restore_threshold": 0.70,    # health fraction -> restore EstadoVida (deep history)
        "heal_rate_per_sec": 0.05,    # fraction of max_health healed per second (10%/s)
        "safe_distance": 450.0,       # px, distance considered "safe" from player
        "player_lost_timeout": 2.0,   # seconds to wait before switching from Atacar->Cazar when player not visible
        "patrol_path_nodes": 20,      # desired minimum number of navemesh nodes for patrol path
        "face_range_multiplier": 1.5, # multiplier applied to vision_range for Face behaviour (e.g. 1.5 -> 150%) 
        "check_los_throttle": 0.12    # seconds between expensive LOS checks
    },

    # Top-level HSM:
    # Root has three level-1 states: EstadoVida (composite with sub-states), Huyendo, Curarse
    "states": {
        "root": {
            "type": "composite",
            "initial": "EstadoVida",
            "substates": ["EstadoVida", "Huyendo", "Curarse"],
            "entry": ["hsm_noop"],
            "exit": ["hsm_noop"]
        },

        # Nivel 1: Estado de Vida (subMáquina)
        "EstadoVida": {
            "type": "composite",
            "initial": "Cazar",
            "history": "deep",   # enable deep history for this composite
            "substates": ["Cazar", "Atacar"],
            "entry": ["record_last_state_start"],   # optional bookkeeping
            "exit": []
        },

        # Nivel 0 dentro de EstadoVida: Cazar (patrullar / buscar)
        "EstadoVida.Cazar": {
            "type": "leaf",
            "entry": ["start_random_patrol"],   # action: request patrol path / FollowPath
            "update": ["patrol_tick", "throttle_check_player_visibility"],
            "exit": ["stop_patrol"],
            "transitions": [
                {
                    "to": "EstadoVida.Atacar",
                    "cond": "PlayerVisible",
                    "cond_params": {"max_dist_key": "vision_range", "fov_key": "vision_fov_deg"},
                    "priority": 100
                },
                {
                    "to": "Huyendo",
                    "cond": "HealthBelow",
                    "cond_params": {"threshold": "flee_threshold"},
                    "priority": 200
                }
            ]
        },

        # Nivel 0 dentro de EstadoVida: Atacar (perseguir y golpear)
        "EstadoVida.Atacar": {
            "type": "leaf",
            "entry": ["start_pursue_target"],
            "update": ["pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
            "exit": ["stop_pursue"],
            "transitions": [
                {
                    "to": "EstadoVida.Cazar",
                    "cond": "PlayerNotVisibleFor",
                    "cond_params": {"timeout_key": "player_lost_timeout"},
                    "priority": 50
                },
                {
                    "to": "Huyendo",
                    "cond": "HealthBelow",
                    "cond_params": {"threshold": "flee_threshold"},
                    "priority": 200
                }
            ]
        },

        # Nivel 1: Huyendo (evadir)
        "Huyendo": {
            "type": "leaf",
            "entry": ["start_evade_from_player", "set_behavior_flag_fleeing"],
            "update": ["evade_tick", "evaluate_safe_distance"],
            "exit": ["stop_evade", "clear_behavior_flag_fleeing"],
            "transitions": [
                {
                    "to": "Curarse",
                    "cond": "PlayerFarAndNoThreat",
                    "cond_params": {"safe_distance_key": "safe_distance", "no_enemies_radius": 300.0},
                    "priority": 150
                },
                # allow immediate interrupt to Curarse if health is already very low and safe condition met
            ]
        },

        # Nivel 1: Curarse (quedarse estático, Face, curar)
        "Curarse": {
            "type": "leaf",
            "entry": ["face_towards_safe_anchor", "stop_movement", "start_heal_tick"],
            "update": ["face_towards_safe_anchor", "heal_tick", "monitor_player_presence"],
            "exit": ["stop_heal_tick", "clear_safe_anchor"],
            "transitions": [
                {
                    "to": "EstadoVida",
                    "cond": "HealthAbove",
                    "cond_params": {"threshold": "restore_threshold"},
                    "priority": 200,
                    "restore_history": True   # instruct builder/runtime to restore deep history of EstadoVida
                },
                {
                    "to": "Huyendo",
                    "cond": "PlayerVisible",
                    "cond_params": {"max_dist_key": "vision_range"},
                    "priority": 300   # if enemy reappears, interrupt healing and flee
                }
            ]
        }
    },

    # Convenience: map of action keys -> human description (for implementers)
    # (actual implementation will be provided in src/ai/actions.py)
    "actions_doc": {
        "start_random_patrol": "Request pathfinder a random waypoint and attach FollowPath",
        "patrol_tick": "Ensure FollowPath active and refresh if stuck",
        "stop_patrol": "Stop FollowPath and clear waypoint",
        "start_pursue_target": "Start Pursue steering toward last known player",
        "pursue_tick": "Tick pursue steering and update last_known_player_pos",
        "stop_pursue": "Stop pursue steering",
        "try_melee_attack": "If within attack_range attempt attack (use existing attack logic)",
        "start_evade_from_player": "Activate Evade steering using player's predicted position",
        "evade_tick": "Tick evade, update distance checks",
        "stop_evade": "Stop evade steering",
        "face_towards_safe_anchor": "Use Face steering to look toward safe anchor point",
        "stop_movement": "Zero velocities / disable steering outputs",
        "start_heal_tick": "Begin periodic heal that increases health by heal_rate_per_sec",
        "heal_tick": "Apply fractional healing each second",
        "stop_heal_tick": "Stop healing timer",
        "record_last_state_start": "Internal bookkeeping to store last substate on entry"
    },

    # Conditions doc: map cond key -> human description (to implement in src/ai/conditions.py)
    "conditions_doc": {
        "PlayerVisible": "True if player within vision_range and (optional) FOV and LOS",
        "PlayerNotVisibleFor": "True if player hasn't been visible for configured timeout",
        "PlayerFarAndNoThreat": "True if player distance > safe_distance and no other enemies within radius",
        "HealthBelow": "True if entity.health / entity.max_health < threshold (threshold may be key->param)",
        "HealthAbove": "True if entity.health / entity.max_health >= threshold"
    }
}

map_1_group = [
    {
        "type": "gargant-soldier",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*3, CONF.MAIN_WIN.RENDER_TILE_SIZE*16),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PURSUE,
        "max_speed": 120.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
        "behavior": HUNTER_BEHAVIOR,
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 28, CONF.MAIN_WIN.RENDER_TILE_SIZE * 49),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 320.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_zone_1,
        "path_offset": paths_1_group["zone 1"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 10, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 180.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 320.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path": path_zone_2,
        "path_offset": paths_1_group["zone 2"]["offset"],
    },
]

map_2_group = map_1_group

map_levels_enemies_data = {
    1 : map_1_group,
    2 : map_2_group,
}
