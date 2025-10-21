from characters.player import Player
from configs.package import CONF

def create_player(
    type="oldman",
    position=(CONF.MAIN_WIN.RENDER_TILE_SIZE*30, CONF.MAIN_WIN.RENDER_TILE_SIZE*30),
    collider_box=(CONF.PLAYER.COLLIDER_BOX_WIDTH, CONF.PLAYER.COLLIDER_BOX_HEIGHT),
    max_speed=250,
):
    return Player(
        type=type,
        position=position,
        collider_box=collider_box,
        max_speed=max_speed,
    )
