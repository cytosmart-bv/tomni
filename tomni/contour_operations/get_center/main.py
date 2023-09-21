from typing import Tuple

import cv2
import numpy as np


def get_center(contour: np.ndarray) -> Tuple[int, int]:
    """
    Calculate the center coordinates of a contour.

    Args:
        contour (np.ndarray): An OpenCV contour of a single object.

    Returns:
        Tuple[int, int]: A tuple containing the x and y coordinates of the center.

    Example::

        contour = np.array([[[1, 2]], [[2, 3]], [[3, 2]], [[2, 1]]])
        get_center(contour)
        (2, 2)
    """
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return contour[0][0][0], contour[0][0][1]
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY
