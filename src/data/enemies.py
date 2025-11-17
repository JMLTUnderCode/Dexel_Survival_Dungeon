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

"""
DOCUMENTACIÓN: HUNTER_BEHAVIOR

Resumen
    Comportamiento 'hunter' (cazador) para enemigos. Diseñado como una HSM (máquina de estados
    jerárquica) con tres estados de alto nivel: EstadoVida (submáquina: Cazar/Atacar), Huyendo y Curarse.
    Objetivo: patrullar/buscar al jugador, perseguir y atacar si se detecta, huir cuando la vida es baja,
    y curarse/esperar en un anchor seguro hasta recuperarse.

Parámetros principales (params)
    - vision_range (px): distancia máxima para ver al jugador.
    - vision_fov_deg (deg): ángulo del cono de visión.
    - attack_range (px): distancia de melee/ataque.
    - flee_threshold (0..1): fracción de vida para entrar en Huyendo.
    - restore_threshold (0..1): fracción de vida para salir de Curarse (restaurar historial).
    - heal_rate_per_sec: fracción de max_health curada por segundo durante Curarse.
    - safe_distance (px): distancia objetivo para calcular safe_anchor (sitio seguro).
    - player_lost_timeout (s): tiempo para considerar que el jugador se perdió.
    - patrol_path_nodes (int): número mínimo de nodos deseados para patrulla aleatoria.
    - face_range_multiplier: multiplica vision_range para decidir cuándo "mirar" al jugador.
    - check_los_throttle (s): throttling para checks de línea de visión.

Estados y semántica
  - EstadoVida (composite, history=deep)
    - Subestados: Cazar (patrullar / vigilar), Atacar (perseguir / golpear)
    - Guarda historial profundo para restaurar comportamiento tras Curarse.

  - EstadoVida.Cazar (Vigilar / patrullar)
    - Patrulla (navmesh o ruta aleatoria) y chequea visibilidad del jugador.
    - No sustituye la ruta guardian (si existe) a menos que corresponda.

  - EstadoVida.Atacar
    - Persecución activa del jugador; intenta ataques cuerpo a cuerpo en rango.
    - Si se pierde visión por un tiempo, vuelve a patrullar.

  - Huyendo
    - Evadir cuando hp bajo. Guarda prev_algorithm para restaurar.
    - Monitoriza distancia al jugador para decidir cuándo detener huida.

  - Curarse
    - Permanece estático (o mirando hacia jugador/anchor), se cura progresivamente.
    - Monitoriza presencia del jugador para interrumpir si aparece amenaza.

Transiciones críticas (resumen práctico)
    - Vigilar + PlayerVisible -> Atacar
    - Vigilar + IsFarFromProtectionZone -> RegresarAZona (si hay path guardian)
    - Atacar + PlayerNotVisibleFor + IsAtProtectionZone -> Vigilar
    - Atacar + PlayerNotVisibleFor + IsFarFromProtectionZone -> RegresarAZona
    - RegresarAZona + IsAtProtectionZone -> Vigilar
    - RegresarAZona + PlayerVisible -> Atacar
    - Huyendo + PlayerFar -> Curarse
    - Curarse + PlayerVisible -> Huyendo
    - Curarse + HealthAbove -> EstadoVida (restaurando historial previo)
"""
HUNTER_BEHAVIOR = {
    "name": "hunter",
    "debug": {"show_state_over_entity": True},
    "params": {
        "vision_range": 300.0,
        "vision_fov_deg": 120.0,
        "attack_range": 48.0,
        "flee_threshold": 0.30,
        "restore_threshold": 0.70,
        "heal_rate_per_sec": 0.05,
        "safe_distance": 450.0,
        "player_lost_timeout": 2.0,
        "patrol_path_nodes": 20,
        "face_range_multiplier": 2,
        "check_los_throttle": 0.12
    },
    "root": "EstadoVida",
    "states": {
        # Nivel 1: EstadoVida (subMáquina)
        "EstadoVida": {
            "type": "composite",
            "initial": "Cazar",
            "history": "deep",
            "substates": ["Cazar", "Atacar"],
            "entry": ["record_last_state_start"],
            "exit": [],
            "transitions": [
                # Si la vida baja, huir
                {"to": "Huyendo", "cond": "HealthBelow", "priority": 200}
            ]
        },

        # Nivel 0: EstadoVida.Cazar (patrullar / buscar)
        "EstadoVida.Cazar": {
            "type": "leaf",
            "entry": ["start_random_patrol"],
            "update": ["patrol_tick", "throttle_check_player_visibility"],
            "exit": ["stop_patrol"],
            "transitions": [
                # Si el jugador es visible, atacar
                {"to": "EstadoVida.Atacar", "cond": "PlayerVisible", "priority": 100},
            ]
        },

        # Nivel 0: EstadoVida.Atacar (perseguir y golpear)
        "EstadoVida.Atacar": {
            "type": "leaf",
            "entry": ["start_pursue_target"],
            "update": ["pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
            "exit": ["stop_pursue"],
            "transitions": [
                # Si el jugador no es visible por un tiempo, volver a cazar
                {"to": "EstadoVida.Cazar", "cond": "PlayerNotVisibleFor", "priority": 100},
            ]
        },

        # Nivel 1: Huyendo (evadir al enemigo)
        "Huyendo": {
            "type": "leaf",
            "entry": ["start_evade_from_player", "set_behavior_flag_fleeing"],
            "update": ["evade_tick"],
            "exit": ["stop_evade", "clear_behavior_flag_fleeing"],
            "transitions": [
                # Si el jugador está lejos, pasar a curarse
                {"to": "Curarse", "cond": "PlayerFar", "priority": 200}
            ]
        },

        # Nivel 1: Curarse (quedarse estático, Face al enemigo, curarse)
        "Curarse": {
            "type": "leaf",
            "entry": ["face_towards_safe_anchor", "stop_movement", "start_heal_tick"],
            "update": ["face_towards_safe_anchor", "heal_tick", "monitor_player_presence"],
            "exit": ["stop_heal_tick", "clear_safe_anchor"],
            "transitions": [
                # Si la entidad se ha recuperado suficiente vida
                {"to": "EstadoVida", "cond": "HealthAbove", "priority": 300, "restore_history": True},
                # Si el jugador aparece mientras se cura
                {"to": "Huyendo", "cond": "PlayerVisible", "priority": 600}
            ]
        },
    },
}

"""
DOCUMENTACIÓN: GUARDIAN_BEHAVIOR

Resumen
    Comportamiento 'guardian' para enemigos. Diseñado para proteger un camino (PolylinePath)
    que representa la "zona" defendida. El guardian patrulla sobre un path definido (si existe)
    y gestiona retorno cuando se aleja del camino. Si no hay path, se comporta como patrulla
    aleatoria. Incluye lógica de persecución/ataque, huida y curado similar a HUNTER pero
    con énfasis en mantener/volver al path protegido.

Parámetros principales (params)
    - vision_range (px): distancia máxima para ver al jugador.
    - vision_fov_deg (deg): ángulo del cono de visión.
    - attack_range (px): distancia de melee/ataque.
    - flee_threshold (0..1): fracción de vida para entrar en Huyendo.
    - restore_threshold (0..1): fracción de vida para salir de Curarse.
    - heal_rate_per_sec: fracción de max_health curada por segundo durante Curarse.
    - safe_distance (px): distancia objetivo para calcular safe_anchor (sitio seguro).
    - player_lost_timeout (s): tiempo para considerar que el jugador se perdió.
    - patrol_path_nodes (int): nodos deseados para patrulla aleatoria.
    - face_range_multiplier: multiplica vision_range para decidir cuándo "mirar" al jugador.
    - check_los_throttle (s): throttling para checks de línea de visión.
    - protection_margin (px): distancia al punto MÁS CERCANO del PolylinePath que define
        si la entidad está "sobre" su ruta patrulla (p.ej. 40 px).
    - arrival_threshold (px): umbral de llegada usado por la ruta de retorno (p.ej. 40 px).

Estados y semántica
  - EstadoVida (composite, history=deep)
    - Subestados: Vigilar, Atacar, RegresarAZona
    - Guarda historial profundo para restaurar comportamiento tras Curarse.

  - EstadoVida.Vigilar (Patrulla guardian / Vigilar)
    - Si la entidad tiene un PolylinePath (entity.path) lo usa como ruta guardian.
    - is_on_guardian_path = True indica que la entidad sigue el path protegido.
    - Si la entidad se aleja más que protection_margin del punto MÁS CERCANO del path,
      la condición IsFarFromProtectionZone dispara el retorno.

  - EstadoVida.Atacar
    - Igual que hunter: perseguir y atacar, pero al perder objetivo decide volver
      al path guardian si está lejos de él.

  - EstadoVida.RegresarAZona (volver al camino protegido)
    - Genera un FollowPath temporal (entity.temp_follow_path) desde la posición actual
      hacia el punto MÁS CERCANO del PolylinePath guardian_original_path.
    - Usa arrival_threshold para decidir llegada por proximidad; al llegar restaura
      PATH_FOLLOWING sobre el path guardian.

  - Huyendo
    - Evadir cuando hp bajo. Guarda prev_algorithm para restaurar.
    - Monitoriza distancia al jugador para decidir cuándo detener huida.

  - Curarse
    - Permanece estático (o mirando hacia jugador/anchor), se cura progresivamente.
    - Monitoriza presencia del jugador para interrumpir si aparece amenaza.

Transiciones críticas (resumen práctico)
    - Vigilar + PlayerVisible -> Atacar
    - Vigilar + IsFarFromProtectionZone -> RegresarAZona
    - Atacar + PlayerNotVisibleAndAtProtectionZone -> Vigilar
    - Atacar + PlayerNotVisibleAndFarFromProtectionZone -> RegresarAZona
    - RegresarAZona + IsAtProtectionZone -> Vigilar
    - RegresarAZona + PlayerVisible -> Atacar
    - Huyendo + PlayerFar -> Curarse
    - Curarse + PlayerVisible -> Huyendo
    - Curarse + HealthAbove -> EstadoVida (restaurando historial)
"""
GUARDIAN_BEHAVIOR = {
    "name": "guardian",
    "debug": {"show_state_over_entity": True},
    "params": {
        "vision_range": 300.0,
        "vision_fov_deg": 120.0,
        "attack_range": 48.0,
        "flee_threshold": 0.30,
        "restore_threshold": 0.70,
        "heal_rate_per_sec": 0.05,
        "safe_distance": 450.0,
        "player_lost_timeout": 2.0,
        "face_range_multiplier": 2,
        "check_los_throttle": 0.25,
        "protection_margin": 40.0,
        "arrival_threshold": 40.0
    },
    "root": "EstadoVida",
    "states": {
        # Nivel 1: EstadoVida (subMáquina)
        "EstadoVida": {
            "type": "composite",
            "initial": "Vigilar",
            "history": "deep",
            "substates": ["Vigilar", "Atacar", "RegresarAZona"],
            "entry": ["record_last_state_start"],
            "update": ["monitor_player_presence"],
            "exit": [],
            "transitions": [
                # Si la vida baja, huir
                {"to": "Huyendo", "cond": "HealthBelow", "priority": 600}
            ]
        },

        # Nivel 0: EstadoVida.Vigilar (Vigila un camino)
        "EstadoVida.Vigilar": {
            "type": "leaf",
            "entry": ["start_guardian_patrol"],
            "update": ["patrol_tick", "throttle_check_player_visibility"],
            "exit": ["stop_patrol"],
            "transitions": [
                # Si el jugador es visible, atacar
                {"to": "EstadoVida.Atacar", "cond": "PlayerVisible", "priority": 150},
                # Si está lejos de la zona protegida, regresar a la zona
                {"to": "EstadoVida.RegresarAZona", "cond": "IsFarFromProtectionZone", "priority": 300},
            ]
        },

        # Nivel 0: EstadoVida.Atacar (perseguir y golpear al enemigo)
        "EstadoVida.Atacar": {
            "type": "leaf",
            "entry": ["start_pursue_target"],
            "update": ["pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
            "exit": ["stop_pursue"],
            "transitions": [
                # Si el jugador no es visible y está en la zona protegida, volver a vigilar
                {"to": "EstadoVida.Vigilar", "cond": "PlayerNotVisibleAndAtProtectionZone", "priority": 150},
                # Si el jugador no es visible y está lejos de la zona protegida, regresar a la zona
                {"to": "EstadoVida.RegresarAZona", "cond": "PlayerNotVisibleAndFarFromProtectionZone", "priority": 300},
            ]
        },

        # Nivel 0: EstadoVida.RegresarAZona (volver al camino de patrullaje)
        "EstadoVida.RegresarAZona": {
            "type": "leaf",
            "entry": ["return_to_protection_zone"],
            "update": ["check_return_path_finished"],
            "exit": [],
            "transitions": [
                # Si ha llegado a la zona protegida, volver a vigilar
                {"to": "EstadoVida.Vigilar", "cond": "IsAtProtectionZone", "priority": 200},
                # Si el jugador es visible, atacar
                {"to": "EstadoVida.Atacar", "cond": "PlayerVisible", "priority": 350},
            ]
        },

        # Nivel 1: Huyendo (evadir al enemigo)
        "Huyendo": {
            "type": "leaf",
            "entry": ["start_evade_from_player", "set_behavior_flag_fleeing"],
            "update": ["evade_tick"],
            "exit": ["stop_evade", "clear_behavior_flag_fleeing"],
            "transitions": [
                # Si el jugador está lejos, pasar a curarse
                {"to": "Curarse", "cond": "PlayerFar", "priority": 200}
            ]
        },

        # Nivel 1: Curarse (quedarse estático, Face al enemigo, curarse)
        "Curarse": {
            "type": "leaf",
            "entry": ["face_towards_safe_anchor", "stop_movement", "start_heal_tick"],
            "update": ["face_towards_safe_anchor", "heal_tick", "monitor_player_presence"],
            "exit": ["stop_heal_tick", "clear_safe_anchor"],
            "transitions": [
                # Si la entidad se ha recuperado suficiente vida
                {"to": "EstadoVida", "cond": "HealthAbove", "priority": 300, "restore_history": True},
                # Si el jugador aparece mientras se cura
                {"to": "Huyendo", "cond": "PlayerVisible", "priority": 600}
            ]
        },
    }
}

"""
DOCUMENTACIÓN: BOSS_BEHAVIOR

Resumen
    Comportamiento del jefe "boss_reposition_invoker". Diseñado para:
    - Permanecer inicialmente en estado Atento (pre-combate) mirando en una dirección fija.
    - Entrar en combate (EstadoVida) al ver al jugador o tras recibir un golpe sorpresa.
    - Alternar entre ataques cuerpo a cuerpo (AtacarMele) y a distancia (AtacarRange).
    - Reposicionarse a boss_position, invocar aliados y regenerarse manteniendo facing cuando aplica.

Parámetros principales (params)
    - vision_range (px): alcance máximo de detección visual del jugador.
    - vision_fov_deg (deg): apertura del cono de visión.
    - player_seen_memory (s): tiempo de "memoria" tras perder visión.
    - dist_for_mele (px): umbral de distancia para preferir melee frente a ranged.
    - boss_position (x,y): posición donde reposicionarse, invocar y regenerar.
    - allies_for_invocation (int): cantidad total de aliados a crear en Invocar.
    - time_for_invocation (s): duración en la que se distribuyen los spawns.
    - timeout_invocations (s): lifetime de cada aliado invocado (expiración).
    - perc_regenerate (0..1): fracción de vida a recuperar durante Regenerar.
    - time_for_regeneration (s): duración del proceso de regeneración.
    - lost_health_trigger_pct (0..1): fracción de vida perdida que fuerza Reposicionar.
    - check_los_throttle (s): throttling para checks de línea de visión.
    - attention_direction (str): dirección cardinal ("N","S","E","W") usada en Atento.
    - attention_distance (px): distancia para generar el punto de facing en Atento.
    - recent_damage_threshold (float): umbral mínimo de HP perdido para considerar golpe sorpresa.
    - recent_damage_window (s): ventana temporal durante la cual RecentlyDamaged sigue siendo True.
    - arrival_threshold (px): umbral de llegada usado por las transiciones IsAtBossPosition / Reposicionar.

Estados y semántica
  - Atento (leaf, root inicial)
      Estado PRE-COMBATE. Boss estático mirando en la dirección configurada (start_attention_facing).
      Sirve para detección inicial y para ser sorprendido por un golpe (RecentlyDamaged).
      No forma parte del history de EstadoVida para evitar restauraciones a Atento.

  - EstadoVida (composite, history="deep")
      Submáquina de COMBATE. Contiene AtacarMele y AtacarRange.
      Mantiene historial profundo entre subestados de combate para restaurar la modalidad de ataque.

  - AtacarMele (leaf)
      Persecución y ataque cuerpo a cuerpo. Usa start_pursue_target / pursue_tick / try_melee_attack.
      Cambia a ranged si el jugador está lejos o a Reposicionar si pierde demasiada vida.

  - AtacarRange (leaf)
      Modo a distancia: boss queda estático (FACE) y lanza efectos a distancia periódicos
      (start_boss_range_attack_mode / boss_range_attack_tick). Vuelve a melee si el jugador se acerca.

  - Reposicionar (leaf)
      Pathfinding hacia boss_position (start_return_to_boss_position / return_to_boss_tick).
      Al llegar transiciona a Invocar.

  - Invocar (leaf)
      Genera aliados distribuidos en time_for_invocation. Los aliados usan algoritmo PURSUE
      hacia el jugador y tienen lifetime = timeout_invocations. Spawns realizados mediante manager.spawn_enemy.

  - Regenerar (leaf)
      El boss permanece en boss_position, estático y mirando al jugador (start_regeneration / regen_tick).
      Recupera vida progresivamente y, al terminar, vuelve a EstadoVida restaurando el history previo.

Transiciones críticas (resumen práctico)
    - Atento + PlayerVisible -> EstadoVida.AtacarMele o EstadoVida.AtacarRange (según distancia)
    - Atento + RecentlyDamaged -> EstadoVida.AtacarMele o EstadoVida.AtacarRange (sorpresa por daño)
    - EstadoVida.AtacarMele -> EstadoVida.AtacarRange cuando PlayerBeyondMelee
    - EstadoVida.AtacarRange -> EstadoVida.AtacarMele cuando PlayerWithinMelee
    - EstadoVida.* -> Reposicionar si LostHealthSinceLastRestoreAtLeast (perdida significativa)
    - Reposicionar -> Invocar cuando IsAtBossPosition
    - Invocar -> Regenerar cuando InvocationFinished
    - Regenerar -> EstadoVida (restore_history=True) cuando RegenerationFinished
"""
BOSS_BEHAVIOR = {
    "name": "boss_reposition_invoker",
    "debug": {"show_state_over_entity": True},
    "params": {
        "vision_range": 500.0,
        "vision_fov_deg": 120.0,
        "player_seen_memory": 0.5,
        "dist_for_mele": 200.0,
        "boss_position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*55, CONF.MAIN_WIN.RENDER_TILE_SIZE*47),
        "allies_for_invocation": 4,
        "time_for_invocation": 6.0,
        "timeout_invocations": 14.0,
        "perc_regenerate": 0.18,
        "time_for_regeneration": 8.0,
        "lost_health_trigger_pct": 0.25,
        "check_los_throttle": 0.12,
        "attention_direction": "W",
        "attention_distance": 10.0,
        "recent_damage_threshold": 1.0,
        "recent_damage_window": 1.0,
        "arrival_threshold": 24.0
    },
    "root": "Atento",
    "states": {
        # Nivel 1: Atento - boss quieto mirando en dirección configurada (puede ser sorprendido)
        "Atento": {
            "type": "leaf",
            "entry": ["start_attention_facing"],
            "update": ["record_health_tick", "throttle_check_player_visibility", "monitor_player_presence"],
            "exit": [],
            "transitions": [
                # si el jugador es visible -> EstadoVida
                {"to": "EstadoVida", "cond": "PlayerVisible", "priority": 250},
                # si el boss fue dañado recientemente -> EstadoVida
                {"to": "EstadoVida", "cond": "RecentlyDamaged", "priority": 400},
            ]
        },

        # Nivel 1: EstadoVida - composite que alterna entre melee y ranged
        "EstadoVida": {
            "type": "composite",
            "initial": "AtacarRange",
            "history": "deep",
            "substates": ["AtacarMele", "AtacarRange"],
            "entry": ["record_last_state_start"],
            "update": ["monitor_player_presence"],
            "exit": [],
            "transitions": [
                # si acumula pérdida de vida >= lost_health_trigger_pct -> Reposicionar
                {"to": "Reposicionar", "cond": "LostHealthSinceLastRestoreAtLeast", "priority": 300}
            ]
        },

        # Nivel 0: EstadoVida.AtacarMele - perseguir y golpear cuerpo a cuerpo
        "EstadoVida.AtacarMele": {
            "type": "leaf",
            "entry": ["start_pursue_target"],
            "update": ["record_health_tick", "pursue_tick", "try_melee_attack", "throttle_check_player_visibility"],
            "exit": ["stop_pursue"],
            "transitions": [
                # si el player está visible y más lejos que dist_for_mele -> cambiar a ranged
                {"to": "EstadoVida.AtacarRange", "cond": "PlayerBeyondMelee", "priority": 150},
            ]
        },

        # Nivel 0: EstadoVida.AtacarRange - ataques a distancia (lanza figura / AOE proyectil)
        "EstadoVida.AtacarRange": {
            "type": "leaf",
            "entry": ["start_boss_range_attack_mode"],
            "update": ["record_health_tick", "boss_range_attack_tick", "throttle_check_player_visibility"],
            "exit": ["stop_boss_range_attack_mode"],
            "transitions": [
                # si el player está visible y dentro de melee -> volver a melee
                {"to": "EstadoVida.AtacarMele", "cond": "PlayerWithinMelee", "priority": 150},
            ]
        },

        # Nivel 1: Reposicionar - pathfinding hacia boss_position + pathfollowing
        "Reposicionar": {
            "type": "leaf",
            "entry": ["start_return_to_boss_position"],
            "update": ["return_to_boss_tick", "throttle_check_player_visibility", "record_health_tick"],
            "exit": ["stop_return_to_boss_position"],
            "transitions": [
                # Cuando alcanza boss_position -> Invocar
                {"to": "Invocar", "cond": "IsAtBossPosition", "priority": 200},
            ]
        },

        # Nivel 1: Invocar - generar aliados que persiguen al player
        "Invocar": {
            "type": "leaf",
            "entry": ["start_invocation"],
            "update": ["invocation_tick"],
            "exit": ["stop_invocation"],
            "transitions": [
                # Cuando concluye el proceso de invocación -> Regenerar
                {"to": "Regenerar", "cond": "InvocationFinished", "priority": 250}
            ]
        },

        # Nivel 1: Regenerar - aplica regeneración de perc_regenerate en time_for_regeneration
        "Regenerar": {
            "type": "leaf",
            "entry": ["start_regeneration"],
            "update": ["regen_tick", "face_towards_safe_anchor", "monitor_player_presence"],
            "exit": ["stop_regeneration", "reset_lost_health_accum"],
            "transitions": [
                # Al completar la regeneración, volver al EstadoVida (restaurando historia)
                {"to": "EstadoVida", "cond": "RegenerationFinished", "priority": 300, "restore_history": True}
            ]
        },
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
        "slow_radius_dist": 140.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.25,
        "behavior": HUNTER_BEHAVIOR,
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 28, CONF.MAIN_WIN.RENDER_TILE_SIZE * 49),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 120.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 140.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.25,
        "path": path_zone_1,
        "path_offset": paths_1_group["zone 1"]["offset"],
        "behavior": GUARDIAN_BEHAVIOR,
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 10, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 120.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 140.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.25,
        "path": path_zone_2,
        "path_offset": paths_1_group["zone 2"]["offset"],
    },
    {
        "type": "gargant-boss",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*55, CONF.MAIN_WIN.RENDER_TILE_SIZE*47),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": None,
        "max_speed": 100.0,
        "target_radius_dist": 40.0,
        "slow_radius_dist": 140.0,
        "target_radius_deg": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius_deg": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.25,
        "behavior": BOSS_BEHAVIOR,
    },
]

map_2_group = map_1_group

map_levels_enemies_data = {
    1 : map_1_group,
    2 : map_2_group,
}
