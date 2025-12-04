import math
import heapq
from typing import List, Tuple, Optional
from map.navmesh import NavMesh
from tacticals.tactical_profile import TacticalProfile

class TacticalPathfinder:
    """
    Descripción
        CLASE: Pathfinder táctico que implementa A* sobre el NavMesh considerando perfiles tácticos.
        Modifica el costo de recorrido (g_score) sumando penalizaciones o bonificaciones
        según el tipo táctico del nodo destino.

    Atributos
        - navmesh (NavMesh): referencia al NavMesh utilizado para búsquedas.

    Métodos y Funciones
        - find_path: Calcula la ruta óptima considerando distancia y pesos tácticos.
        - _dist: Calcula distancia euclidiana.
    """
    def __init__(self, navmesh: NavMesh):
        # Inicializar referencia al NavMesh
        self.navmesh = navmesh

    def _dist(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """
        Descripción
            FUNCIÓN: Calcula la distancia euclidiana entre dos puntos.
        """
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def find_path(self, start_pos: Tuple[float, float], end_pos: Tuple[float, float], profile: TacticalProfile) -> Optional[List[Tuple[float, float]]]:
        """
        Descripción
            MÉTODO: Encuentra una ruta táctica entre dos puntos usando A* ponderado.

        Argumentos
            - start_pos (Tuple[float,float]): Inicio en world-space.
            - end_pos (Tuple[float,float]): Destino en world-space.
            - profile (TacticalProfile): Perfil con los pesos tácticos a aplicar.

        Retorno
            - Optional[List[Tuple[float, float]]]: Lista de puntos de la ruta o None.
        """
        # 1. Obtener nodos de inicio y fin
        start_node = self.navmesh.get_node_at(start_pos)
        end_node = self.navmesh.get_node_at(end_pos)

        if start_node is None or end_node is None:
            return None

        # 2. Inicializar estructuras A*
        open_heap = []
        came_from = {}
        g_score = {start_node.id: 0.0}
        
        # Heurística inicial (distancia directa)
        h_start = self._dist(start_node.center, end_node.center)
        f_score = {start_node.id: h_start}

        heapq.heappush(open_heap, (f_score[start_node.id], start_node.id, start_node))
        closed = set()

        # 3. Bucle principal A*
        while open_heap:
            _, _, current = heapq.heappop(open_heap)

            if current.id in closed:
                continue
            
            # 3.1 Reconstruir camino si llegamos al destino
            if current is end_node:
                path_nodes = []
                node = current
                while node.id in came_from:
                    path_nodes.append(node)
                    node = came_from[node.id]
                path_nodes.append(start_node)
                path_nodes.reverse()

                # Convertir nodos a puntos (centroids)
                points = []
                for n in path_nodes:
                    points.append(n.center)
                points.append(end_pos)
                return points

            closed.add(current.id)

            # 3.2 Expandir vecinos
            for nb in current.neighbors:
                if nb.id in closed:
                    continue

                # --- CÁLCULO DE COSTO TÁCTICO ---
                # Costo base: Distancia geométrica
                dist_cost = self._dist(current.center, nb.center)
                
                # Costo táctico: Peso del nodo destino según perfil
                # Si el nodo tiene tipo 'narrow', 'cover', etc., obtenemos su peso.
                tactical_weight = 0.0
                if nb.tactical_type:
                    tactical_weight = profile.get_weight(nb.tactical_type)

                # Costo total del segmento (Clamp a 1.0 para evitar costos negativos/cero)
                # Fórmula: C = D + w
                segment_cost = max(1.0, dist_cost + tactical_weight)
                # --------------------------------

                tentative_g = g_score.get(current.id, math.inf) + segment_cost

                if tentative_g < g_score.get(nb.id, math.inf):
                    came_from[nb.id] = current
                    g_score[nb.id] = tentative_g
                    
                    # Heurística: Distancia restante estimada
                    h = self._dist(nb.center, end_node.center)
                    f = tentative_g + h
                    
                    f_score[nb.id] = f
                    heapq.heappush(open_heap, (f, nb.id, nb))

        return None