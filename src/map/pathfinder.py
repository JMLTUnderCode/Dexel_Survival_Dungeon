import math
import heapq
from typing import List, Tuple, Optional

from map.navmesh import NavMesh, NavMeshNode

class Pathfinder:
    """
    Descripción
        CLASE: Pathfinder que implementa A* sobre el NavMesh.

    Atributos
        - navmesh (NavMesh): referencia al NavMesh utilizado para búsquedas.

    Métodos y Funciones
        - find_node_path: Ejecuta A* entre dos nodos.
        - find_path: Resuelve nodos contenedores y devuelve lista de puntos world-space.

    Propósito
        - Proveer una interfaz simple para que sistemas de IA o enemigos calculen rutas
          desde una posición a otra usando la malla de navegación.
    """
    def __init__(self, navmesh: NavMesh):
        # Inicializar referencia al NavMesh
        self.navmesh = navmesh

    def _dist(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """
        Descripción
            FUNCIÓN: Calcula la distancia euclidiana entre dos puntos (x, z).

        Argumentos
            - a (Tuple[float,float]) : Punto A (x, z).
            - b (Tuple[float,float]) : Punto B (x, z).

        Retorno
            - float: distancia euclidiana entre A y B.
        """
        # 1. Calcular e retornar la distancia euclidiana
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def find_node_path(self, start_node: NavMeshNode, end_node: NavMeshNode) -> Optional[List[NavMeshNode]]:
        """
        Descripción
            MÉTODO: Ejecuta A* entre `start_node` y `end_node` en el grafo de NavMesh.

        Argumentos
            - start_node (NavMeshNode): nodo inicial.
            - end_node (NavMeshNode): nodo objetivo.

        Retorno
            - Optional[List[NavMeshNode]]: lista ordenada de nodos [start,...,end] si existe camino,
              o None si no existe o si alguno de los nodos es None.
        """
        # 1. Validaciones iniciales
        if start_node is None or end_node is None:
            return None

        # 2. Caso trivial: mismo nodo
        if start_node == end_node:
            return [start_node]

        # 3. Inicializar estructuras A* (open heap, mapas de costes y predecessor)
        open_heap = []  # heap de (f_score, node.id, node_obj)
        came_from = {}  # mapa node.id -> predecessor node_obj
        g_score = {start_node.id: 0.0}
        f_score = {start_node.id: self._dist(start_node.center, end_node.center)}

        # 4. Insertar nodo inicial en el heap
        heapq.heappush(open_heap, (f_score[start_node.id], start_node.id, start_node))

        # 5. Conjunto de nodos ya expandidos
        closed = set()

        # 6. Loop principal de A*
        while open_heap:
            # 6.1 Extraer el nodo con menor f_score
            _, _, current = heapq.heappop(open_heap)

            # 6.2 Ignorar entradas obsoletas ya cerradas
            if current.id in closed:
                continue

            # 6.3 Si alcanzamos el objetivo, reconstruir el camino
            if current is end_node:
                path: List[NavMeshNode] = []
                node = current
                while node.id in came_from:
                    path.append(node)
                    node = came_from[node.id]
                path.append(start_node)
                path.reverse()
                return path

            # 6.4 Marcar nodo como expandido
            closed.add(current.id)

            # 6.5 Expandir vecinos del nodo actual
            for nb in current.neighbors:
                # 6.5.1 Ignorar vecinos ya cerrados
                if nb.id in closed:
                    continue

                # 6.5.2 Calcular coste tentativa desde start hasta el vecino vía current
                tentative_g = g_score.get(current.id, math.inf) + self._dist(current.center, nb.center)

                # 6.5.3 Si la ruta tentativa es mejor, actualizar estructuras
                if tentative_g < g_score.get(nb.id, math.inf):
                    came_from[nb.id] = current
                    g_score[nb.id] = tentative_g
                    f = tentative_g + self._dist(nb.center, end_node.center)
                    heapq.heappush(open_heap, (f, nb.id, nb))
                    f_score[nb.id] = f

        # 7. No se encontró camino
        return None

    def find_path(self, start_pos: Tuple[float, float], end_pos: Tuple[float, float]) -> Optional[List[Tuple[float, float]]]:
        """
        Descripción
            MÉTODO: Resuelve los nodos que contienen `start_pos` y `end_pos` y ejecuta A* para obtener ruta.

        Argumentos
            - start_pos (Tuple[float,float]) : posición de inicio en world-space (x, z).
            - end_pos (Tuple[float,float]) : posición objetivo en world-space (x, z).

        Retorno
            - Optional[List[Tuple[float,float]]]: lista de puntos [start_pos, center(node1), ..., end_pos]
              si se pudo generar ruta; None si no es posible (p. ej. puntos fuera del NavMesh).
        """
        # 1. Localizar nodos contenedores para las posiciones dadas
        start_node = self.navmesh.get_node_at(start_pos)
        end_node = self.navmesh.get_node_at(end_pos)

        # 2. Si alguno no pertenece a la malla, no se puede generar ruta
        if start_node is None or end_node is None:
            return None

        # 3. Ejecutar A* sobre nodos
        node_path = self.find_node_path(start_node, end_node)
        if not node_path:
            return None

        # 4. Construir lista de puntos world-space (incluye start_pos y end_pos)
        points: List[Tuple[float, float]] = [start_pos]
        for n in node_path:
            points.append(n.center)
        points.append(end_pos)
        return points