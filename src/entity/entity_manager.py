from __future__ import annotations
import math
import time
import importlib
import traceback
from typing import Optional, List, Dict, Any

from entity.kinematic import Kinematic
from entity.entity_spec import EntitySpec, SpawnedEntityMeta
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
        registro, mantenimiento por-frame y limpieza de jugadores, enemigos y efectos.

    Atributos
        - player (Optional[Player]): Referencia al jugador principal.
        - enemies (List[Enemy]): Lista de enemigos activos en el mundo.
        - pathfinder (Optional[Pathfinder]): Pathfinding auxiliar para recalcular rutas.
        - kills (int): Contador de enemigos eliminados.
        - attack_effects (List[Dict[str, Any]]): Efectos visuales/lógicos (AOE/VFX) activos.
    """
    def __init__(self) -> None:
        # 1. Inicializar contenedores y estado
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.pathfinder: Optional[Pathfinder] = None
        self.kills: int = 0
        self.attack_effects: List[Dict[str, Any]] = []

    def create_player(self, **kwargs) -> Player:
        """
        Descripción
            MÉTODO: Crear y registrar la instancia del jugador.

        Argumentos
            - kwargs (dict): Parámetros opcionales para el constructor del jugador.

        Retorno
            - Player: instancia creada y registrada.
        """
        # 1. Preparar valores por defecto y mezclar con overrides
        defaults = {
            "type": "oldman",
            "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 20, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
            "collider_box": (CONF.PLAYER.COLLIDER_BOX_WIDTH, CONF.PLAYER.COLLIDER_BOX_HEIGHT),
            "max_speed": 250,
        }
        config = {**defaults, **kwargs}

        # 2. Crear la instancia del player y guardarla en el manager
        self.player = Player(**config)
        return self.player

    def create_enemy_from_data(self, spec: EntitySpec, target: Optional[Kinematic] = None) -> Enemy:
        """
        Descripción
            MÉTODO: Fabrica un enemigo completo a partir de una especificación tipada (EntitySpec).

        Argumentos
            - spec (EntitySpec): Especificación tipada del enemigo a crear.
            - target (Optional[Kinematic]): Target para la entidad (por defecto self.player).

        Retorno
            - Enemy: instancia creada y añadida a self.enemies.
        """
        # 1. Resolver target por defecto (player)
        if target is None:
            target = self.player

        # 2. Instanciar Enemy pasando la spec
        enemy = Enemy(target=target, spec=spec)

        # 3. Resolver y enlazar behavior si la spec lo define
        behavior_spec = spec.behavior
        if behavior_spec:
            try:
                # 3.1 Si behavior es string intentar resolver desde data.enemies (compatibilidad)
                if isinstance(behavior_spec, str):
                    try:
                        data_mod = importlib.import_module("data.enemies")
                        resolved = getattr(data_mod, behavior_spec, None)
                        if resolved is not None:
                            behavior_spec = resolved
                    except Exception:
                        # best-effort resolution, continuar si falla
                        pass

                # 3.2 Construir Behavior usando el builder central
                enemy.behavior = Behavior.from_spec(behavior_spec, enemy, self)
                if enemy.behavior is None:
                    print(f"[EntityManager] Behavior.from_spec returned None for enemy '{getattr(enemy, 'type', 'unknown')}'")
            except Exception as exc:
                # 3.3 Capturar errores para no romper loop de creación
                print(f"[EntityManager] Error building behavior for enemy '{getattr(enemy, 'type', 'unknown')}': {exc}")
                print(traceback.format_exc())
                enemy.behavior = None

        # 4. Registrar la entidad en la lista y retornar
        self.enemies.append(enemy)
        return enemy

    def spawn_attack_effect(self, effect_name: str, *, position: tuple[float, float], radius: float = 0.0, **kwargs) -> Dict[str, Any]:
        """
        Descripción
            MÉTODO: Registrar y retornar un efecto de ataque (AOE / VFX).

        Argumentos
            - effect_name (str): Identificador del efecto.
            - position (tuple[float, float]): Posición (x,z) donde se crea el efecto.
            - radius (float): Radio del efecto.
            - kwargs: Parámetros adicionales guardados en el efecto.

        Retorno
            - dict: Representación del efecto creado.
        """
        # 1. Construir la estructura del efecto con marca de tiempo
        try:
            effect = {
                "name": effect_name,
                "position": (float(position[0]), float(position[1])),
                "radius": float(radius),
                "created_at": time.time(),
                **kwargs
            }

            # 2. Registrar y devolver
            self.attack_effects.append(effect)
            return effect
        except Exception as exc:
            # 3. Manejo de error defensivo
            print(f"[EntityManager.spawn_attack_effect] Error: {exc}")
            return {}

    def process_player_attacks(self) -> None:
        """
        Descripción
            MÉTODO: Procesa las ondas de ataque del jugador y aplica daño a enemigos dentro del radio.

        Argumentos
            - Ninguno

        Blackboard utilizado/modificado
            - player.attack_waves (read): colección de ondas pendientes del jugador.
        """
        # 1. Validaciones rápidas: requiere player y enemigos
        if not self.player:
            return
        if not self.enemies:
            return

        # 2. Iterar sobre las ondas activas y aplicar daño por proximidad
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
                        # 2.1 Calcular daño y aplicarlo (defensivo ante excepciones)
                        dmg = 0.20 * getattr(enemy, "max_health", 100.0)
                        try:
                            enemy.take_damage(dmg)
                        except Exception:
                            enemy.health = max(0.0, getattr(enemy, "health", 0.0) - dmg)

                # 2.2 Marcar onda como aplicada
                try:
                    wave.mark_applied()
                except Exception:
                    wave.applied = True

    def remove_dead_enemies(self) -> None:
        """
        Descripción
            MÉTODO: Purga enemigos muertos y expira invocados por su `lifetime`.

        Argumentos
            - Ninguno

        Detalle
            - Recorre self.enemies, invoca die() si un invocado excede su lifetime y elimina
              las entidades no vivas, incrementando contador de kills.
        """
        try:
            now = time.time()

            # 1. Expirar invocados por lifetime (spawn_meta)
            for enemy in list(self.enemies):
                spawn_meta: Optional[SpawnedEntityMeta] = getattr(enemy, "spawn_meta", None)
                if spawn_meta:
                    lifetime = getattr(spawn_meta, "lifetime", 0.0)
                    spawned_at = getattr(spawn_meta, "spawned_at", 0.0)
                    if lifetime and lifetime > 0.0 and (now - spawned_at) >= lifetime:
                        try:
                            enemy.die()
                        except Exception:
                            enemy.alive = False

            # 2. Filtrar la lista de enemigos, actualizar contador de bajas
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

        Argumentos
            - Ninguno
        """
        # 1. Resetear referencias y colecciones
        self.player = None
        self.enemies.clear()
        self.attack_effects.clear()
        self.kills = 0

    def create_enemy_group(self, group_key: str, group_type: str) -> None:
        """
        Descripción
            MÉTODO: Crea un grupo de enemigos a partir de datos preconfigurados.

        Argumentos
            - group_key (str): clave del grupo en los datos.
            - group_type (str): "map" o "alg" para seleccionar dataset.
        """
        # 1. Limpiar lista actual de enemigos antes de poblar
        self.enemies.clear()

        # 2. Seleccionar dataset correcto según tipo y clave
        enemy_group_data = []
        if group_type == "map" and group_key in MAP_ENEMIES_DATA:
            enemy_group_data = MAP_ENEMIES_DATA[group_key]
        elif group_type == "alg" and group_key in ALGORITHM_ENEMIES_DATA:
            enemy_group_data = ALGORITHM_ENEMIES_DATA[group_key]

        # 3. Iterar y crear cada enemigo usando create_enemy_from_data
        for enemy_data in enemy_group_data:
            try:
                self.create_enemy_from_data(enemy_data)
            except Exception as exc:
                print(f"[EntityManager.create_enemy_group] Failed to create enemy: {exc}")

    def update_enemy_paths_to(self, target_pos: tuple[float, float]) -> None:
        """
        Descripción
            MÉTODO: Recalcula y asigna un nuevo Path a todos los enemigos.

        Argumentos
            - target_pos (tuple[float,float]): posición objetivo (x,z).
        """
        # 1. Para cada enemigo sin behavior, recalcular path hacia target_pos usando pathfinder
        for enemy in list(self.enemies):
            if getattr(enemy, "behavior", None) is None:
                start = enemy.get_pos()
                if not self.pathfinder:
                    continue
                pts = self.pathfinder.find_path(start, target_pos)
                if not pts:
                    continue
                # 2. Crear objeto Path y asignarlo a la instancia follow_path si existe
                poly = Path(pts, closed=False)
                if getattr(enemy, "follow_path", None):
                    enemy.follow_path.path = poly