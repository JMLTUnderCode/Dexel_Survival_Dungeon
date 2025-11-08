import math
import heapq
from typing import List, Tuple, Optional

from map.navmesh import NavMesh, NavMeshNode

class Pathfinder:
    """
    Servicio A* sobre NavMesh (nivel 0).
    Interfaz pública:
      - find_node_path(start_node, end_node) -> Optional[List[NavMeshNode]]
      - find_path(start_pos, end_pos) -> Optional[List[Tuple[float,float]]]  (lista de puntos world-space)
    """
    def __init__(self, navmesh: NavMesh):
        self.navmesh = navmesh

    def _dist(self, a: Tuple[float,float], b: Tuple[float,float]) -> float:
        return math.hypot(a[0]-b[0], a[1]-b[1])

    def find_node_path(self, start_node: NavMeshNode, end_node: NavMeshNode) -> Optional[List[NavMeshNode]]:
        if start_node is None or end_node is None:
            return None
        if start_node == end_node:
            return [start_node]

        # A* over nodes, cost = euclidean between centers, heuristic = euclidean to goal center
        open_heap = []
        came_from = {}
        g_score = {start_node.id: 0.0}
        f_score = {start_node.id: self._dist(start_node.center, end_node.center)}

        heapq.heappush(open_heap, (f_score[start_node.id], start_node.id, start_node))

        closed = set()

        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            if current.id in closed:
                continue
            if current is end_node:
                # reconstruct path
                path = []
                node = current
                while node.id in came_from:
                    path.append(node)
                    node = came_from[node.id]
                path.append(start_node)
                path.reverse()
                return path

            closed.add(current.id)

            for nb in current.neighbors:
                if nb.id in closed:
                    continue
                tentative_g = g_score.get(current.id, math.inf) + self._dist(current.center, nb.center)
                if tentative_g < g_score.get(nb.id, math.inf):
                    came_from[nb.id] = current
                    g_score[nb.id] = tentative_g
                    f = tentative_g + self._dist(nb.center, end_node.center)
                    f_score[nb.id] = f
                    heapq.heappush(open_heap, (f, nb.id, nb))

        return None

    def find_path(self, start_pos: Tuple[float,float], end_pos: Tuple[float,float]) -> Optional[List[Tuple[float,float]]]:
        """
        Devuelve una lista de puntos world-space: [start_pos, center(node1), ..., end_pos]
        """
        start_node = self.navmesh.get_node_at(start_pos)
        end_node = self.navmesh.get_node_at(end_pos)

        if start_node is None or end_node is None:
            return None

        node_path = self.find_node_path(start_node, end_node)
        if not node_path:
            return None

        points: List[Tuple[float,float]] = [start_pos]
        for n in node_path:
            points.append(n.center)
        points.append(end_pos)
        return points