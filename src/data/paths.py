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
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 25, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 49 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2),
            segments=35
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_1 = PathInstance(
        path=make_rectangle_path(
            width=520.0,
            height=280.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 19 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 6 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_2 = PathInstance(
        path=make_rectangle_path(
            width=520.0,
            height=300.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 40 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 6 + CONF.MAIN_WIN.RENDER_TILE_SIZE // 2),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_3 = PathInstance(
        path=make_rectangle_path(
            width=520.0,
            height=320.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 57 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 6 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_4 = PathInstance(
        path=make_rectangle_path(
            width=380.0,
            height=420.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 27 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 30 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_5 = PathInstance(
        path=make_rectangle_path(
            width=380.0,
            height=420.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 17 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 30 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_6 = PathInstance(
        path=make_rectangle_path(
            width=380.0,
            height=420.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 7 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 30 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )

    RECT_ZONE_LEVEL2_7 = PathInstance(
        path=make_rectangle_path(
            width=800.0,
            height=150.0,
            center=(CONF.MAIN_WIN.RENDER_TILE_SIZE * 54 + CONF.MAIN_WIN.RENDER_TILE_SIZE, 
                    CONF.MAIN_WIN.RENDER_TILE_SIZE * 47 + CONF.MAIN_WIN.RENDER_TILE_SIZE),
            segments=20
        ),
        offset=1.0,
        curr_param=0.0
    )