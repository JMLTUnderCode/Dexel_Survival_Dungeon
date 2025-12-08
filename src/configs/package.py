from dataclasses import dataclass, field
from . import ui as UI
from . import main_window as MAIN_WIN
from . import development as DEV
from . import constants as CONST
from . import player as PLAYER
from . import enemy as ENEMY
from . import map as MAP
from . import algorithms as ALG
from . import algorithms_ui as ALG_UI
from . import map_ui as MAP_UI
from . import tactical as TACTICAL
from . import audio as AUDIO

@dataclass
class UIConfig:
    VERSION: str = UI.VERSION
    BACKGROUND_COLOR: tuple[int, int, int] = UI.BACKGROUND_COLOR
    FOLDER_UI: str = UI.FOLDER_UI
    BUTTONS: dict = field(default_factory=lambda: dict(UI.BUTTONS))
    ICONS: dict = field(default_factory=lambda: dict(UI.ICONS))

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
    HSM_HISTORY: bool = DEV.HSM_HISTORY
    MAX_HSM_HISTORY_SIZE: int = DEV.MAX_HSM_HISTORY_SIZE
    PIVOTS: bool = DEV.PIVOTS
    TACTICAL_TYPES: bool = DEV.TACTICAL_TYPES

@dataclass
class ConstantsConfig:
    PI: float = CONST.PI
    CONVERT_TO_RAD: float = CONST.CONVERT_TO_RAD
    CONVERT_TO_DEG: float = CONST.CONVERT_TO_DEG

@dataclass
class PlayerConfig:
    FOLDER_ANIM: str = PLAYER.FOLDER_ANIM
    TILE_WIDTH: int = PLAYER.TILE_WIDTH
    TILE_HEIGHT: int = PLAYER.TILE_HEIGHT
    COLLIDER_BOX_WIDTH: int = PLAYER.COLLIDER_BOX_WIDTH
    COLLIDER_BOX_HEIGHT: int = PLAYER.COLLIDER_BOX_HEIGHT
    ACTIONS: PLAYER.ACTIONS = PLAYER.ACTIONS
    FOLDER_EFFECTS: str = PLAYER.FOLDER_EFFECTS
    EFFECTS: dict = field(default_factory=lambda: dict(PLAYER.EFFECTS))
    PIVOT_MOVE_SPEED: float = PLAYER.PIVOT_MOVE_SPEED
    PIVOT_RETURN_SPEED: float = PLAYER.PIVOT_RETURN_SPEED
    PIVOT_EPS: float = PLAYER.PIVOT_EPS

@dataclass
class EnemyConfig:
    FOLDER_ANIM: str = ENEMY.FOLDER_ANIM
    TILE_WIDTH: int = ENEMY.TILE_WIDTH
    TILE_HEIGHT: int = ENEMY.TILE_HEIGHT
    COLLIDER_BOX_WIDTH: int = ENEMY.COLLIDER_BOX_WIDTH
    COLLIDER_BOX_HEIGHT: int = ENEMY.COLLIDER_BOX_HEIGHT
    ACTIONS: ENEMY.ACTIONS = ENEMY.ACTIONS
    FOLDER_EFFECTS: str = ENEMY.FOLDER_EFFECTS
    EFFECTS: dict = field(default_factory=lambda: dict(ENEMY.EFFECTS))
    
@dataclass
class MapConfig:
    LEVELS: dict = field(default_factory=lambda: dict(MAP.LEVELS))

@dataclass
class AlgorithmConfigType:
    ALGORITHM: ALG.ALGORITHM = ALG.ALGORITHM
    EPS: float = ALG.EPS

@dataclass
class TacticalTypes:
    TYPES: TACTICAL.TYPES = TACTICAL.TYPES

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

@dataclass
class AudioConfig:
    FOLDER_AUDIO: str = AUDIO.FOLDER_AUDIO
    MUSIC: dict = field(default_factory=lambda: dict(AUDIO.MUSIC))
    SFX: dict = field(default_factory=lambda: dict(AUDIO.SFX))
    DEFAULT_MUSIC_VOLUME: float = AUDIO.DEFAULT_MUSIC_VOLUME
    DEFAULT_SFX_VOLUME: float = AUDIO.DEFAULT_SFX_VOLUME

class Config:
    UI: UIConfig
    MAIN_WIN: MainWindowConfig
    DEV: DevelopmentConfig
    CONST: ConstantsConfig
    PLAYER: PlayerConfig
    ENEMY: EnemyConfig
    MAP: MapConfig
    ALG: AlgorithmConfigType
    ALG_UI: AlgorithmUIConfig
    MAP_UI: MapUIConfig
    TACTICAL: TacticalTypes
    AUDIO: AudioConfig

    def __init__(self):
        self.UI = UIConfig()
        self.MAIN_WIN = MainWindowConfig()
        self.DEV = DevelopmentConfig()
        self.CONST = ConstantsConfig()
        self.PLAYER = PlayerConfig()
        self.ENEMY = EnemyConfig()
        self.MAP = MapConfig()
        self.ALG = AlgorithmConfigType()
        self.ALG_UI = AlgorithmUIConfig()
        self.MAP_UI = MapUIConfig()
        self.TACTICAL = TacticalTypes()
        self.AUDIO = AudioConfig()

CONF = Config()