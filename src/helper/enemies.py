from characters.enemy import Enemy
from data.enemies import list_of_enemies_data

def create_enemies(
    algorithm="EMPTY",
    target=None,
):
    if algorithm not in list_of_enemies_data:
        algorithm = "EMPTY" if "EMPTY" in list_of_enemies_data else next(iter(list_of_enemies_data.keys()))
    enemy_list = list_of_enemies_data[algorithm]

    return [
        Enemy(
            type=enemy["type"],
            position=enemy["position"],
            collider_box=enemy["collider_box"],
            target=target,
            algorithm=enemy["algorithm"],
            max_speed=enemy["max_speed"],
            target_radius=enemy["target_radius"],
            slow_radius=enemy["slow_radius"],
            time_to_target=enemy["time_to_target"],
            max_acceleration=enemy["max_acceleration"],
            max_rotation=enemy["max_rotation"],
            max_angular_accel=enemy["max_angular_accel"],
            path_type=enemy.get("path_type", None),
            path_params=enemy.get("path_params", None),
            path_offset=enemy.get("path_offset", 12.0),   
        )
        for enemy in enemy_list
    ]