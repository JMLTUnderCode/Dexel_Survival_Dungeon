"""
Descripción
    MÓDULO: Definiciones tipadas para especificaciones de entidad (EntitySpec).
    Contiene dataclasses que representan la información mínima necesaria para
    construir enemigos y controlar su ciclo de vida (stats, sprite, spawn_meta, configs).
"""

# 1. Imports
from dataclasses import dataclass
from typing import Optional, Dict, Tuple
from algorithms.algorithms_configs import AlgorithmConfigType

__all__ = ["SpawnedEntityMeta", "Stats", "Sprite", "EntitySpec"]

@dataclass
class SpawnedEntityMeta:
    """
    Descripción
        CLASE: Metadatos asociados a una entidad invocada/spawned.

    Atributos
        - lifetime (float): duración en segundos tras la cual la entidad expira (0 = infinito).
        - spawned_at (float): timestamp (time.time()) de cuando fue creada la entidad.
    
    Propósito
        - Encapsular la información de vida temporal para invocaciones y efectos.
    """
    lifetime: float = 0.0
    spawned_at: float = 0.0

@dataclass
class Stats:
    """
    Descripción
        CLASE: Estadísticas básicas de una entidad (salud, daños, cooldowns).

    Atributos
        - alive (bool): indicador de vida (True = vivo).
        - health (float): puntos de vida actuales.
        - mana (Optional[float]): recurso secundario (si aplica).
        - armor (Optional[float]): valor de armadura/reducción de daño.
        - mele_dmg (Optional[float]): daño cuerpo a cuerpo.
        - mele_cooldown (Optional[float]): tiempo entre ataques cuerpo a cuerpo.
        - magic_dmg (Optional[float]): daño a distancia.
        - magic_cooldown (Optional[float]): tiempo entre ataques a distancia.
    
    Propósito
        - Proveer un contenedor simple para estadísticas usadas por la lógica de combate.
    """
    alive: bool = True
    health: float = 100.0
    mana: Optional[float] = 100.0
    armor: Optional[float] = 0.0
    mele_dmg: Optional[float] = 20.0
    mele_cooldown: Optional[float] = 3.0
    magic_dmg: Optional[float] = 25.0
    magic_cooldown: Optional[float] = 3.5

@dataclass
class Sprite:
    """
    Descripción
        CLASE: Metadatos para carga de sprite/animaciones.

    Atributos
        - name (str): nombre base del sprite/archivo (ej. 'gargant-berserker').
        - frame_duration (Optional[float]): duración por frame en segundos.
        - scale (Optional[float]): factor de escala aplicado al sprite.
    
    Propósito
        - Centralizar la información necesaria para load_animations en Enemy.
    """
    name: str
    frame_duration: Optional[float] = 0.12
    scale: Optional[float] = 1.25

@dataclass
class EntitySpec:
    """
    Descripción
        CLASE: Especificación tipada y compacta para crear una entidad/enemigo.

    Atributos
        - id (str): identificador único del spec (útil para debugging y mapeos).
        - sprite (Sprite): metadatos del sprite asociado.
        - initial_position (Tuple[float, float]): posición inicial (x, z) en el mapa.
        - collider_box (Tuple[float, float]): dimensiones de la caja de colisión (w, h).
        - initial_algorithm (str): algoritmo inicial activo (clave de CONF.ALG.ALGORITHM).
        - alg_configs (Dict[str, AlgorithmConfigType]): mapeo algoritmo -> config específica.
        - statistics (Optional[Stats]): estadísticas iniciales de la entidad.
        - behavior (Optional[str | dict]): referencia al spec HSM (string para resolver o dict inline).
        - spawn_meta (Optional[SpawnedEntityMeta]): metadatos de spawn/vida temporal.
    
    Métodos y Funciones
        - Ninguno

    Propósito
        - Proveer una representación clara, tipada y portable de los parámetros necesarios
          para instanciar enemigos en el EntityManager y para el tuning por algoritmo.
    """
    id: str
    sprite: Sprite
    initial_position: Tuple[float, float]
    collider_box: Tuple[float, float]
    initial_algorithm: str
    alg_configs: Dict[str, AlgorithmConfigType]
    statistics: Optional[Stats] = None
    behavior: Optional[Dict] = None
    spawn_meta: Optional[SpawnedEntityMeta] = None