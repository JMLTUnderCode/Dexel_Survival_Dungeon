import enum

FOLDER_ANIM = "player"
TILE_WIDTH = 64
TILE_HEIGHT = 64
COLLIDER_BOX_WIDTH = 48
COLLIDER_BOX_HEIGHT = 48
class ACTIONS(str, enum.Enum):
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"
FOLDER_EFFECTS = "attacks"
EFFECTS = {
    "mele": {
        "file": "mele.png",
        "frames": 11,
        "w": TILE_WIDTH,
        "h": TILE_HEIGHT,
    },
    "magic": {
        "file": "magic.png",
        "frames": 11,
        "w": TILE_WIDTH,
        "h": TILE_HEIGHT,
    }
}
PIVOT_MOVE_SPEED = 700.0
PIVOT_RETURN_SPEED = 700.0
PIVOT_EPS = 1e-3