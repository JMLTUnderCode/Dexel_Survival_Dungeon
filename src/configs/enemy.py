import enum

FOLDER_ANIM = "enemies"
TILE_WIDTH = 64
TILE_HEIGHT = 64
COLLIDER_BOX_WIDTH = 48
COLLIDER_BOX_HEIGHT = 48
class ACTIONS(str, enum.Enum):
    IDLE = "idle"
    MOVE = "move"
    MOVE_WOUNDED = "move-wounded"
    ATTACK = "attack"
    ATTACK_WOUNDED = "attack-wounded"
    DEATH_0 = "death-0"
    DEATH_1 = "death-1"
FOLDER_EFFECTS = "effects"
EFFECTS = {
    "mele": {
        "file": "mele-strike-2.png",
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
    "invocation": {
        "file": "invocation.png",
        "frames": 8,
        "w": 72,
        "h": 72,
    }
}