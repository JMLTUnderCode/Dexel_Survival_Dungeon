from dataclasses import dataclass, field
from . import main_window as MAIN_WIN
from . import development as DEV
from . import constants as CONST
from . import player as PLAYER
from . import enemy as ENEMY
from . import algorithms as ALG
from . import algorithms_ui as ALG_UI

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
class AlgorithmConfig:
    ALGORITHM: ALG.ALGORITHM = ALG.ALGORITHM

@dataclass
class AlgorithmUIConfig:
    PANEL_WIDTH: int = ALG_UI.PANEL_WIDTH
    PADDING: int = ALG_UI.PADDING
    BUTTON_HEIGHT: int = ALG_UI.BUTTON_HEIGHT
    BG_COLOR: tuple[int, int, int, int] = ALG_UI.BG_COLOR
    BUTTON_COLOR: tuple[int, int, int] = ALG_UI.BUTTON_COLOR
    BUTTON_HOVER: tuple[int, int, int] = ALG_UI.BUTTON_HOVER
    BUTTON_ACTIVE: tuple[int, int, int] = ALG_UI.BUTTON_ACTIVE
    TEXT_COLOR: tuple[int, int, int] = ALG_UI.TEXT_COLOR
    TITLE_COLOR: tuple[int, int, int] = ALG_UI.TITLE_COLOR
    TITLE_FONT = ALG_UI.TITLE_FONT
    FONT = ALG_UI.FONT
    BUTTONS: list = field(default_factory=lambda: list(ALG_UI.BUTTONS))
    PARSING_BUTTONS: dict = field(default_factory=lambda: dict(ALG_UI.PARSING_BUTTONS))
    SELECTED_ALGORITHM = ALG_UI.SELECTED_ALGORITHM

class Config:
    MAIN_WIN: MainWindowConfig
    DEV: DevelopmentConfig
    CONST: ConstantsConfig
    PLAYER: PlayerConfig
    ENEMY: EnemyConfig
    ALG: AlgorithmConfig
    ALG_UI: AlgorithmUIConfig

    def __init__(self):
        self.MAIN_WIN = MainWindowConfig()
        self.DEV = DevelopmentConfig()
        self.CONST = ConstantsConfig()
        self.PLAYER = PlayerConfig()
        self.ENEMY = EnemyConfig()
        self.ALG = AlgorithmConfig()
        self.ALG_UI = AlgorithmUIConfig()

CONF = Config()