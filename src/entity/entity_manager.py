from __future__ import annotations
import math
import time
import pygame
from typing import Optional, List, Dict, Any
from entity.kinematic import Kinematic
from entity.entity_spec import EntitySpec, Stats, Sprite, SpawnedEntityMeta
from entity.player import Player
from entity.enemy import Enemy
from map.paths import Path
from map.pathfinder import Pathfinder
from map.tactical_pathfinder import TacticalPathfinder
import algorithms.algorithms_configs as ALG_CONF
from entity.floating_text import FloatingText
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
        - tactical_pathfinder (Optional[TacticalPathfinder]): Pathfinding táctico para nodos estratégicos.
        - kills (int): Contador de enemigos eliminados.
        - attack_effects (List[Dict[str, Any]]): Efectos visuales/lógicos (AOE/VFX) activos.
        - floating_texts (List[FloatingText]): Lista de textos de daño flotantes activos.

    Métodos y Funciones
        - create_player: Crea y registra la instancia del jugador principal.
        - create_enemy_from_data: Fabrica un enemigo basado en una especificación de datos.
        - remove_dead_enemies: Elimina enemigos muertos y gestiona expiración por tiempo.
        - clear_all: Resetea todo el estado del gestor.
        - create_enemy_group: Genera un grupo de enemigos desde configuraciones predefinidas.
        - update_enemy_paths_to: Recalcula rutas de enemigos hacia un objetivo.
        - spawn_damage_text: Genera un efecto visual de texto de daño.
        - resolve_attack_damage: Calcula colisiones y aplica daño de ataques activos.
        - update: Ciclo principal de actualización del gestor.
        - draw_floating_texts: Renderiza los textos flotantes en pantalla.

    Propósito
        - Centralizar la lógica de ciclo de vida, interacción y actualización de todas las entidades dinámicas del juego.
    """
    def __init__(self) -> None:
        # 1. Inicializar contenedores y estado
        self.player: Optional[Player] = None
        self.enemies: List[Enemy] = []
        self.pathfinder: Optional[Pathfinder] = None
        self.tactical_pathfinder: Optional[TacticalPathfinder] = None
        self.kills: int = 0
        self.attack_effects: List[Dict[str, Any]] = []
        self.floating_texts: List[FloatingText] = []

    def create_player(self) -> Player:
        """
        Descripción
            MÉTODO: Crear y registrar la instancia del jugador.

        Argumentos
            - Ninguno

        Retorno
            - Player: instancia creada y registrada.
        """
        # 1. Preparar datos de configuración del player
        player_data = EntitySpec(
            id=1,
            sprite=Sprite(name="oldman", frame_duration=0.0592),
            initial_position=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 34, CONF.MAIN_WIN.RENDER_TILE_SIZE * 36),
            collider_box=(CONF.PLAYER.COLLIDER_BOX_WIDTH, CONF.PLAYER.COLLIDER_BOX_HEIGHT),
            initial_algorithm=CONF.ALG.ALGORITHM.FACE,
            alg_configs={
                CONF.ALG.ALGORITHM.ARRIVE_DYNAMIC: ALG_CONF.DynamicArriveConfig(
                    max_speed=220.0,
                    target_radius_dist=40.0,
                    slow_radius_dist=160.0,
                    time_to_target=0.1,
                    max_acceleration=400.0
                ),
                CONF.ALG.ALGORITHM.FACE: ALG_CONF.FaceConfig(
                    target_radius_deg=5 * CONF.CONST.CONVERT_TO_RAD,
                    slow_radius_deg=50 * CONF.CONST.CONVERT_TO_RAD,
                    time_to_target=0.1,
                    max_rotation=3.0,
                    max_angular_accel=35.0
                ),
            },
            statistics=Stats(alive=True, health=300.0, mele_dmg=15.0, mele_cooldown=0.8, magic_cooldown=1.0, magic_dmg=20.0)
        )

        # 2. Crear la instancia del player y guardarla en el manager
        self.player = Player(player_data)
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
        # 1. Resolver target por defecto (player) si no se especifica
        if target is None:
            target = self.player
        
        enemy = None
        try:
            # 2. Instanciar Enemy pasando la especificación
            enemy = Enemy(target=target, spec=spec, entity_manager=self)

            # 3. Registrar la entidad en la lista y retornar
            self.enemies.append(enemy)
        except Exception as exc:
            print(f"[EntityManager.create_enemy_from_data] Error: {exc}")
        
        return enemy

    def remove_dead_enemies(self) -> None:
        """
        Descripción
            MÉTODO: Purga enemigos muertos y expira invocados por su `lifetime`.

        Argumentos
            - Ninguno
        """
        try:
            now = time.time()

            # 1. Expirar invocados por lifetime (spawn_meta)
            for enemy in list(self.enemies):
                spawn_meta: Optional[SpawnedEntityMeta] = getattr(enemy, "spawn_meta", None)
                if spawn_meta:
                    lifetime = getattr(spawn_meta, "lifetime", 0.0)
                    spawned_at = getattr(spawn_meta, "spawned_at", 0.0)
                    
                    # 1.1 Verificar si ha excedido su tiempo de vida
                    if lifetime and lifetime > 0.0 and (now - spawned_at) >= lifetime:
                        try:
                            enemy.die()
                        except Exception:
                            enemy.alive = False

            # 2. Filtrar la lista de enemigos manteniendo solo los vivos
            alive_list: List[Enemy] = []
            for e in self.enemies:
                if getattr(e, "alive", True):
                    alive_list.append(e)
                else:
                    # 2.1 Incrementar contador de bajas si la entidad murió
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
        # 1. Iterar sobre cada enemigo para actualizar su ruta
        for enemy in list(self.enemies):
            # 1.1 Solo actualizar si no tiene un behavior complejo (IA simple)
            if getattr(enemy, "behavior", None) is None:
                start = enemy.get_pos()
                if not self.pathfinder:
                    continue
                
                # 1.2 Calcular ruta usando pathfinder
                pts = self.pathfinder.find_path(start, target_pos)
                if not pts:
                    continue
                
                # 1.3 Crear objeto Path y asignarlo a la instancia follow_path si existe
                poly = Path(pts, closed=False)
                if getattr(enemy, "follow_path", None):
                    enemy.follow_path.path = poly

    def spawn_damage_text(self, position: tuple[float, float], damage: float) -> None:
        """
        Descripción
            MÉTODO: Crea un nuevo texto flotante de daño en la posición indicada.

        Argumentos
            - position (tuple): Coordenadas (x, z) donde aparece el texto.
            - damage (float): Valor del daño a mostrar.
        """
        # 1. Crear instancia de texto flotante y añadir a la lista activa
        ft = FloatingText(position, int(damage))
        self.floating_texts.append(ft)

    def resolve_attack_damage(self) -> None:
        """
        Descripción
            MÉTODO: Resuelve el daño de los ataques activos (Mele y Magic) basándose en la posición
            visual de los efectos. Se ejecuta frame a frame.
        
        Argumentos
            - Ninguno
        """
        # 1. Recopilar todas las entidades vivas (Player + Enemigos)
        all_entities: List[Kinematic] = []
        if self.player and self.player.is_alive():
            all_entities.append(self.player)
        all_entities.extend([e for e in self.enemies if e.is_alive()])

        # 2. Iterar sobre cada entidad para verificar si está atacando
        for attacker in all_entities:
            # 2.1 Verificar si tiene un efecto activo y si NO ha aplicado daño aún
            if getattr(attacker, "current_effect", None) and not getattr(attacker, "current_effect", None).is_finished:
                if not attacker.effect_damage_applied:
                    
                    # 3. Obtener posición del "hitbox" del efecto
                    hit_pos = attacker.get_current_effect_center()
                    if not hit_pos:
                        continue
                    
                    # 4. Definir objetivos (Player ataca Enemigos, Enemigos atacan Player)
                    targets = []
                    if isinstance(attacker, Player):
                        targets = [e for e in self.enemies if e.is_alive()]
                    elif isinstance(attacker, Enemy) and self.player and self.player.is_alive():
                        targets = [self.player]
                    
                    # 5. Definir radio de colisión del efecto
                    effect_radius = 24.0 

                    # 6. Verificar colisión contra objetivos
                    hit_occurred = False
                    for target in targets:
                        tx, tz = target.get_pos()
                        hx, hz = hit_pos
                        dist = math.hypot(tx - hx, tz - hz)
                        
                        target_radius = 24.0
                        
                        # 6.1 Comprobar intersección de radios
                        if dist < (effect_radius + target_radius):
                            # 7. ¡IMPACTO! Aplicar daño según tipo de ataque
                            dmg = 0.0
                            if attacker.current_effect_type == "mele":
                                dmg = getattr(attacker, "mele_dmg", 10.0)
                            elif attacker.current_effect_type == "magic":
                                dmg = getattr(attacker, "magic_dmg", 15.0)
                            
                            target.take_damage(dmg)
                            
                            # 7.1 Generar texto flotante de daño
                            self.spawn_damage_text(target.get_pos(), dmg)
                            
                            hit_occurred = True
                            
                    # 8. Si hubo al menos un impacto, marcar el efecto como "gastado"
                    if hit_occurred:
                        attacker.effect_damage_applied = True
                        # 8.1 Si es magia, finalizar visualmente el proyectil al impactar
                        if attacker.current_effect_type == "magic":
                            attacker.current_effect.finished = True

    def update(self, dt: float) -> None:
        """
        Descripción
            MÉTODO: Actualización centralizada del manager. Ejecuta la resolución de daños,
            procesamiento de ataques, limpieza de entidades y actualización de UI de mundo.

        Argumentos
            - dt (float): Delta time en segundos.
        """
        # 1. Resolver daños por colisión de efectos visuales (Hitbox activa)
        self.resolve_attack_damage()

        # 2. Eliminar enemigos muertos o expirados
        self.remove_dead_enemies()

        # 3. Actualizar textos flotantes
        for ft in self.floating_texts:
            ft.update(dt)
        
        # 4. Limpiar textos expirados de la lista
        self.floating_texts = [ft for ft in self.floating_texts if ft.is_alive()]

    def draw_floating_texts(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja todos los textos flotantes activos.

        Argumentos
            - surface (pygame.Surface): Superficie de destino.
            - camera_x (float): Posición X de la cámara.
            - camera_z (float): Posición Z de la cámara.
        """
        # 1. Iterar y dibujar cada texto flotante
        for ft in self.floating_texts:
            ft.draw(surface, camera_x, camera_z)