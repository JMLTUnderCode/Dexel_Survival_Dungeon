from configs.package import CONF
from map.paths import PathInstance, make_circle_path, make_rectangle_path

class PathsData:
    CIRCLE_ZONE_LEVEL0_1 = PathInstance(
        path=make_circle_path(
            radius=300.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
            segments=48
        ),
        offset=2.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL0_1 = PathInstance(
        path=make_rectangle_path(
            width=700.0, 
            height=700.0, 
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 30, CONF.MAIN_WIN.RENDER_TILE_SIZE * 30),
            segments=70, 
        ),
        offset=3.0,
        curr_param=0.0
    )

    CIRCLE_ZONE_LEVEL2_1 = PathInstance(
        path=make_circle_path(
            radius=260.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 15, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 49 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2),
            segments=35
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_1 = PathInstance(
        path=make_rectangle_path(
            width=540.0,
            height=320.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 9 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 6 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
            segments=30
        ),
        offset=1.0,
        curr_param=0.0
    )