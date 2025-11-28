from __future__ import annotations
import math
import time
import random
import importlib
import traceback
from typing import Optional, List, Dict, Any

from entity.kinematic import Kinematic
from entity.entity_spec import *
from entity.player import Player
from entity.enemy import Enemy
from map.paths import Path
from map.pathfinder import Pathfinder
from ai.behavior import Behavior
from data.map_enemies import MAP_ENEMIES_DATA
from data.algorithm_enemies import ALGORITHM_ENEMIES_DATA
from configs.package import CONF

class EntityManager:
    """
    Descripción
        CLASE: Gestor central de entidades del juego. Encapsula creación,
        registro, gestión por-frame y limpieza de jugadores, enemigos y efectos.

    Atributos
        - player (Optional[Player]): Referencia al jugador principal.
        - enemies (List[Enemy]): Lista de enemigos activos en el mundo.
        - pathfinder (Optional[Pathfinder]): Referencia al pathfinder usado para rutas.
        - kills (int): Contador simple de enemigos eliminados.
        - attack_effects (List[Dict[str, Any]]): Efectos (AOE/VFX) gestionados por el manager.
        - _spawned_entities_meta (List[Dict[str, Any]]): Metadatos para invocados (lifetime, spawn time).
    
    Métodos y Funciones
        - create_player: Fabrica y registra el jugador.
        - create_enemy_from_data: Fabrica un enemigo completo desde un spec.
        - spawn_enemy: Fabrica enemigos ligeros para IA (invocaciones).
        - spawn_attack_effect: Registra efectos de ataque (visual/lógico).
        - process_player_attacks: Aplica ondas de ataque del jugador sobre enemigos.
        - remove_dead_enemies: Purga enemigos muertos y expira invocados por lifetime.
        - update: Mantenimiento por-frame (debe llamarse desde game loop).
        - clear_all: Limpia todas las colecciones internas.
        - create_enemy_group: Construye grupo de enemigos desde datos.
        - update_enemy_paths_to: Recalcula rutas para todos los enemigos.
    """
    def __init__(self):
        # 1. Inicializar atributos contenedores
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.pathfinder: Optional[Pathfinder] = None
        self.kills: int = 0
        self.attack_effects: List[Dict[str, Any]] = []
        # Cada meta: {"entity": Enemy, "lifetime": float, "spawned_at": float}
        self._spawned_entities_meta: List[Dict[str, Any]] = []

    def create_player(self, **kwargs) -> Player:
        """
        Descripción
            MÉTODO: Crear y registrar la instancia del jugador.

        Argumentos
            - kwargs (dict): Parámetros opcionales para el constructor del jugador.

        Retorno
            - Player: instancia creada y registrada.
        """
        defaults = {
            "type": "oldman",
            "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 20, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
            "collider_box": (CONF.PLAYER.COLLIDER_BOX_WIDTH, CONF.PLAYER.COLLIDER_BOX_HEIGHT),
            "max_speed": 250,
        }
        config = {**defaults, **kwargs}
        # Crear player y registrar
        self.player = Player(**config)
        return self.player

    def create_enemy_from_data(self, spec: EntitySpec, target: Optional[Kinematic] = None) -> Enemy:
        """
        Descripción
            MÉTODO: Fabrica un enemigo completo a partir de una especificación.
        
        Argumentos
            - enemy_data (dict): Especificación completa del enemigo (keys: type, position, collider_box, algorithm, ...).
            - target (Optional[Kinematic]): Target para la entidad (por defecto self.player).
        
        Retorno
            - Enemy: instancia creada y añadida a self.enemies.
        """
        # 1. Default target fallback
        if target is None:
            target = self.player

        # 2. Instanciar Enemy usando campos provistos
        enemy = Enemy(
            target=target,
            spec=spec
        )

        # 3. Attach behavior if provided (resolve string names)
        behavior_spec = spec.behavior
        if behavior_spec:
            try:
                if isinstance(behavior_spec, str):
                    try:
                        data_mod = importlib.import_module("data.enemies")
                        resolved = getattr(data_mod, behavior_spec, None)
                        if resolved is not None:
                            behavior_spec = resolved
                    except Exception:
                        # best-effort resolution, continue if fails
                        pass
                enemy.behavior = Behavior.from_spec(behavior_spec, enemy, self)
                if enemy.behavior is None:
                    print(f"[EntityManager] Behavior.from_spec returned None for enemy '{enemy.type}'")
            except Exception as exc:
                print(f"[EntityManager] Error building behavior for enemy '{enemy.type}': {exc}")
                print(traceback.format_exc())
                enemy.behavior = None

        # 4. Registrar y retornar
        self.enemies.append(enemy)
        return enemy

    def spawn_attack_effect(self, effect_name: str, *, position: tuple[float, float], radius: float = 0.0, **kwargs) -> Dict[str, Any]:
        """
        Descripción
            MÉTODO: Registrar y retornar un efecto de ataque (AOE / VFX).
        
        Argumentos
            - effect_name (str): Identificador del efecto.
            - position (tuple): Posición (x,z) donde se crea el efecto.
            - radius (float): Radio del efecto.
            - kwargs: Parámetros adicionales guardados en el efecto.
        
        Retorno
            - dict: Representación del efecto creado.
        """
        try:
            effect = {
                "name": effect_name,
                "position": (float(position[0]), float(position[1])),
                "radius": float(radius),
                "created_at": time.time(),
                **kwargs
            }
            self.attack_effects.append(effect)
            return effect
        except Exception as exc:
            print(f"[EntityManager.spawn_attack_effect] Error: {exc}")
            return {}

    def process_player_attacks(self) -> None:
        """
        Descripción
            MÉTODO: Procesa las ondas de ataque del jugador y aplica daño a enemigos dentro del radio.
        
        Blackboard/estado usado
            - player.attack_waves (read): colección de ondas pendientes.
        """
        # 1. Validaciones rápidas
        if not self.player:
            return
        if not self.enemies:
            return

        # 2. Iterar ondas y aplicar daño por proximidad
        for wave in list(self.player.attack_waves):
            if not getattr(wave, "applied", False):
                wx, wz = wave.x, wave.z
                r = wave.max_radius
                for enemy in list(self.enemies):
                    if not getattr(enemy, "alive", True):
                        continue
                    ex, ez = enemy.get_pos()
                    dist = math.hypot(ex - wx, ez - wz)
                    if dist <= r:
                        dmg = 0.20 * getattr(enemy, "max_health", 100.0)
                        try:
                            enemy.take_damage(dmg)
                        except Exception:
                            enemy.health = max(0.0, getattr(enemy, "health", 0.0) - dmg)
                
                wave.mark_applied()

    def remove_dead_enemies(self) -> None:
        """
        Descripción
            MÉTODO: Purga enemigos muertos y expira invocados por su `lifetime`.
        
        Detalle
            - Revisa self._spawned_entities_meta para expirar entidades invocadas por lifetime.
            - Llama a die() si existe; si no, marca alive=False.
            - Elimina de self.enemies las entidades no vivas y actualiza self.kills.
        """
        try:
            now = time.time()

            # 1. Expirar invocados por lifetime
            for enemy in self.enemies:
                if getattr(enemy, "spawn_meta", None):
                    lifetime = enemy.spawn_meta.lifetime
                    spawned_at = enemy.spawn_meta.spawned_at
                    if lifetime > 0.0 and (now - spawned_at) >= lifetime:
                        enemy.die()

            # 2. Remover enemigos muertos de la lista principal
            alive_list: List[Enemy] = []
            for e in self.enemies:
                if getattr(e, "alive", True):
                    alive_list.append(e)
                else:
                    self.kills += 1
            self.enemies = alive_list
        except Exception as exc:
            print(f"[EntityManager.remove_dead_enemies] Error: {exc}")

    def clear_all(self) -> None:
        """
        Descripción
            MÉTODO: Elimina todas las entidades gestionadas y resetea contadores.
        """
        self.player = None
        self.enemies.clear()
        self.attack_effects.clear()
        self._spawned_entities_meta.clear()
        self.kills = 0

    def create_enemy_group(self, group_key: str, group_type: str) -> None:
        """
        Descripción
            MÉTODO: Crea un grupo de enemigos a partir de datos preconfigurados.
        
        Argumentos
            - group_key (str): clave del grupo en los datos.
            - group_type (str): "map" o "alg" para seleccionar dataset.
        """
        self.enemies.clear()
        enemy_group_data = []
        if group_type == "map" and group_key in MAP_ENEMIES_DATA:
            enemy_group_data = MAP_ENEMIES_DATA[group_key]
        if group_type == "alg" and group_key in ALGORITHM_ENEMIES_DATA:
            enemy_group_data = ALGORITHM_ENEMIES_DATA[group_key]
        for enemy_data in enemy_group_data:
            self.create_enemy_from_data(enemy_data)

    def update_enemy_paths_to(self, target_pos: tuple[float, float]) -> None:
        """
        Descripción
            MÉTODO: Recalcula y asigna un nuevo Path a todos los enemigos.

        Argumentos
            - target_pos (tuple): posición objetivo (x,z).
        """
        for enemy in list(self.enemies):
            if getattr(enemy, "behavior", None) is None:
                start = enemy.get_pos()
                if not self.pathfinder:
                    continue
                pts = self.pathfinder.find_path(start, target_pos)
                if not pts:
                    continue
                poly = Path(pts, closed=False)
                if getattr(enemy, "follow_path", None):
                    enemy.follow_path.path = poly