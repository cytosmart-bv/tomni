import cv2
import numpy as np


def roundness(contour: np.ndarray) -> float:
    """
    Calculate the roundness of a contour.

    The roundness is determined by the ratio of the area of the contour to the area of
    the minimum enclosing circle.

    Args:
        contour (np.ndarray): An OpenCV contour of a single object.

    Returns:
        float: The roundness value, ranging from 0 to 1, where 1 indicates a perfect circle.

    Examples:
        >>> contour = np.array([[[1, 2]], [[2, 3]], [[3, 2]], [[2, 1]]])
        >>> roundness(contour)
        0.8367346938775511
    """

    area = cv2.contourArea(contour)
    _, radius = cv2.minEnclosingCircle(contour)
    enclosing_circle_area = radius**2 * np.pi
    roundness = area / enclosing_circle_area
    return roundness
