import pygame
from typing import List, Tuple, Dict, Optional
from collections import deque
from matplotlib.path import Path as MplPath
from configs.package import CONF

class NavMeshNode:
    """
    Descripción
        CLASE: Representa un único polígono transitable (nodo) en el grafo de navegación.

    Atributos
        - id (int): Identificador único del nodo (usualmente obj.id de Tiled).
        - polygon (List[Tuple[float,float]]): Lista de vértices del polígono en coordenadas del mundo.
        - center (Tuple[float,float]): Centro geométrico del polígono.
        - neighbors (List[NavMeshNode]): Lista de nodos conectados (adyacentes).
        - figure (MplPath): Objeto de Matplotlib para consultas puntuales dentro del polígono.

    Propósito
        - Encapsular la información geométrica y topológica de una región transitable.
    """
    def __init__(self, id: int, polygon: List[Tuple[float, float]]):
        # 1. Guardar identificador y lista de puntos del polígono
        self.id = id
        self.polygon = polygon

        # 2. Calcular centro como promedio de vértices
        self.center = (
            sum(p[0] for p in polygon) / len(polygon),
            sum(p[1] for p in polygon) / len(polygon)
        )

        # 3. Inicializar lista de vecinos y figura para pruebas puntuales
        self.neighbors: List[NavMeshNode] = []
        self.figure = MplPath(self.polygon)

    def contains_point(self, point: Tuple[float, float]) -> bool:
        """
        Descripción
            FUNCIÓN: Comprueba si un punto dado está dentro del polígono de este nodo.

        Argumentos
            - point (Tuple[float,float]) : Punto (x, y) a evaluar en coordenadas del mundo.

        Retorno
            - bool: True si el punto está dentro del polígono, False en caso contrario.
        """
        # 1. Delegar la comprobación al MplPath que contiene el polígono
        return bool(self.figure.contains_point(point))

class NavMesh:
    """
    Descripción
        CLASE: Grafo de navegación construido a partir de objetos poligonales
        extraídos desde Tiled. Provee utilidades para ubicar nodos, construir conexiones
        y realizar búsquedas locales sobre la malla de navegación.

    Atributos
        - nodes (Dict[int, NavMeshNode]): Mapa id -> nodo del NavMesh.
    
    Métodos y Funciones
        - get_node_at: Obtiene el nodo que contiene una posición.
        - find_node_from: Busca un nodo contenedor partiendo desde un nodo inicial mediante BFS.
        - _build_nodes: Construye nodos a partir de objetos Tiled.
        - _calculate_edges: Calcula adyacencias entre nodos.
        - draw: Dibuja el NavMesh para depuración.

    Propósito
        - Proveer utilidades para localizar entidades en la malla y para pathfinding local.
    """
    def __init__(self, objects: list, zoom: float):
        # 1. Inicializar contenedor de nodos
        self.nodes: Dict[int, NavMeshNode] = {}

        # 2. Construir nodos a partir de los objetos provistos y aplicar zoom
        self._build_nodes(objects, zoom)

        # 3. Calcular aristas entre nodos adyacentes
        self._calculate_edges()

    def get_node_at(self, position: Tuple[float, float]) -> Optional[NavMeshNode]:
        """
        Descripción
            FUNCIÓN: Devuelve el nodo que contiene `position` (x, y) o None si no hay ninguno.

        Argumentos
            - position (Tuple[float,float]) : Coordenada (x, y) en el mundo.

        Retorno
            - Optional[NavMeshNode]: Nodo que contiene la posición o None.
        """
        # 1. Iterar sobre los nodos y comprobar pertenencia
        for node in self.nodes.values():
            if node.contains_point(position):
                return node
        # 2. Si ninguno contiene el punto, devolver None
        return None

    def find_node_from(self, start_node, position: Tuple[float, float]) -> Optional[NavMeshNode]:
        """
        Descripción
            FUNCIÓN: Busca el nodo que contiene `position` partiendo desde `start_node` usando BFS sobre vecinos.

        Argumentos
            - start_node (Optional[int|NavMeshNode]) : Nodo de partida (None | node id | NavMeshNode).
            - position (Tuple[float,float]) : Punto objetivo (x, y) en coordenadas del mundo.

        Retorno
            - Optional[NavMeshNode]: Nodo que contiene la posición o None si no se encuentra.
        """
        # 1. Resolver start_node a objeto NavMeshNode si fue pasado como id
        if start_node is None:
            return self.get_node_at(position)

        if isinstance(start_node, int):
            start = self.nodes.get(start_node)
        else:
            start = start_node

        # 2. Si start no existe o la posición está dentro de start, resolver rápido
        if start is None:
            return self.get_node_at(position)

        if start.contains_point(position):
            return start

        # 3. BFS por vecinos para buscar el nodo contenedor en la componente conectada
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

        # 4. Fallback global si no se encontró en la componente conectada
        return self.get_node_at(position)

    def _build_nodes(self, objects: list, zoom: float) -> None:
        """
        Descripción
            MÉTODO: Crea los nodos del grafo a partir de los objetos poligonales de Tiled.

        Argumentos
            - objects (list) : Lista de objetos provenientes de la capa 'graph' de Tiled.
            - zoom (float) : Factor de escala aplicado a las coordenadas de los objetos.
        """
        # 1. Iterar objetos y procesar únicamente los que contienen 'points'
        for obj in objects:
            if not hasattr(obj, 'points') or not obj.points:
                continue

            try:
                # 2. Convertir puntos a tuplas (x*zoom, y*zoom)
                polygon_points = [
                    (p.x * zoom, p.y * zoom)
                    for p in obj.points
                ]

                # 3. Usar obj.id como clave estable para el nodo
                node_id = obj.id
                self.nodes[node_id] = NavMeshNode(node_id, polygon_points)

            except Exception as e:
                # 4. En caso de error, registrar para depuración y continuar
                print(f"[NavMesh] Error al procesar objeto NavMesh id={getattr(obj, 'id', 'unknown')}: {e}")

    def _calculate_edges(self) -> None:
        """
        Descripción
            MÉTODO: Calcula las conexiones (aristas) entre nodos adyacentes.

        Argumentos
            - Ninguno
        """
        # 1. Obtener lista de nodos y comparar pares para detectar bordes compartidos
        node_list = list(self.nodes.values())
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                node_a = node_list[i]
                node_b = node_list[j]

                # 2. Si comparten borde, añadir como vecinos mutuamente
                if self._polygons_share_border(node_a.polygon, node_b.polygon):
                    node_a.neighbors.append(node_b)
                    node_b.neighbors.append(node_a)

    def _polygons_share_border(self, poly1: list, poly2: list) -> bool:
        """
        Descripción
            FUNCIÓN: Determina si dos polígonos comparten un borde mediante la comparación de segmentos.

        Argumentos
            - poly1 (list) : Lista de vértices del primer polígono.
            - poly2 (list) : Lista de vértices del segundo polígono.

        Retorno
            - bool: True si comparten un borde con solapamiento significativo.
        """
        # 1. Iterar segmentos de ambos polígonos y verificar solapamiento colineal
        for i in range(len(poly1)):
            p1 = poly1[i]
            p2 = poly1[(i + 1) % len(poly1)]  # Segmento p1-p2

            for j in range(len(poly2)):
                p3 = poly2[j]
                p4 = poly2[(j + 1) % len(poly2)]  # Segmento p3-p4

                # 2. Si los segmentos son colineales y se solapan, retornar True
                if self._are_segments_collinear_and_overlapping(p1, p2, p3, p4):
                    return True
        # 3. No se detectó borde compartido
        return False

    def _are_segments_collinear_and_overlapping(self, p1: tuple, p2: tuple, p3: tuple, p4: tuple) -> bool:
        """
        Descripción
            FUNCIÓN: Verifica si dos segmentos son colineales y si su solapamiento es mayor que un punto.

        Argumentos
            - p1 (tuple) : Inicio del primer segmento (x, y).
            - p2 (tuple) : Fin del primer segmento (x, y).
            - p3 (tuple) : Inicio del segundo segmento (x, y).
            - p4 (tuple) : Fin del segundo segmento (x, y).

        Retorno
            - bool: True si son colineales y su solapamiento es mayor que la tolerancia.
        """
        # 1. Tolerancia para comparaciones de punto flotante
        epsilon = CONF.ALG.EPS

        # 2. Calcular vectores basales
        vec1 = (p2[0] - p1[0], p2[1] - p1[1])
        vec2 = (p3[0] - p1[0], p3[1] - p1[1])
        vec3 = (p4[0] - p1[0], p4[1] - p1[1])

        # 3. Producto cruzado para comprobar colinealidad
        cross_product1 = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        cross_product2 = vec1[0] * vec3[1] - vec1[1] * vec3[0]

        # 4. Si cualquiera excede la tolerancia, no son colineales
        if abs(cross_product1) > epsilon or abs(cross_product2) > epsilon:
            return False

        # 5. Proyectar segmentos sobre el eje dominante (X o Y) para medir solapamiento
        dot_p1 = p1[0]
        dot_p2 = p2[0]
        dot_p3 = p3[0]
        dot_p4 = p4[0]

        # 6. Si el segmento es principalmente vertical, usar Y para proyección
        if abs(vec1[0]) < epsilon:
            dot_p1 = p1[1]
            dot_p2 = p2[1]
            dot_p3 = p3[1]
            dot_p4 = p4[1]

        # 7. Calcular intervalo de solapamiento
        overlap_start = max(min(dot_p1, dot_p2), min(dot_p3, dot_p4))
        overlap_end = min(max(dot_p1, dot_p2), max(dot_p3, dot_p4))

        # 8. Retornar True si la longitud del solapamiento supera la tolerancia
        return (overlap_end - overlap_start) > epsilon

    def draw(self, surface: pygame.Surface, camera_x: float, camera_z: float) -> None:
        """
        Descripción
            MÉTODO: Dibuja el NavMesh (polígonos, centros y conexiones) en la superficie indicada.

        Argumentos
            - surface (pygame.Surface) : Superficie destino donde dibujar.
            - camera_x (float) : Coordenada X de la cámara.
            - camera_z (float) : Coordenada Z de la cámara.

        Retorno
            - Ninguno
        """
        # 1. Iterar nodos y dibujar polígonos ajustados a la cámara
        for node in self.nodes.values():
            points_on_camera = [(p[0] - camera_x, p[1] - camera_z) for p in node.polygon]

            # 2. Dibujar borde del polígono
            pygame.draw.polygon(surface, (255, 255, 0), points_on_camera, 2)

            # 3. Dibujar conexiones hacia vecinos desde el centro
            center_on_camera = (node.center[0] - camera_x, node.center[1] - camera_z)
            for neighbor in node.neighbors:
                neighbor_center_on_camera = (neighbor.center[0] - camera_x, neighbor.center[1] - camera_z)
                pygame.draw.line(surface, (39, 245, 242), center_on_camera, neighbor_center_on_camera, 2)

            # 4. Dibujar el centro del nodo
            pygame.draw.circle(surface, (255, 0, 0), (int(center_on_camera[0]), int(center_on_camera[1])), 4)