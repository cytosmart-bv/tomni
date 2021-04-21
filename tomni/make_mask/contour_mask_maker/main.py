import numpy as np
import cv2
from typing import Union


def sendErrorShape(shapeC):
    raise TypeError("Expect contour in form (N, 2) not {}".format(shapeC))


def make_mask_contour(img_shape: tuple, contour: Union[list, np.ndarray]) -> np.ndarray:
    """
    This function produces a boolean image with the contour given.

    img_shape: (tuple, shape (2,) ) the shape of the image given in image coordinates.
        These can be obtained with img_dim.
    contour: (list, np.ndarray) This is a contour as outputted by opencv

    return:
        numpy array with type boolean
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
