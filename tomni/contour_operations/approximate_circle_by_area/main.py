from math import pi, sqrt
from typing import Tuple

import cv2
import numpy as np

from .. import get_center


def approximate_circle_by_area(contour: np.ndarray) -> Tuple[float, float, float]:
    """
    Approximate a circle with the same area and center as the given contour.

    Args:
        contour (np.ndarray): An OpenCV contour of a single object.

    Returns:
        Tuple[float, float, float]: A tuple containing the following values:
            - x (float): Center x position of the approximate circle.
            - y (float): Center y position of the approximate circle.
            - radius (float): Radius of the approximate circle.

    Example::

        contour = np.array([[[1, 2]], [[2, 3]], [[3, 2]], [[2, 1]]])
        center_x, center_y, circle_radius = approximate_circle_by_area(contour)
        (2.0, 2.0, 1.0)
    """
    x, y = get_center(contour)
    area = cv2.contourArea(contour)
    radius = sqrt(area / pi)
    return x, y, radius
