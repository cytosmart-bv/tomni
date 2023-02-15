from typing import List

import numpy as np
from rdp import rdp

from ..annotations import Point


def parse_points_to_contour(points: List[Point]) -> np.ndarray:
    contour_points = [[[point.x, point.y]] for point in points]
    contour = np.array(contour_points, dtype=np.int32)
    return contour


def compress_polygon_points(
    points: List[Point],
    n_points_limit: int = 100,
    n_iter: int = 3,
    epsilon: float = 0.9,
    do_rdp_compresion: bool = False,
) -> List[Point]:
    if len(points) > n_points_limit:
        return recursive_compression(points, n_iter)
    elif len(points) <= n_points_limit and do_rdp_compresion:
        return rdp_compression(points, epsilon)
    else:
        return points


def recursive_compression(points: List[Point], n_iter: int) -> List[Point]:
    assert n_iter > 0, "Nr of iterations must be positive."

    for _ in range(n_iter):
        points = points[::2]

    return points


def rdp_compression(points: List[Point], epsilon: float) -> List[Point]:
    assert 0 <= epsilon <= 1, "Epsilon must be in [0, 1]."

    point_arr = [[point.x, point.y] for point in points]
    point_arr_compressed = rdp(point_arr, epsilon=epsilon)
    return [Point(x, y) for (x, y) in point_arr_compressed]
