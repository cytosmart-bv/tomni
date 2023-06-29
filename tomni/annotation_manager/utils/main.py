from typing import List

import numpy as np

from tomni.annotation_manager.annotations.point import Point


def parse_points_to_contour(points: List[Point]) -> np.ndarray:
    contour_points = [[[point.x, point.y]] for point in points]
    contour = np.array(contour_points, dtype=np.int32)
    return contour
