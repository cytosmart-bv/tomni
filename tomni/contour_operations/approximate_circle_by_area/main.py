from math import pi, sqrt
from typing import Tuple

import cv2
import numpy as np

from .. import get_center


def approximate_circle_by_area(contour: np.ndarray) -> Tuple[float, float, float]:
    """
    Returns a circle with the same area and center as the contour.

    Args:
        contour (np.ndarray): An opencv contour of a single object

    Returns:
        x: (float) Center x postion
        y: (float) Center y postion
        radius: (float) Radius of the circle
    """
    x, y = get_center(contour)
    area = cv2.contourArea(contour)
    radius = sqrt(area / pi)
    return x, y, radius
