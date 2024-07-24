import numpy as np
import cv2
from typing import Union


def sendErrorShape(shapeC):
    raise TypeError("Expect contour in form (N, 2) not {}".format(shapeC))


def make_mask_contour(img_shape: tuple, contour: Union[list, np.ndarray]) -> np.ndarray:
    """
    Create a binary mask from a given contour and image shape. The mask sets pixels inside the contour to 1 (True)
    and pixels outside to 0 (False).

    Args:
        img_shape (tuple): The shape of the image given in image coordinates, represented as (width, height).
        contour (list or np.ndarray): The contour as outputted by OpenCV, with shape (N, 2).

    Returns:
        np.ndarray: A boolean image where the area enclosed by the contour is True and the rest is False.

    Raises:
        TypeError: If the provided contour is not in the form (N, 2), where N is the number of points.

    Example::

        # Usage example with OpenCV's contour output
        img_shape = (640, 480)  # Width and height of the target image
        contour = np.array([[100, 200], [200, 100], [300, 400]], dtype=np.int32)
        mask = make_mask_contour(img_shape, contour)
        # 'mask' will contain a binary mask representing the specified contour.
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
