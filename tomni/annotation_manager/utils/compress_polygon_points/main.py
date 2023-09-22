from simplification.cutil import simplify_coords
from typing import List
from tomni.annotation_manager.annotations.point import Point


def compress_polygon_points(
    points: List[Point], epsilon: float = 3.0, min_number_of_points: int = 5
):
    """Compresses the polygon

    Args:
        points (List): The points of the polygon
        epsilon (float, optional): Epsilon value in Ramer-Douglas-Peucker algorithm. The smaller the epsilon, the more points are kept and the more faithful the simplified curve is to the original one.
        Defaults to 3.0.

    Returns:
        _type_: A list of 2D points, each represented as an instance of the `Point` class.
    """
    assert epsilon >= 0

    point_arr = [[point.x, point.y] for point in points]
    point_arr_compressed = simplify_coords(point_arr, epsilon)
    if len(point_arr_compressed) < min_number_of_points:
        return points
    return [Point(x, y) for (x, y) in point_arr_compressed]
