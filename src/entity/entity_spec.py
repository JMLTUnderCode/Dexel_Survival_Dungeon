from algorithms.algorithms_configs import AlgorithmConfigType
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class SpawnedEntityMeta:
    lifetime: float
    spawned_at: float

@dataclass
class Stats:
    alive: bool = True
    health: float = 100.0
    mana: Optional[float] = 100.0
    armor: Optional[float] = 100.0
    mele_dmg: Optional[float] = 20.0
    mele_cooldown: Optional[float] = 3.0
    range_dmg: Optional[float] = 25.0
    range_cooldown: Optional[float] = 3.5

@dataclass
class Sprite:
    name: str
    frame_duration: Optional[float] = 0.12
    scale: Optional[float] = 1.25

@dataclass
class EntitySpec:
    id: int
    sprite: Sprite
    initial_position: tuple[float, float]
    collider_box: tuple[float, float]
    initial_algorithm: str
    alg_configs: Dict[str, AlgorithmConfigType]
    statistics: Stats = None
    behavior: Optional[str] = None
    spawn_meta: Optional[SpawnedEntityMeta] = None