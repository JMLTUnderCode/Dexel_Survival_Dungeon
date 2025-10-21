import enum

FOLDER = "enemies"
TILE_WIDTH = 64
TILE_HEIGHT = 64
COLLIDER_BOX_WIDTH = 48
COLLIDER_BOX_HEIGHT = 48
class ACTIONS(str, enum.Enum):
    MOVE = "move"
    MOVE_WOUNDED = "move-wounded"
    ATTACK = "attack"
    ATTACK_WOUNDED = "attack-wounded"
    DEATH_0 = "death-0"
    DEATH_1 = "death-1"