from configs.package import CONF

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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*29, CONF.MAIN_WIN.RENDER_TILE_SIZE*29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FLEE_KINEMATIC,
        "max_speed": 140.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*20, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ARRIVE_KINEMATIC,
        "max_speed": 200.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*31),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.FLEE_DYNAMIC,
        "max_speed": 140.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*28, CONF.MAIN_WIN.RENDER_TILE_SIZE*22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC,
        "max_speed": 200.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*26, CONF.MAIN_WIN.RENDER_TILE_SIZE*26),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.ALIGN,
        "max_speed": 180.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
# - target_radius: radio de llegada (float)
# - slow_radius: radio de desaceleración (float)
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
        "target_radius": 40.0,
        "slow_radius": 180.0,
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
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*31, CONF.MAIN_WIN.RENDER_TILE_SIZE*31),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.EVADE,
        "max_speed": 180.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.1,
    },
]

# Para Face
# Atributos relevantes:
# - target_radius: umbral de orientación (float)
# - slow_radius: radio de desaceleración (float)
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 1.0,
    },
]

# Para Look Where You're Going (junto a Evade)
# Atributos relevantes:
# - target_radius: umbral de orientación (float)
# - slow_radius: radio de desaceleración (float)
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.1,
        "max_acceleration": 300.0,
        "max_rotation": 2.0,
        "max_angular_accel": 30.0,
        "max_prediction": 0.1,
    },
]

# Para Dynamic Wander
# Atributos relevantes:
# - target_radius: umbral de orientación (float)
# - slow_radius: radio de desaceleración (float)
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
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

enemy_follow_path_circle = [
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 31),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["circle"]["type"],
        "path_params": PATH_CONFIGS["circle"]["params"],
        "path_offset": PATH_CONFIGS["circle"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 29, CONF.MAIN_WIN.RENDER_TILE_SIZE * 29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["circle"]["type"],
        "path_params": PATH_CONFIGS["circle"]["params"],
        "path_offset": PATH_CONFIGS["circle"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 31, CONF.MAIN_WIN.RENDER_TILE_SIZE * 29),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["circle"]["type"],
        "path_params": PATH_CONFIGS["circle"]["params"],
        "path_offset": PATH_CONFIGS["circle"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 40, CONF.MAIN_WIN.RENDER_TILE_SIZE * 40),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["circle"]["type"],
        "path_params": PATH_CONFIGS["circle"]["params"],
        "path_offset": PATH_CONFIGS["circle"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 16, CONF.MAIN_WIN.RENDER_TILE_SIZE * 28),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["circle"]["type"],
        "path_params": PATH_CONFIGS["circle"]["params"],
        "path_offset": PATH_CONFIGS["circle"]["offset"],
    },
]

enemy_follow_path_rect = [
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 25),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["rectangle"]["type"],
        "path_params": PATH_CONFIGS["rectangle"]["params"],
        "path_offset": PATH_CONFIGS["rectangle"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 35, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["rectangle"]["type"],
        "path_params": PATH_CONFIGS["rectangle"]["params"],
        "path_offset": PATH_CONFIGS["rectangle"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 35),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["rectangle"]["type"],
        "path_params": PATH_CONFIGS["rectangle"]["params"],
        "path_offset": PATH_CONFIGS["rectangle"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 25, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["rectangle"]["type"],
        "path_params": PATH_CONFIGS["rectangle"]["params"],
        "path_offset": PATH_CONFIGS["rectangle"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 16, CONF.MAIN_WIN.RENDER_TILE_SIZE * 38),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["rectangle"]["type"],
        "path_params": PATH_CONFIGS["rectangle"]["params"],
        "path_offset": PATH_CONFIGS["rectangle"]["offset"],
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 44, CONF.MAIN_WIN.RENDER_TILE_SIZE * 22),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": PATH_CONFIGS["rectangle"]["type"],
        "path_params": PATH_CONFIGS["rectangle"]["params"],
        "path_offset": PATH_CONFIGS["rectangle"]["offset"],
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
        "type": "circle",
        "params": {
            "radius": 240, 
            "segments": 35, 
            "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 14 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2, 
                       CONF.MAIN_WIN.RENDER_TILE_SIZE * 49 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2)},
        "offset": 2,
    },
    "zone 2" : {
        "type": "rectangle",
        "params": {
            "width": 540.0, 
            "height": 320.0, 
            "segments": 30, 
            "center": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 9 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                       CONF.MAIN_WIN.RENDER_TILE_SIZE * 6 + CONF.MAIN_WIN.RENDER_TILE_SIZE)},
        "offset": 3,
    }
}

map_1_group = [
    {
        "type": "gargant-soldier",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE*3, CONF.MAIN_WIN.RENDER_TILE_SIZE*16),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PURSUE,
        "max_speed": 200.0,
        "target_radius": 40.0,
        "slow_radius": 180.0,
        "time_to_target": 0.15,
        "max_acceleration": 300.0,
        "max_rotation": 1.0,
        "max_angular_accel": 1.0,
        "max_prediction": 0.5,
    },
    {
        "type": "gargant-lord",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 28, CONF.MAIN_WIN.RENDER_TILE_SIZE * 49),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 100.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": paths_1_group["zone 1"]["type"],
        "path_params": paths_1_group["zone 1"]["params"],
        "path_offset": paths_1_group["zone 1"]["offset"],
    },
    {
        "type": "gargant-berserker",
        "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 10, CONF.MAIN_WIN.RENDER_TILE_SIZE * 7),
        "collider_box": (CONF.ENEMY.COLLIDER_BOX_WIDTH, CONF.ENEMY.COLLIDER_BOX_HEIGHT),
        "algorithm": CONF.ALG.ALGORITHM.PATH_FOLLOWING,
        "max_speed": 120.0,
        "target_radius": 5 * CONF.CONST.CONVERT_TO_RAD,
        "slow_radius": 60 * CONF.CONST.CONVERT_TO_RAD,
        "time_to_target": 0.15,
        "max_acceleration": 200.0,
        "max_rotation": 2.0,
        "max_angular_accel": 4.0,
        "max_prediction": 0.5,
        "path_type": paths_1_group["zone 2"]["type"],
        "path_params": paths_1_group["zone 2"]["params"],
        "path_offset": paths_1_group["zone 2"]["offset"],
    },
]

map_2_group = map_1_group

map_levels_enemies_data = {
    1 : map_1_group,
    2 : map_2_group,
}