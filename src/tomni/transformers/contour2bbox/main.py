import cv2
import numpy as np


def contour2bbox(contour: np.ndarray) -> tuple:
    """
    Convert OpenCV contours into a bounding box format (xmin, ymin, xmax, ymax).

    Args:
        contour (np.ndarray): An array with coordinates defining the contour of an object.

    Returns:
        tuple: A tuple containing the bounding box coordinates (xmin, ymin, xmax, ymax).

    Example::

        contour = np.array([[[3, 3]], [[3, 5]], [[5, 5]], [[5, 3]]], dtype=np.int32)
        bbox = contour2bbox(contour)
        print(bbox)
        (3, 3, 6, 6)

    Note:
        - The function uses OpenCV's `cv2.boundingRect` to compute the bounding box.

    """
    x_min, y_min, w, h = cv2.boundingRect(contour)
    return (x_min, y_min, x_min + w, y_min + h)
