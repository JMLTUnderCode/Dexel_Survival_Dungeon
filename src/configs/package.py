from dataclasses import dataclass, field
from . import main_window as MAIN_WIN
from . import development as DEV
from . import constants as CONST
from . import player as PLAYER
from . import enemy as ENEMY
from . import map as MAP
from . import algorithms as ALG
from . import algorithms_ui as ALG_UI
from . import map_ui as MAP_UI

@dataclass
class MainWindowConfig:
    GAME_TITLE: str = MAIN_WIN.GAME_TITLE
    FPS: int = MAIN_WIN.FPS
    TILE_SIZE: int = MAIN_WIN.TILE_SIZE
    ZOOM: int = MAIN_WIN.ZOOM
    RENDER_TILE_SIZE: int = MAIN_WIN.RENDER_TILE_SIZE
    SCREEN_OFF_SET: int = MAIN_WIN.SCREEN_OFF_SET

@dataclass
class DevelopmentConfig:
    DEBUG: bool = DEV.DEBUG
    COLLISION_RECTS: bool = DEV.COLLISION_RECTS
    ACTIVE_ALG: bool = DEV.ACTIVE_ALG
    PATHFOLLOWER: bool = DEV.PATHFOLLOWER
    NAV_MESH: bool = DEV.NAV_MESH
    NODE_LOCATION: bool = DEV.NODE_LOCATION
    PATHFINDER: bool = DEV.PATHFINDER
    TEMP_PATHFOLLOWER: bool = DEV.TEMP_PATHFOLLOWER
    HSM: bool = DEV.HSM
    ACTIVE_BEHAVIOR: bool = DEV.ACTIVE_BEHAVIOR
    MAX_HSM_HISTORY_SIZE: int = DEV.MAX_HSM_HISTORY_SIZE

@dataclass
class ConstantsConfig:
    PI: float = CONST.PI
    CONVERT_TO_RAD: float = CONST.CONVERT_TO_RAD
    CONVERT_TO_DEG: float = CONST.CONVERT_TO_DEG

@dataclass
class PlayerConfig:
    FOLDER: str = PLAYER.FOLDER
    TILE_WIDTH: int = PLAYER.TILE_WIDTH
    TILE_HEIGHT: int = PLAYER.TILE_HEIGHT
    COLLIDER_BOX_WIDTH: int = PLAYER.COLLIDER_BOX_WIDTH
    COLLIDER_BOX_HEIGHT: int = PLAYER.COLLIDER_BOX_HEIGHT
    ACTIONS: PLAYER.ACTIONS = PLAYER.ACTIONS

@dataclass
class EnemyConfig:
    FOLDER: str = ENEMY.FOLDER
    TILE_WIDTH: int = ENEMY.TILE_WIDTH
    TILE_HEIGHT: int = ENEMY.TILE_HEIGHT
    COLLIDER_BOX_WIDTH: int = ENEMY.COLLIDER_BOX_WIDTH
    COLLIDER_BOX_HEIGHT: int = ENEMY.COLLIDER_BOX_HEIGHT
    ACTIONS: ENEMY.ACTIONS = ENEMY.ACTIONS

@dataclass
class MapConfig:
    LEVELS: dict = field(default_factory=lambda: dict(MAP.LEVELS))

@dataclass
class AlgorithmConfig:
    ALGORITHM: ALG.ALGORITHM = ALG.ALGORITHM

@dataclass
class AlgorithmUIConfig:
    ACTIVE: bool = ALG_UI.ACTIVE
    PANEL_WIDTH: int = ALG_UI.PANEL_WIDTH
    PADDING: int = ALG_UI.PADDING
    BUTTON_HEIGHT: int = ALG_UI.BUTTON_HEIGHT
    BG_COLOR: tuple[int, int, int, int] = ALG_UI.BG_COLOR
    BUTTON_COLOR: tuple[int, int, int] = ALG_UI.BUTTON_COLOR
    BUTTON_HOVER: tuple[int, int, int] = ALG_UI.BUTTON_HOVER
    BUTTON_ACTIVE: tuple[int, int, int] = ALG_UI.BUTTON_ACTIVE
    TEXT_COLOR: tuple[int, int, int] = ALG_UI.TEXT_COLOR
    TITLE: str = ALG_UI.TITLE
    TITLE_COLOR: tuple[int, int, int] = ALG_UI.TITLE_COLOR
    TITLE_FONT = ALG_UI.TITLE_FONT
    FONT = ALG_UI.FONT
    BUTTONS: list = field(default_factory=lambda: list(ALG_UI.BUTTONS))
    PARSING_BUTTONS: dict = field(default_factory=lambda: dict(ALG_UI.PARSING_BUTTONS))
    SELECTED = ALG_UI.SELECTED

@dataclass
class MapUIConfig:
    ACTIVE: bool = MAP_UI.ACTIVE
    PANEL_WIDTH: int = MAP_UI.PANEL_WIDTH
    PADDING: int = MAP_UI.PADDING
    BUTTON_HEIGHT: int = MAP_UI.BUTTON_HEIGHT
    BG_COLOR: tuple[int, int, int, int] = MAP_UI.BG_COLOR
    BUTTON_COLOR: tuple[int, int, int] = MAP_UI.BUTTON_COLOR
    BUTTON_HOVER: tuple[int, int, int] = MAP_UI.BUTTON_HOVER
    BUTTON_ACTIVE: tuple[int, int, int] = MAP_UI.BUTTON_ACTIVE
    TEXT_COLOR: tuple[int, int, int] = MAP_UI.TEXT_COLOR
    TITLE: str = MAP_UI.TITLE
    TITLE_COLOR: tuple[int, int, int] = MAP_UI.TITLE_COLOR
    TITLE_FONT = MAP_UI.TITLE_FONT
    FONT = MAP_UI.FONT
    BUTTONS: list = field(default_factory=lambda: list(MAP_UI.BUTTONS))
    PARSING_BUTTONS: dict = field(default_factory=lambda: dict(MAP_UI.PARSING_BUTTONS))
    SELECTED = MAP_UI.SELECTED

class Config:
    MAIN_WIN: MainWindowConfig
    DEV: DevelopmentConfig
    CONST: ConstantsConfig
    PLAYER: PlayerConfig
    ENEMY: EnemyConfig
    MAP: MapConfig
    ALG: AlgorithmConfig
    ALG_UI: AlgorithmUIConfig
    MAP_UI: MapUIConfig

    def __init__(self):
        self.MAIN_WIN = MainWindowConfig()
        self.DEV = DevelopmentConfig()
        self.CONST = ConstantsConfig()
        self.PLAYER = PlayerConfig()
        self.ENEMY = EnemyConfig()
        self.MAP = MapConfig()
        self.ALG = AlgorithmConfig()
        self.ALG_UI = AlgorithmUIConfig()
        self.MAP_UI = MapUIConfig()

CONF = Config()