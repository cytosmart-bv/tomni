import numpy as np
import cv2
from typing import Union


def sendErrorShape(shapeC):
    raise TypeError("Expect contour in form (N, 2) not {}".format(shapeC))


def make_mask_contour(img_shape: tuple, contour: Union[list, np.ndarray]) -> np.ndarray:
    """
    Create a boolean image with the specified contour.

    Args:
        img_shape (tuple): The shape of the image given in image coordinates, represented as (width, height).
        contour (list or np.ndarray): The contour as outputted by OpenCV, with shape (N, 2).

    Returns:
        np.ndarray: A boolean image where the area enclosed by the contour is True and the rest is False.

    Raises:
        TypeError: If the provided contour is not in the form (N, 2), where N is the number of points.

    """
    contour = np.array(contour, dtype=np.int32)
    shapeC = np.shape(contour)

    if len(shapeC) != 2:
        sendErrorShape(shapeC)

    if shapeC[1] != 2:
        sendErrorShape(shapeC)

    contour = contour.reshape((1, shapeC[0], 2))

    mask = np.zeros((img_shape[1], img_shape[0]), dtype=np.uint8)
    cv2.fillPoly(mask, contour, 1)
    return mask
