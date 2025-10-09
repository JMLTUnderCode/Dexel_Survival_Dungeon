import enum
import os

# Cargar variable DEVELOPMENT desde .env si existe
DEVELOPMENT = None
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip().startswith("DEVELOPMENT="):
                _, value = line.strip().split("=", 1)
                DEVELOPMENT = value.strip().lower() == "true" or value.strip() == "1" or value.strip().lower() == "yes" or value.strip().lower() == "on"
                break

# Cargar variable ALGORITHM desde .env si existe
ALGORITHM = "ARRIVE"  # Por defecto, usar ARRIVE
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip().startswith("ALGORITHM="):
                _, value = line.strip().split("=", 1)
                ALGORITHM = value.strip()
                break

# Configuraciones generales del juego
GAME_TITLE = "Dexel Survival Dungeon"
FPS = 60
TILE_SIZE = 16
ZOOM = 2.5
RENDER_TILE_SIZE = TILE_SIZE * ZOOM
CAMERA_WIDTH = 1200
CAMERA_HEIGHT = 800

# Configuraciones del jugador
PLAYER="player" # carpeta base de assets del jugador
PLAYER_TILE_WIDTH = 64
PLAYER_TILE_HEIGHT = 64
PLAYER_COLLIDER_BOX = 48
class PLAYER_STATES(str, enum.Enum):
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"

# Configuraciones del enemigo
ENEMY="enemies" # carpeta base de assets de enemigos
ENEMY_TILE_WIDTH = 64
ENEMY_TILE_HEIGHT = 64
ENEMY_COLLIDER_BOX = 48
class ENEMY_STATES(str, enum.Enum):
    MOVE = "move"
    MOVE_WOUNDED = "move-wounded"
    ATTACK = "attack"
    ATTACK_WOUNDED = "attack-wounded"
    DEATH_0 = "death-0"
    DEATH_1 = "death-1"
