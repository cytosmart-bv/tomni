from typing import Union, List

import numpy as np

from tomni.annotation_manager.annotations.point import Point


def parse_points_to_contour(points: List[Point]) -> np.ndarray:
    contour_points = [[[point.x, point.y]] for point in points]
    contour = np.array(contour_points, dtype=np.int32)
    return contour


def parse_points_to_inner_contour(
    list_points: Union[List[List[Point]], List]
) -> List[np.ndarray]:
    inner_contours = []
    for points in list_points:
        contour_points = [[[point.x, point.y]] for point in points]
        contour = np.array(contour_points, dtype=np.int32)
        inner_contours.append(contour)
    return inner_contours
