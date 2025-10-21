"""
Path utilities: Path base + PolylinePath and CirclePath implementations.

Interfaz esperada por los behaviours:
- get_param(position: tuple[float, float], last_param: float) -> float
  Devuelve un "param" que codifica el segmento y la posición local sobre el segmento:
    param = segment_index + t  (t en [0,1])
  El uso de `last_param` permite búsqueda local para mejorar rendimiento.
- get_position(param: float) -> tuple[float, float]
  Devuelve la posición (x, z) correspondiente al param.

Además se ofrecen funciones de fábrica:
- make_rectangle_path(width, height, center=(0,0), closed=True)
- make_circle_path(radius, segments=32, center=(0,0))

Notas
- Coordenadas: usamos (x, z) como tuplas de floats para mantener coherencia con el repo.
- Para PolylinePath el path se considera cerrado si closed=True; el índice de segmento hace wrap automáticamente.
- get_param busca primero alrededor del segmento sugerido por last_param (ventana configurable) y, si no
  encuentra un candidato razonable, hace búsqueda completa.
"""
from __future__ import annotations
import math
import pygame
from typing import List, Tuple

Vector2 = Tuple[float, float]


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
    """Interfaz base."""

    def get_param(self, position: Vector2, last_param: float) -> float:
        raise NotImplementedError

    def get_position(self, param: float) -> Vector2:
        raise NotImplementedError


class PolylinePath(Path):
    """
    Path representado por una lista de puntos (vertices).
    Parametrización: param = segment_index + t, t in [0,1].
    Si closed=True el path hace wrap entre último y primer punto.
    """

    def __init__(self, points: List[Vector2], closed: bool = True, search_window: int = 4) -> None:
        if len(points) < 2:
            raise ValueError("PolylinePath requiere al menos 2 puntos.")
        self.points = points[:]  # copiar
        self.closed = bool(closed)
        self.segment_count = len(points) if closed else len(points) - 1
        self.search_window = max(1, int(search_window))

    def _segment_point(self, idx: int) -> Tuple[Vector2, Vector2]:
        a = self.points[idx]
        b = self.points[(idx + 1) % len(self.points)]
        return a, b

    def get_param(self, position: Vector2, last_param: float) -> float:
        """
        Busca el punto más cercano en la ruta y devuelve param = seg_idx + t.
        Optimización: comienza la búsqueda en torno a last_param (ventana self.search_window).
        """
        px, pz = position
        # clamp last segment index
        last_seg = int(math.floor(last_param)) if last_param is not None else 0
        last_seg = last_seg % (self.segment_count if self.segment_count > 0 else 1)

        best_dist2 = float("inf")
        best_param = float(last_seg)

        # window search
        segs = []
        for d in range(-self.search_window, self.search_window + 1):
            seg_idx = (last_seg + d) % self.segment_count if self.closed else (last_seg + d)
            if seg_idx < 0 or seg_idx >= self.segment_count:
                continue
            segs.append(seg_idx)

        # evaluate candidates in window
        for seg_idx in segs:
            a, b = self._segment_point(seg_idx)
            ab = _sub(b, a)
            ap = _sub((px, pz), a)
            ab_len2 = _dot(ab, ab)
            if ab_len2 == 0:
                t = 0.0
            else:
                t = _dot(ap, ab) / ab_len2
                if t < 0.0:
                    t = 0.0
                elif t > 1.0:
                    t = 1.0
            proj = _add(a, _mul(ab, t))
            d2 = _dist2(proj, (px, pz))
            if d2 < best_dist2:
                best_dist2 = d2
                best_param = seg_idx + t

        # if window search didn't find a good candidate (should be rare), fallback to global search
        # Heurística: si best_dist2 is huge, do full search
        if best_dist2 > 1e6:
            for seg_idx in range(self.segment_count):
                a, b = self._segment_point(seg_idx)
                ab = _sub(b, a)
                ap = _sub((px, pz), a)
                ab_len2 = _dot(ab, ab)
                if ab_len2 == 0:
                    t = 0.0
                else:
                    t = _dot(ap, ab) / ab_len2
                    t = max(0.0, min(1.0, t))
                proj = _add(a, _mul(ab, t))
                d2 = _dist2(proj, (px, pz))
                if d2 < best_dist2:
                    best_dist2 = d2
                    best_param = seg_idx + t

        # normalize param into range [0, segment_count)
        # If closed, allow wrap; if open clamp to [0, segment_count)
        if self.closed:
            # param can be larger than segment_count; bring to base cycle
            base = math.floor(best_param)
            frac = best_param - base
            best_param = (base % self.segment_count) + frac
        else:
            best_param = max(0.0, min(float(self.segment_count - 1) + 1.0 - 1e-6, best_param))

        return float(best_param)

    def get_position(self, param: float) -> Vector2:
        """
        Convierte param a posición. param = seg_idx + t.
        Si closed, el segmento index hace wrap.
        """
        if self.segment_count == 0:
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

    def draw(self, surface, camera_x: float = 0.0, camera_z: float = 0.0, color: Tuple[int,int,int] = (255, 255, 0), width: int = 2, draw_nodes: bool = True):
        """
        Dibuja el path en pantalla para debugging.
        - surface: pygame.Surface donde dibujar.
        - camera_x, camera_z: offsets de cámara (mundo -> pantalla).
        - color: color (por defecto amarillo).
        - width: grosor de líneas.
        - draw_nodes: si True dibuja los vértices como pequeños círculos.
        """
        if pygame is None:
            return

        if not self.points:
            return

        pts = [ (int(p[0] - camera_x), int(p[1] - camera_z)) for p in self.points ]

        # dibujar segmentos
        for i in range(len(pts) - 1):
            pygame.draw.line(surface, color, pts[i], pts[i+1], width)

        if self.closed and len(pts) > 1:
            pygame.draw.line(surface, color, pts[-1], pts[0], width)

        if draw_nodes:
            node_color = (0, 0, 0)
            for p in pts:
                pygame.draw.circle(surface, node_color, p, max(4, width))

# Factory helpers

def make_rectangle_path(width: float, height: float, center: Vector2 = (0.0, 0.0), segments: int = 48) -> PolylinePath:
    """
    Crea un path rectangular centrado en `center` aproximando el perímetro con 'segments' vértices.
    'segments' es el número total de vértices a distribuir a lo largo del perímetro.
    Se garantiza al menos 4 vértices (uno por esquina). Los vértices se distribuyen
    proporcionalmente a la longitud de cada lado para evitar concentraciones.
    """
    cx, cz = center
    w = float(width)
    h = float(height)
    perim = 2.0 * (w + h)

    segs = max(4, int(segments))

    # longitudes de los 4 lados (clockwise): bottom, right, top, left
    side_lengths = [w, h, w, h]

    # asignar un número inicial de vértices por lado proporcionalmente (al menos 1)
    side_counts: list[int] = []
    remaining = segs
    for L in side_lengths:
        count = max(1, int(round((L / perim) * segs)))
        side_counts.append(count)
        remaining -= count

    # distribuir el resto de vértices empezando por los lados más largos
    if remaining > 0:
        idxs = sorted(range(4), key=lambda i: -side_lengths[i])
        i = 0
        while remaining > 0:
            side_counts[idxs[i % 4]] += 1
            remaining -= 1
            i += 1

    # construir puntos a lo largo de cada lado. Para cada lado generamos 'count' puntos
    # con t en [0, 1) -> evitamos duplicar la esquina final del último segmento
    hw = w / 2.0
    hh = h / 2.0
    corners = [
        (cx - hw, cz - hh),  # bottom-left
        (cx + hw, cz - hh),  # bottom-right
        (cx + hw, cz + hh),  # top-right
        (cx - hw, cz + hh),  # top-left
    ]

    points: List[Vector2] = []
    for side in range(4):
        a = corners[side]
        b = corners[(side + 1) % 4]
        count = max(1, side_counts[side])
        for k in range(count):
            t = k / float(count)  # t in [0, 1)
            pt = _lerp(a, b, t)
            points.append(pt)

    return PolylinePath(points, closed=True)


def make_circle_path(radius: float, center: Vector2 = (0.0, 0.0), segments: int = 48) -> PolylinePath:
    """
    Crea un PolylinePath que aproxima una circunferencia usando 'segments' vértices.
    Esto permite compatibilidad con PolylinePath get_param/search optimizado.
    """
    segs = max(8, int(segments))
    pts: List[Vector2] = []
    for i in range(segs):
        theta = (i / segs) * 2.0 * math.pi
        x = center[0] + math.cos(theta) * radius
        z = center[1] + math.sin(theta) * radius
        pts.append((x, z))
    return PolylinePath(pts, closed=True)