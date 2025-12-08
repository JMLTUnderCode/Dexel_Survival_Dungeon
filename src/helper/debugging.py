import pygame
import math
from configs.package import CONF

def draw_node_location(game_surface: pygame.Surface, game_map, entity_manager, camera_x: float, camera_z: float):
    if CONF.DEV.NODE_LOCATION and game_map and game_map.navmesh:
        for entity in entity_manager.enemies + ([entity_manager.player] if entity_manager.player else []):
            node = getattr(entity, "node_location", None)
            if node and getattr(node, "polygon", None):
                pts = [(int(p[0] - camera_x), int(p[1] - camera_z)) for p in node.polygon]
                pygame.draw.polygon(game_surface, (255, 0, 0), pts, 2)

def draw_tactical_types(navmesh, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
    """
    Descripción
        MÉTODO: Dibuja los tipos tácticos de cada nodo en la superficie indicada.

    Argumentos
        - surface (pygame.Surface) : Superficie destino donde dibujar.
        - camera_x (float) : Coordenada X de la cámara.
        - camera_z (float) : Coordenada Z de la cámara.

    Retorno
        - Ninguno
    """
    # 1. Iterar nodos y dibujar el tipo táctico en el centro
    for node in navmesh.nodes.values():
        if node.tactical_type is None:
            continue

        center_on_camera = (node.center[0] - camera_x, node.center[1] - camera_z)
        text_surf = navmesh.debug_font.render(node.tactical_type, True, (0, 255, 0))
        text_rect = text_surf.get_rect(center=(int(center_on_camera[0]), int(center_on_camera[1])))
        surface.blit(text_surf, text_rect)
        
        # 2. Dibujar borde del polígono
        points_on_camera = [(p[0] - camera_x, p[1] - camera_z) for p in node.polygon]
        pygame.draw.polygon(surface, (255, 255, 0), points_on_camera, 2)

def draw_tactical_nodes(game_surface: pygame.Surface, game_map, entity_manager, camera_x: float, camera_z: float):
    if CONF.DEV.TACTICAL_TYPES and game_map and game_map.navmesh:
        draw_tactical_types(game_map.navmesh, game_surface, camera_x, camera_z)

        # Dibujar si un nodo Cover es valido o no
        # Buscar candidatos Cover
        px, pz = entity_manager.player.get_pos()
        nodes_map = game_map.navmesh.nodes
        
        for node in nodes_map.values():
            # Filtro Estático: cover
            if node.tactical_type not in ["cover"]:
                continue
            
            # Filtro Dinámico de Seguridad:
            # El punto debe estar LEJOS del jugador para ser considerado una opción.
            nx, nz = node.center
            dist_to_player = math.hypot(nx - px, nz - pz)
            
            if dist_to_player >= 440.0:
                color = (0, 255, 0)  # Verde: Válido
            else:
                color = (255, 0, 0)  # Rojo: No válido
            
            pygame.draw.circle(game_surface, color, (int(nx - camera_x), int(nz - camera_z + 20)), 6)

def update_enemy_paths_to(entity_manager, event, ui_panel_width: float, camera_x: float, camera_z: float):
    # Verificar que el modo pathfinder está activo y que el evento es un clic izquierdo fuera del panel de UI
    if (CONF.DEV.PATHFINDER and 
        event.type == pygame.MOUSEBUTTONDOWN and 
        event.button == 1 and 
        event.pos[0] >= ui_panel_width):
        # Convertir coords de pantalla -> coords world
        world_x = event.pos[0] - ui_panel_width + camera_x
        world_z = event.pos[1] + camera_z
        entity_manager.update_enemy_paths_to((world_x, world_z))

def draw_collision_box(entity, surface: pygame.Surface, sx: float, sz: float) -> None:
    """
    Descripción
        MÉTODO: Dibuja la caja de colisión de la entidad para depuración.

    Argumentos
        - entity: Entidad asociada a la caja de colisión.
        - surface (pygame.Surface): Superficie destino.
        - sx (float): Posición en x relativa a la cámara.
        - sz (float): Posición en z relativa a la cámara.
    """
    # 1. Calcular rectángulo centrado en la posición del jugador
    box = pygame.Rect(
        int(sx - entity.collider_box[0] // 2),
        int(sz - entity.collider_box[1] // 2),
        int(entity.collider_box[0]),
        int(entity.collider_box[1]),
    )
    pygame.draw.rect(surface, (0, 255, 0), box, 1)

def draw_enemy_overlays(enemy, surface, sx, sz, camera_x, camera_z):
    font = pygame.font.SysFont("Segoe UI", 20, bold=True)
    anim_h = enemy.current_animation.get_size()[1]
    base_y = sz - (anim_h // 2) - 40
    _, line_h = font.size("Mg")

    # 5.1 Mostrar algoritmo activo si está habilitado
    if CONF.DEV.ACTIVE_ALG:
        start_y = base_y + (line_h * 2)
        alg_text = enemy.algorithm.value.upper() if hasattr(enemy.algorithm, "value") else str(enemy.algorithm).upper()
        ts = font.render(alg_text, True, (0, 255, 0))
        tw, th = ts.get_size()
        y = int(start_y - line_h) - th
        surface.blit(ts, (sx - tw // 2, y))

    # 5.2 Mostrar historial HSM si existe
    if CONF.DEV.HSM and getattr(enemy, "behavior", None):
        stack = enemy.behavior.get_active_stack()
        
        start_y = base_y
        if CONF.DEV.HSM_HISTORY and stack:
            rep = " > ".join(stack)
            hist = getattr(enemy, "_hsm_stack_history", [])
            if not hist or hist[-1] != rep:
                hist.append(rep)
                if len(hist) > CONF.DEV.MAX_HSM_HISTORY_SIZE:
                    hist.pop(0)
                enemy._hsm_stack_history = hist

            start_y -= (line_h * (len(enemy._hsm_stack_history) - 1))
            for i, line in enumerate(enemy._hsm_stack_history):
                ts = font.render(line, True, (255, 255, 255))
                tw, th = ts.get_size()
                y = int(start_y + i * line_h) - th
                surface.blit(ts, (sx - tw // 2, y))

        # 5.2.1 Mostrar comportamiento activo en pantalla si está habilitado
        if CONF.DEV.ACTIVE_BEHAVIOR:
            behavior_text = enemy.behavior.get_name().upper()
            ts = font.render(behavior_text, True, (0, 255, 0))
            tw, th = ts.get_size()
            y = int(start_y - line_h) - th
            surface.blit(ts, (sx - tw // 2, y))

    # 5.3 Opciones de debug adicionales: colisión y paths
    if CONF.DEV.COLLISION_RECTS:
        draw_collision_box(enemy, surface, sx, sz)

    if CONF.DEV.PATHFOLLOWER and hasattr(enemy, "follow_path") and enemy.follow_path is not None:
        path = getattr(enemy.follow_path, "path", None)
        if path is not None:
            path.draw(surface, camera_x, camera_z, color=(0, 255, 0), width=2)

    if CONF.DEV.TEMP_PATHFOLLOWER and getattr(enemy, "temp_follow_path", None) is not None:
        path = getattr(enemy.temp_follow_path, "path", None)
        if path is not None:
            path.draw(surface, camera_x, camera_z, color=(0, 0, 255), width=2)

def draw_player_pivots(player, surface, camera_x, camera_z):
    if CONF.DEV.PIVOTS:
        pmx, pmy = player.pivot_point_move.position
        screen_pmx = pmx - camera_x
        screen_pmy = pmy - camera_z
        pygame.draw.circle(surface, (0, 255, 0), (int(screen_pmx), int(screen_pmy)), 4)

        # dibujar corona mínima y máxima alrededor del player para visualizar límites
        player_screen = (int(player.position[0] - camera_x), int(player.position[1] - camera_z))
        if player.pivot_max_radius > 0:
            pygame.draw.circle(surface, (0, 100, 255), player_screen, int(player.pivot_max_radius), 1)

        mmx, mmy = player.pivot_point_mouse.position
        screen_mmx = mmx - camera_x
        screen_mmy = mmy - camera_z
        pygame.draw.circle(surface, (255, 200, 0), (int(screen_mmx), int(screen_mmy)), 4)

def draw_player_overlays(player, surface, sx, sz, camera_x, camera_z):
    # Cuadro de colisión
    if CONF.DEV.COLLISION_RECTS:
        draw_collision_box(player, surface, sx, sz)
    
    # Dibujar pivotes y coronas mín/máx del pivot_move
    if CONF.DEV.PIVOTS:
        draw_player_pivots(player, surface, camera_x, camera_z)