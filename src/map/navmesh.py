import pygame
from typing import List, Tuple, Dict
from collections import deque
from matplotlib.path import Path as MplPath

class NavMeshNode:
    """Representa un único polígono transitable (nodo) en el grafo de navegación."""
    def __init__(self, id: int, polygon: List[Tuple[float, float]]):
        self.id = id
        self.polygon = polygon
        self.center = (
            sum(p[0] for p in polygon) / len(polygon),
            sum(p[1] for p in polygon) / len(polygon)
        )
        self.neighbors: List[NavMeshNode] = []
        self.figure = MplPath(self.polygon)

    def contains_point(self, point: Tuple[float, float]) -> bool:
        """
        Devuelve True si `point` (x, y) está dentro del polígono de este nodo..
        """
        return bool(self.figure.contains_point(point))
    
class NavMesh:
    """
    Gestiona el grafo de navegación (NavMesh) construido a partir de polígonos.
    """
    def __init__(self, objects: list, zoom: float):
        self.nodes: Dict[int, NavMeshNode] = {}
        self._build_nodes(objects, zoom)
        self._calculate_edges()

    def get_node_at(self, position: Tuple[float, float]):
        """
        Devuelve el nodo que contiene `position` (x, y) o None si no hay ninguno.
        Útil para ubicar entidades dentro del NavMesh antes de iniciar pathfinding.
        """
        for node in self.nodes.values():
            if node.contains_point(position):
                return node
        return None

    def find_node_from(self, start_node, position: Tuple[float, float]):
        """
        Busca el nodo que contiene `position` partiendo desde `start_node` usando BFS por vecinos.
        - start_node: None, int (node id) o NavMeshNode.
        - position: (x, y) en coordenadas del mundo (ya escaladas).
        Retorna NavMeshNode o None.
        """
        # Resolver start_node a objeto
        if start_node is None:
            return self.get_node_at(position)

        if isinstance(start_node, int):
            start = self.nodes.get(start_node)
        else:
            start = start_node

        if start is None:
            return self.get_node_at(position)

        # Si la posición sigue dentro del nodo, devolverlo rápido
        if start.contains_point(position):
            return start

        # BFS limitado por vecinos (asume no teleport)
        visited = set()
        q = deque([start])
        visited.add(start.id)

        while q:
            node = q.popleft()
            for nb in node.neighbors:
                if nb.id in visited:
                    continue
                if nb.contains_point(position):
                    return nb
                visited.add(nb.id)
                q.append(nb)

        # No encontrado en la componente conectada desde start -> fallback global
        return self.get_node_at(position)
      
    def _build_nodes(self, objects: list, zoom: float):
        """Crea los nodos del grafo a partir de los objetos poligonales de Tiled."""
        for obj in objects:
            # La condición clave: el objeto debe tener un atributo 'points' y no debe estar vacío.
            if not hasattr(obj, 'points') or not obj.points:
                continue

            try:
                # Los puntos en obj.points son objetos Point con atributos .x y .y.
                # Ya están en coordenadas absolutas del mapa, solo necesitamos aplicar el zoom.
                polygon_points = [
                    (p.x * zoom, p.y * zoom) 
                    for p in obj.points
                ]
                
                # Usamos el ID único del objeto de Tiled como clave para nuestro nodo.
                # Esto es más robusto que usar 'name', que puede repetirse o ser None.
                node_id = obj.id
                self.nodes[node_id] = NavMeshNode(node_id, polygon_points)

            except Exception as e:
                print(f"[Error] Fallo al procesar el objeto de NavMesh con ID {obj.id}: {e}")

    def _calculate_edges(self):
        """
        Calcula las conexiones (aristas) entre nodos adyacentes.
        Dos nodos se consideran adyacentes si sus polígonos comparten un borde.
        """
        node_list = list(self.nodes.values())
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                node_a = node_list[i]
                node_b = node_list[j]

                if self._polygons_share_border(node_a.polygon, node_b.polygon):
                    node_a.neighbors.append(node_b)
                    node_b.neighbors.append(node_a)

    def _polygons_share_border(self, poly1: list, poly2: list) -> bool:
        """Determina si dos polígonos comparten un borde colisionando sus segmentos."""
        for i in range(len(poly1)):
            p1 = poly1[i]
            p2 = poly1[(i + 1) % len(poly1)] # Segmento p1-p2

            for j in range(len(poly2)):
                p3 = poly2[j]
                p4 = poly2[(j + 1) % len(poly2)] # Segmento p3-p4

                # Si los segmentos son colineales y se solapan, están compartiendo un borde.
                if self._are_segments_collinear_and_overlapping(p1, p2, p3, p4):
                    return True
        return False

    def _are_segments_collinear_and_overlapping(self, p1: tuple, p2: tuple, p3: tuple, p4: tuple) -> bool:
        """
        Verifica si dos segmentos de línea son colineales y si su solapamiento
        es mayor que un solo punto (es decir, comparten un borde real).
        """
        # Tolerancia para comparaciones de punto flotante
        epsilon = 1e-5

        # 1. Comprobar colinealidad
        # Vector del primer segmento
        vec1 = (p2[0] - p1[0], p2[1] - p1[1])
        # Vectores desde el inicio del primer segmento a los puntos del segundo
        vec2 = (p3[0] - p1[0], p3[1] - p1[1])
        vec3 = (p4[0] - p1[0], p4[1] - p1[1])
        
        # El producto cruzado de los vectores debe ser (casi) cero para ser colineales
        cross_product1 = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        cross_product2 = vec1[0] * vec3[1] - vec1[1] * vec3[0]

        if abs(cross_product1) > epsilon or abs(cross_product2) > epsilon:
            return False # No son colineales

        # 2. Comprobar que el solapamiento es más que un punto
        # Proyectar los segmentos sobre el eje X
        dot_p1 = p1[0]
        dot_p2 = p2[0]
        dot_p3 = p3[0]
        dot_p4 = p4[0]

        # Si el segmento es principalmente vertical, usar el eje Y para mayor precisión
        if abs(vec1[0]) < epsilon:
            dot_p1 = p1[1]
            dot_p2 = p2[1]
            dot_p3 = p3[1]
            dot_p4 = p4[1]

        # Encontrar los puntos de inicio y fin del intervalo de solapamiento
        overlap_start = max(min(dot_p1, dot_p2), min(dot_p3, dot_p4))
        overlap_end = min(max(dot_p1, dot_p2), max(dot_p3, dot_p4))

        # La longitud del solapamiento debe ser mayor que nuestra tolerancia.
        # Si es ~0, solo se tocan en un punto.
        return (overlap_end - overlap_start) > epsilon

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float):
        """Dibuja el NavMesh (polígonos, centros y conexiones)."""
        for node in self.nodes.values():
            # Ajustar los puntos del polígono a la vista de la cámara
            points_on_camera = [(p[0] - camera_x, p[1] - camera_z) for p in node.polygon]
            
            """ # Dibujar el polígono del nodo con transparencia
            poly_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(poly_surface, (0, 100, 255, 100), points_on_camera)
            surface.blit(poly_surface, (0,0))
            """
            pygame.draw.polygon(surface, (255, 255, 0), points_on_camera, 2) # Borde
            
            center_on_camera = (node.center[0] - camera_x, node.center[1] - camera_z)
            
            # Dibujar las aristas (conexiones) a los vecinos
            for neighbor in node.neighbors:
                neighbor_center_on_camera = (neighbor.center[0] - camera_x, neighbor.center[1] - camera_z)
                pygame.draw.line(surface, (39, 245, 242), center_on_camera, neighbor_center_on_camera, 2)
            
            # Dibujar el centro del nodo
            pygame.draw.circle(surface, (255, 0, 0), center_on_camera, 4) # Círculo rojo