from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from characters.player import Player
from characters.enemy import Enemy
from data.enemies import list_of_enemies_data, map_levels_enemies_data
from configs.package import CONF

if TYPE_CHECKING:
    from kinematics.kinematic import Kinematic

class EntityManager:
    """
    Gestiona la creación, almacenamiento y acceso a todas las entidades del juego.
    Utiliza un patrón Factory para centralizar la lógica de instanciación.
    """
    def __init__(self):
        self.player: Optional[Player] = None
        self.enemies: list[Enemy] = []

    def create_player(self, **kwargs) -> Player:
        """
        Factory para crear una instancia del jugador.
        Argumentos clave (kwargs) pueden sobreescribir los valores por defecto.
        """
        defaults = {
            "type": "oldman",
            "position": (CONF.MAIN_WIN.RENDER_TILE_SIZE * 25, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
            "collider_box": (CONF.PLAYER.COLLIDER_BOX_WIDTH, CONF.PLAYER.COLLIDER_BOX_HEIGHT),
            "max_speed": 250,
        }
        config = {**defaults, **kwargs}
        
        self.player = Player(**config)
        return self.player

    def create_enemy_from_data(self, enemy_data: dict, target: Optional[Kinematic] = None) -> Enemy:
        """
        Factory para crear una instancia de un enemigo a partir de un diccionario de datos.
        Si el target no se provee, intenta usar el jugador principal.
        """
        if target is None:
            target = self.player

        enemy = Enemy(
            type=enemy_data["type"],
            position=enemy_data["position"],
            collider_box=enemy_data["collider_box"],
            target=target,
            algorithm=enemy_data["algorithm"],
            max_speed=enemy_data.get("max_speed", 200.0),
            target_radius=enemy_data.get("target_radius", 40.0),
            slow_radius=enemy_data.get("slow_radius", 150.0),
            time_to_target=enemy_data.get("time_to_target", 0.15),
            max_acceleration=enemy_data.get("max_acceleration", 300.0),
            max_rotation=enemy_data.get("max_rotation", 1.0),
            max_angular_accel=enemy_data.get("max_angular_accel", 8.0),
            path_type=enemy_data.get("path_type"),
            path_params=enemy_data.get("path_params"),
            path_offset=enemy_data.get("path_offset", 12.0),
        )
        self.enemies.append(enemy)
        return enemy

    def create_enemy_group(self, group_key: str, group_type: str) -> None:
        """
        Crea un grupo de enemigos basado en una clave del diccionario de datos y el tipo de grupo.
        """
        self.enemies.clear()
        enemy_group_data = []
        if group_type == "map" and group_key in map_levels_enemies_data:
            enemy_group_data = map_levels_enemies_data[group_key]
        
        if group_type == "alg" and group_key in list_of_enemies_data:
            enemy_group_data = list_of_enemies_data[group_key]
        
        for enemy_data in enemy_group_data:
            self.create_enemy_from_data(enemy_data)

    def clear_all(self):
        """Elimina todas las entidades."""
        self.player = None
        self.enemies.clear()