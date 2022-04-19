from typing import Tuple

import cv2
import numpy as np


def roundness(contour: np.ndarray) -> float:
    """
    Returns roundess of the contour
    Roundness is determined by difference in areas of the contour and enclosing circle


    Args:
        contour (np.ndarray): An opencv contour of a single object

    Returns:
        float: roundess number between 0 and 1
    """

    area = cv2.contourArea(contour)
    _, radius = cv2.minEnclosingCircle(contour)
    enclosing_circle_area = radius**2 * np.pi
    roundness = area / enclosing_circle_area
    return roundness
