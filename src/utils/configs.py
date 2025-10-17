import math
import os
import enum

# Cargar variable DEVELOPMENT desde .env si existe
DEVELOPMENT = True
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip().startswith("DEVELOPMENT="):
                _, value = line.strip().split("=", 1)
                DEVELOPMENT = value.strip().lower() == "true" or value.strip() == "1" or value.strip().lower() == "yes" or value.strip().lower() == "on"
                break

# Lista de algoritmos disponibles
class ALGORITHM(str, enum.Enum):
    SEEK_KINEMATIC = "SEEK KINEMATIC"
    FLEE_KINEMATIC = "FLEE KINEMATIC"
    ARRIVE_KINEMATIC = "ARRIVE KINEMATIC"
    WANDER_KINEMATIC = "WANDER KINEMATIC"
    SEEK_DYNAMIC = "SEEK DYNAMIC"
    FLEE_DYNAMIC = "FLEE DYNAMIC"
    ARRIVE_DYNAMIC = "ARRIVE DYNAMIC"
    WANDER_DYNAMIC = "WANDER DYNAMIC"
    ALIGN = "ALIGN"
    VELOCITY_MATCH = "VELOCITY MATCH"
    PURSUE = "PURSUE"
    EVADE = "EVADE"
    FACE = "FACE"
    LOOK_WHERE_YOURE_GOING = "LOOK WHERE YOU'RE GOING"
    PATH_FOLLOWING = "PATH FOLLOWING"

# Configuraciones generales del juego
GAME_TITLE = "Dexel Survival Dungeon"
FPS = 60
TILE_SIZE = 16
ZOOM = 2.5
RENDER_TILE_SIZE = TILE_SIZE * ZOOM
SCREEN_OFF_SET = 60
PI = math.pi
CONVERT_TO_RAD = PI / 180
CONVERT_TO_DEG = 180 / PI

# Configuraciones del jugador
PLAYER_FOLDER = "player"
PLAYER_TILE_WIDTH = 64
PLAYER_TILE_HEIGHT = 64
PLAYER_COLLIDER_BOX_WIDTH = 48
PLAYER_COLLIDER_BOX_HEIGHT = 48
class PLAYER_STATES(str, enum.Enum):
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"

# Configuraciones del enemigo
ENEMY_FOLDER = "enemies"
ENEMY_TILE_WIDTH = 64
ENEMY_TILE_HEIGHT = 64
ENEMY_COLLIDER_BOX_WIDTH = 48
ENEMY_COLLIDER_BOX_HEIGHT = 48
class ENEMY_STATES(str, enum.Enum):
    MOVE = "move"
    MOVE_WOUNDED = "move-wounded"
    ATTACK = "attack"
    ATTACK_WOUNDED = "attack-wounded"
    DEATH_0 = "death-0"
    DEATH_1 = "death-1"

# Configuraciones de UI para conjuntos de enemigos con algoritmos

# --- UI: panel de selección de listas de enemigos ---
UI_PANEL_WIDTH = 200
UI_PADDING = 12
UI_BUTTON_HEIGHT = 36
UI_BG_COLOR = (20, 20, 20, 220)
UI_BUTTON_COLOR = (50, 50, 50)
UI_BUTTON_HOVER = (70, 70, 70)
UI_BUTTON_ACTIVE = (90, 160, 90)
UI_TEXT_COLOR = (230, 230, 230)
UI_TITLE_COLOR = (180, 220, 255)
UI_TITLE_FONT = None
UI_FONT = None

parsing_button = {
    "ALGORITHM.SEEK_KINEMATIC": "SEEK KINEMATIC",
    "ALGORITHM.FLEE_KINEMATIC": "FLEE KINEMATIC",
    "ALGORITHM.ARRIVE_KINEMATIC": "ARRIVE KINEMATIC",
    "ALGORITHM.WANDER_KINEMATIC": "WANDER KINEMATIC",
    "ALGORITHM.SEEK_DYNAMIC": "SEEK DYNAMIC",
    "ALGORITHM.FLEE_DYNAMIC": "FLEE DYNAMIC",
    "ALGORITHM.ARRIVE_DYNAMIC": "ARRIVE DYNAMIC",
    "ALGORITHM.WANDER_DYNAMIC": "WANDER DYNAMIC",
    "ALGORITHM.ALIGN": "ALIGN",
    "ALGORITHM.VELOCITY_MATCH": "VELOCITY MATCH",
    "ALGORITHM.PURSUE": "PURSUE",
    "ALGORITHM.EVADE": "EVADE",
    "ALGORITHM.FACE": "FACE",
    "ALGORITHM.LOOK_WHERE_YOURE_GOING": "LOOK W. Y. GOING",
    "ALGORITHM.PATH_FOLLOWING": "PATH FOLLOWING",
    "ALL": "ALL",
    "EMPTY": "EMPTY"
}
UI_BUTTONS = []  # list of dicts {key, rect}