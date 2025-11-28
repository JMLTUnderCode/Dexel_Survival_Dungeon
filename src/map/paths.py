"""
Módulo de utilidades para caminos polilínea usados por el comportamiento FollowPath.

Descripción
    Este archivo expone una implementación simple y única de Path basada en una
    lista de puntos (x,z). La clase Path ofrece dos operaciones principales:
      - get_param(position, last_param=None) -> float
          Devuelve un parámetro que identifica la posición más cercana sobre el camino
          en forma segment_index + t (t ∈ [0,1]).
      - get_position(param) -> (x,z)
          Convierte un parámetro en una posición 2D sobre el camino.

Convenciones
    - Código en inglés (nombres en snake_case), documentación y comentarios en español.
    - Path admite caminos cerrados (cíclicos) y abiertos.
    - Búsqueda local alrededor de last_param para rendimiento, con fallback a búsqueda completa.
"""
import math
import pygame
from typing import List, Tuple, Optional
from configs.package import CONF

Vector2 = Tuple[float, float]

# --------------------
# Helpers matemáticos (internos)
# --------------------
def _dot(a: Vector2, b: Vector2) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _sub(a: Vector2, b: Vector2) -> Vector2:
    return (a[0] - b[0], a[1] - b[1])


def _add(a: Vector2, b: Vector2) -> Vector2:
    return (a[0] + b[0], a[1] + b[1])


def _mul(a: Vector2, s: float) -> Vector2:
    return (a[0] * s, a[1] * s)


def _lerp(a: Vector2, b: Vector2, t: float) -> Vector2:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _dist2(a: Vector2, b: Vector2) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

class Path:
    """
    Descripción
        CLASE: Camino polilínea simple implementado sobre una lista de puntos (x,z).

    Atributos
        - points (List[Vector2]): lista de nodos del camino.
        - closed (bool): indica si el camino es cíclico (el último conecta con el primero).
        - segment_count (int): número de segmentos efectivos.
        - search_window (int): radio en segmentos para búsqueda local en get_param.

    Métodos principales
        - get_param(position, last_param=None): calcula param más cercano sobre el camino.
        - get_position(param): obtiene la posición 2D asociada a param.
        - draw(surface, camera_x, camera_z, ...): dibuja el camino para debug (si pygame está disponible).
    """
    def __init__(self, points: List[Vector2], closed: bool = True, search_window: int = 4) -> None:
        """
        Descripción
            MÉTODO: Inicializa el Path con la lista de puntos.

        Argumentos
            - points (List[Vector2]): lista de puntos (x,z), mínimo 2.
            - closed (bool): si True el camino es cíclico.
            - search_window (int): ventana de búsqueda local (en segmentos).
        """
        if len(points) < 2:
            raise ValueError("Path requires at least 2 points.")
        # copiar para evitar aliasing desde fuera
        self.points: List[Vector2] = points[:]
        self.closed: bool = bool(closed)
        self.segment_count: int = len(points) if self.closed else max(0, len(points) - 1)
        self.search_window: int = max(1, int(search_window))

    def _segment_point(self, idx: int) -> Tuple[Vector2, Vector2]:
        # devuelve los extremos (a,b) del segmento idx
        a = self.points[idx]
        b = self.points[(idx + 1) % len(self.points)]
        return a, b

    def get_param(self, position: Vector2, last_param: Optional[float] = None) -> float:
        """
        Descripción
            FUNCIÓN: Busca el punto sobre el camino más cercano a 'position' y devuelve
            su parametro como segment_index + t.

        Argumentos
            - position (Vector2): posición (x,z) de referencia.
            - last_param (Optional[float]): pista para búsqueda local (opcional).

        Retorno
            - float: parámetro que identifica la proyección sobre el camino.
        """
        px, pz = position

        # caso defensa: sin segmentos
        if self.segment_count <= 0:
            return 0.0

        # calcular segmento central para búsqueda local
        if last_param is None:
            center_seg = 0
        else:
            try:
                center_seg = int(math.floor(last_param)) % self.segment_count
            except Exception:
                center_seg = 0

        best_param = float(center_seg)
        best_d2 = float("inf")

        # construir lista de segmentos a evaluar (ventana local)
        segs = []
        for d in range(-self.search_window, self.search_window + 1):
            idx = center_seg + d
            if self.closed:
                idx = idx % self.segment_count
            if idx < 0 or idx >= self.segment_count:
                continue
            segs.append(idx)

        # evaluar ventana local
        for seg_idx in segs:
            a, b = self._segment_point(seg_idx)
            ab = _sub(b, a)
            ap = _sub((px, pz), a)
            ab_len2 = _dot(ab, ab)
            if ab_len2 == 0.0:
                t = 0.0
            else:
                t = _dot(ap, ab) / ab_len2
                t = max(0.0, min(1.0, t))
            proj = _add(a, _mul(ab, t))
            d2 = _dist2(proj, (px, pz))
            if d2 < best_d2:
                best_d2 = d2
                best_param = seg_idx + t

        # fallback: si la búsqueda local no fue efectiva (entidad muy lejos), evaluar todos los segmentos
        if best_d2 == float("inf"):
            for seg_idx in range(self.segment_count):
                a, b = self._segment_point(seg_idx)
                ab = _sub(b, a)
                ap = _sub((px, pz), a)
                ab_len2 = _dot(ab, ab)
                if ab_len2 == 0.0:
                    t = 0.0
                else:
                    t = _dot(ap, ab) / ab_len2
                    t = max(0.0, min(1.0, t))
                proj = _add(a, _mul(ab, t))
                d2 = _dist2(proj, (px, pz))
                if d2 < best_d2:
                    best_d2 = d2
                    best_param = seg_idx + t

        # normalizar y recortar param según si está cerrado o abierto
        if self.closed:
            base = math.floor(best_param)
            frac = best_param - base
            best_param = (base % self.segment_count) + frac
        else:
            max_param = float(self.segment_count - 1) + 1.0 - CONF.ALG.EPS
            best_param = max(0.0, min(max_param, best_param))

        return float(best_param)

    def get_position(self, param: float) -> Vector2:
        """
        Descripción
            FUNCIÓN: Convierte un parámetro (segment_index + t) a una posición (x,z) sobre el camino.

        Argumentos
            - param (float): parámetro a convertir.

        Retorno
            - Vector2: posición (x,z) correspondiente.
        """
        if self.segment_count <= 0:
            return self.points[0]
        seg_idx = int(math.floor(param))
        t = param - seg_idx
        if self.closed:
            seg_idx = seg_idx % self.segment_count
        else:
            seg_idx = max(0, min(self.segment_count - 1, seg_idx))
            t = max(0.0, min(1.0, t))
        a, b = self._segment_point(seg_idx)
        return _lerp(a, b, t)

    def draw(self, surface, camera_x: float = 0.0, camera_z: float = 0.0, color=(255, 255, 0), width: int = 2, draw_nodes: bool = True):
        """
        Descripción
            MÉTODO: Dibuja el camino en pantalla para depuración. No falla si pygame no está presente.

        Argumentos
            - surface: superficie pygame donde dibujar.
            - camera_x (float), camera_z (float): desplazamiento de cámara.
            - color (tuple), width (int), draw_nodes (bool): parámetros visuales.
        """
        if pygame is None:
            return
        if not self.points:
            return
        pts = [(int(p[0] - camera_x), int(p[1] - camera_z)) for p in self.points]
        for i in range(len(pts) - 1):
            pygame.draw.line(surface, color, pts[i], pts[i + 1], width)
        if self.closed and len(pts) > 1:
            pygame.draw.line(surface, color, pts[-1], pts[0], width)
        if draw_nodes:
            node_color = (0, 0, 0)
            for p in pts:
                pygame.draw.circle(surface, node_color, p, max(3, width))


# --------------------
# Helpers de fábrica
# --------------------
def make_rectangle_path(width: float, height: float, center: Vector2 = (0.0, 0.0), segments: int = 48) -> Path:
    """
    Descripción
        FUNCIÓN: Crea un Path rectangular centrado en 'center'.
    """
    cx, cz = center
    w = float(width)
    h = float(height)
    segs = max(4, int(segments))
    perim = 2.0 * (w + h)
    side_lengths = [w, h, w, h]
    side_counts = [max(1, int(round((L / perim) * segs))) for L in side_lengths]
    remaining = segs - sum(side_counts)
    idxs = sorted(range(4), key=lambda i: -side_lengths[i])
    i = 0
    while remaining > 0:
        side_counts[idxs[i % 4]] += 1
        remaining -= 1
        i += 1
    hw = w / 2.0
    hh = h / 2.0
    corners = [
        (cx - hw, cz - hh),
        (cx + hw, cz - hh),
        (cx + hw, cz + hh),
        (cx - hw, cz + hh),
    ]
    points: List[Vector2] = []
    for side in range(4):
        a = corners[side]
        b = corners[(side + 1) % 4]
        count = max(1, side_counts[side])
        for k in range(count):
            t = k / float(count)
            points.append(_lerp(a, b, t))
    return Path(points, closed=True)


def make_circle_path(radius: float, center: Vector2 = (0.0, 0.0), segments: int = 48) -> Path:
    """
    Descripción
        FUNCIÓN: Crea un Path que aproxima una circunferencia.
    """
    segs = max(8, int(segments))
    pts: List[Vector2] = []
    for i in range(segs):
        theta = (i / segs) * 2.0 * math.pi
        x = center[0] + math.cos(theta) * radius
        z = center[1] + math.sin(theta) * radius
        pts.append((x, z))
    return Path(pts, closed=True)

class PathInstance:
    """
    DOCUMENTACIÓN: PATH INSTANCE

    Resumen
        Instancia de un camino (Path) para entidades que lo siguen.

    Atributos
        - path (Path): el camino asociado.
        - offset (float): desplazamiento inicial a lo largo del camino.
        - curr_param (float): parámetro actual sobre el camino.

    """
    def __init__(self, path: Path, offset: float = 1.0, curr_param: float = 0.0) -> None:
        self.path = path
        self.offset = offset
        self.curr_param = curr_param