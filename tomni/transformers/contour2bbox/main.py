import cv2
import numpy as np


def contour2bbox(contour: np.ndarray) -> tuple:
    """
    Converts opencv2 contours into (xmin, ymin, xmax, ymax) bounding box format

    Args:
        contour (np.ndarray): an array with the coordinates that defines the contour of a object
        e.g
        Contour
        array( [[[3, 3]],

                [[3, 5]],

                [[5, 5]],

                [[5, 3]]], dtype=int32)

        The object
        array( [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)

        boundingbox (3, 3, 6, 6)

    Returns:
        tuple: (xmin, ymin, xmax, ymax)
    """
    x_min, y_min, w, h = cv2.boundingRect(contour)
    return (x_min, y_min, x_min + w, y_min + h)
