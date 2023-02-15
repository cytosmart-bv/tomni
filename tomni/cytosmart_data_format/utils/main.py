from typing import List

import numpy as np
from rdp import rdp

from ..annotations import Point


def parse_points_to_contour(points: List[Point]) -> np.ndarray:
    """
    Converts a list of 2D points to a numpy array that can be used as input to OpenCV functions.

    Args:
        points: A list of 2D points, each represented as an instance of the `Point` class.

    Returns:
        A numpy array of shape (n, 1, 2), where n is the number of points in the input list.
        The array is of data type int32 and contains the x and y coordinates of each point in the input list.
    """
    contour_points = [[[point.x, point.y]] for point in points]
    contour = np.array(contour_points, dtype=np.int32)
    return contour


def compress_polygon_points(
    points: List[Point],
    n_points_theshold: int = 100,
    n_iter: int = 3,
    epsilon: float = 0.9,
    do_rdp_compresion: bool = False,
) -> List[Point]:
    """
    Compresses a list of 2D points representing a polygon by reducing the number of points using either a recursive
    method or the Ramer-Douglas-Peucker (RDP) algorithm.

    Args:
        points: A list of 2D points, each represented as an instance of the `Point` class.
        n_points_theshold: An integer representing the maximum number of points in selects the recursive method .
        n_iter: An integer representing the number of times to apply the recursive compression method.
        epsilon: A float representing the error tolerance for the RDP algorithm.
        do_rdp_compresion: A boolean flag indicating whether to use the RDP algorithm for compression.

    Returns:
        A list of 2D points, each represented as an instance of the `Point` class. The points are compressed using either the recursive
        method, the RDP algorithm or none, based on the value of `do_rdp_compresion`.
    """
    if len(points) > n_points_theshold:
        return recursive_compression(points, n_iter)
    elif len(points) <= n_points_theshold and do_rdp_compresion:
        return rdp_compression(points, epsilon)
    else:
        return points


def recursive_compression(points: List[Point], n_iter: int) -> List[Point]:
    """
    Compresses a list of 2D points by reducing the number of points by half iteratively.

    Args:
        points: A list of 2D points, each represented as an instance of the `Point` class.
        n_iter: An integer representing the number of times to apply the recursive compression method.

    Returns:
        A list of 2D points, each represented as an instance of the `Point` class. The number of points in the output
        list is half the number of points in the input list, repeated `n_iter` times.
    """
    assert n_iter > 0, "Nr of iterations must be positive."

    for _ in range(n_iter):
        points = points[::2]

    return points


def rdp_compression(points: List[Point], epsilon: float) -> List[Point]:
    """
    Compresses a list of 2D points using the Ramer-Douglas-Peucker (RDP) algorithm for line simplification.

    Args:
        points: A list of 2D points, each represented as an instance of the `Point` class.
        epsilon: A float representing the error tolerance for the RDP algorithm.

    Returns:
        A list of 2D points, each represented as an instance of the `Point` class. The points are compressed using the
        RDP algorithm with the specified error tolerance.
    """
    assert 0 <= epsilon <= 1, "Epsilon must be in [0, 1]."

    point_arr = [[point.x, point.y] for point in points]
    point_arr_compressed = rdp(point_arr, epsilon=epsilon)
    return [Point(x, y) for (x, y) in point_arr_compressed]
