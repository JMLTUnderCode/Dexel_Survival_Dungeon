from characters.player import Player
from characters.enemy import Enemy
from data.enemies import list_of_enemies_data
import utils.configs as configs

# --- Inicial create (por defecto ALL) ---
# Helper para crear player y la lista de enemigos desde una key del data set
def create_player_and_enemies(key="ALL"):
    """
    Crea/Resetea globalmente `player` y `enemies` usando list_of_enemies_data[key].
    Si la key no existe, usa "ALL" o la primera disponible.
    """
    if key not in list_of_enemies_data:
        key = "ALL" if "ALL" in list_of_enemies_data else next(iter(list_of_enemies_data.keys()))
    enemy_list = list_of_enemies_data[key]

    # Re-crear player (reset)
    player = Player(
        type="oldman",
        position=(configs.RENDER_TILE_SIZE*30, configs.RENDER_TILE_SIZE*30),
        collider_box=(configs.PLAYER_COLLIDER_BOX_WIDTH, configs.PLAYER_COLLIDER_BOX_HEIGHT),
        max_speed=210,
    )

    # Re-crear enemies
    enemies = [
        Enemy(
            type=enemy["type"],
            position=enemy["position"],
            collider_box=enemy["collider_box"],
            target=player,
            algorithm=enemy["algorithm"],
            max_speed=enemy["max_speed"],
            target_radius=enemy["target_radius"],
            slow_radius=enemy["slow_radius"],
            time_to_target=enemy["time_to_target"],
            max_acceleration=enemy["max_acceleration"],
            max_rotation=enemy["max_rotation"],
            max_angular_accel=enemy["max_angular_accel"],
        )
        for enemy in enemy_list
    ]

    return player, enemies