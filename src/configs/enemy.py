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
FOLDER_EFFECTS = "attacks"
EFFECTS = {
    "mele": {
        "file": "mele-2.png",
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