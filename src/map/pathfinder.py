import math
import heapq
from typing import List, Tuple, Optional

from map.navmesh import NavMesh, NavMeshNode

class Pathfinder:
    """
    Servicio A* sobre NavMesh (nivel 0).

    - find_node_path(start_node, end_node) -> Optional[List[NavMeshNode]]
        Ejecuta A* entre dos nodos del NavMesh y devuelve la lista de nodos que forman el
        camino (incluyendo start_node y end_node). Retorna None si no existe camino.

    - find_path(start_pos, end_pos) -> Optional[List[Tuple[float, float]]]
        Localiza los nodos que contienen start_pos y end_pos usando
        [`NavMesh.get_node_at`](src/map/navmesh.py) y ejecuta `find_node_path`.
        Devuelve una lista de puntos en world-space: [start_pos, center(node1), ..., end_pos].
    """

    def __init__(self, navmesh: NavMesh):
        """
        Inicializa el Pathfinder con una referencia al NavMesh.

        Args:
            navmesh: NavMesh ya procesado (nodos y vecinos calculados).
        """
        self.navmesh = navmesh

    def _dist(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """Distancia euclidiana entre dos puntos (x, z)."""
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def find_node_path(self, start_node: NavMeshNode, end_node: NavMeshNode) -> Optional[List[NavMeshNode]]:
        """
        Ejecuta A* entre `start_node` y `end_node`.

        Args:
            start_node: nodo inicial (NavMeshNode).
            end_node: nodo objetivo (NavMeshNode).

        Returns:
            Lista de NavMeshNode representando el camino en orden [start, ..., end]
            o None si no existe camino o si alguno de los nodos es None.
        """
        if start_node is None or end_node is None:
            return None

        if start_node == end_node:
            return [start_node]

        # Estructuras A*
        open_heap = []  # heap de (f_score, node.id, node_obj)
        came_from = {}  # mapa node.id -> predecessor node_obj
        g_score = {start_node.id: 0.0}
        f_score = {start_node.id: self._dist(start_node.center, end_node.center)}

        # Push start
        heapq.heappush(open_heap, (f_score[start_node.id], start_node.id, start_node))

        closed = set()  # nodos ya expandidos

        while open_heap:
            _, _, current = heapq.heappop(open_heap)

            # Skip stale entries (mismo nodo puede aparecer varias veces en heap)
            if current.id in closed:
                continue

            # Si alcanzamos el objetivo -> reconstruir camino
            if current is end_node:
                path: List[NavMeshNode] = []
                node = current
                while node.id in came_from:
                    path.append(node)
                    node = came_from[node.id]
                path.append(start_node)
                path.reverse()
                return path

            closed.add(current.id)

            # Expandir vecinos
            for nb in current.neighbors:
                if nb.id in closed:
                    continue

                # coste tentativa: g(current) + cost(current, nb)
                tentative_g = g_score.get(current.id, math.inf) + self._dist(current.center, nb.center)

                if tentative_g < g_score.get(nb.id, math.inf):
                    came_from[nb.id] = current
                    g_score[nb.id] = tentative_g
                    f = tentative_g + self._dist(nb.center, end_node.center)
                    # push en heap; si ya había entrada menos óptima, se ignorará al extraerla
                    heapq.heappush(open_heap, (f, nb.id, nb))
                    f_score[nb.id] = f

        # No se encontró camino
        return None

    def find_path(self, start_pos: Tuple[float, float], end_pos: Tuple[float, float]) -> Optional[List[Tuple[float, float]]]:
        """
        Localiza nodos que contienen start_pos y end_pos y ejecuta A*.

        Args:
            start_pos: posición world-space (x, z) de inicio.
            end_pos: posición world-space (x, z) objetivo.

        Returns:
            Lista de puntos world-space que describen la ruta:
            [start_pos, center(node1), center(node2), ..., end_pos]
            o None si no se puede generar ruta (por ejemplo si alguno de los puntos no está dentro
            de ningún nodo del NavMesh).
        """
        start_node = self.navmesh.get_node_at(start_pos)
        end_node = self.navmesh.get_node_at(end_pos)

        if start_node is None or end_node is None:
            # No hay nodo que contenga start o end -> fallo controlado
            return None

        node_path = self.find_node_path(start_node, end_node)
        if not node_path:
            return None

        points: List[Tuple[float, float]] = [start_pos]
        for n in node_path:
            points.append(n.center)
        points.append(end_pos)
        return points