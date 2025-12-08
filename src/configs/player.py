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
FOLDER_EFFECTS = "effects"
EFFECTS = {
    "mele": {
        "file": "mele-strike-1.png",
        "frames": 11,
        "w": 64,
        "h": 64,
    },
    "magic": {
        "file": "water-explosion.png",
        "frames": 5,
        "w": 128,
        "h": 128,
    },
    "healing": {
        "file": "gas-healing.png",
        "frames": 10,
        "w": 128,
        "h": 128,
    },
}
PIVOT_MOVE_SPEED = 700.0
PIVOT_RETURN_SPEED = 700.0
PIVOT_EPS = 1e-3