import cv2
import numpy as np


def circularity(contour: np.ndarray) -> float:
    """
    Calculate the circularity of a contour.

    The circularity of a contour is a measure of how closely it resembles a perfect circle.
    It is calculated based on the contour's area and perimeter.

    Args:
        contour (np.ndarray): The contour represented as an OpenCV ndarray.

    Returns:
        float: The circularity value, where 0 < circularity <= 1.

    Example:
        >>> contour = np.array([[[1, 2]], [[2, 3]], [[3, 2]], [[2, 1]]])
        >>> circularity(contour)
        0.7853981633974483  # Approximate circularity of a square.

    Note:
        - Formula: Circularity = (4 * π * area) / (perimeter^2)
        - Circularities close to 0 indicate more irregular shapes, while circularities close to 1 suggest shapes that closely resemble a perfect circle.
    """

    # calculate size
    area = cv2.contourArea(contour)

    # calculate shape
    perimeter = cv2.arcLength(contour, True)

    circularity = (4 * np.pi * area) / (perimeter**2)

    return circularity
