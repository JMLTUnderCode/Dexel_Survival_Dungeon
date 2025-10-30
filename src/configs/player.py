import enum

FOLDER = "player"
TILE_WIDTH = 64
TILE_HEIGHT = 64
COLLIDER_BOX_WIDTH = 48
COLLIDER_BOX_HEIGHT = 48
class ACTIONS(str, enum.Enum):
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"
