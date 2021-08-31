import cv2
import numpy as np

from ..json2contours import json2contours


def contour2mask(mask: np.ndarray, contour: list) -> np.ndarray:
    """[summary]

    Args:
        mask (np.ndarray): [description]
        contour (list): [description]

    Raises:
        ValueError: [description]
        ValueError: [description]

    Returns:
        np.ndarray: [description]
    """
    contour = np.array(contour, dtype=np.int32)
    shapeC = np.shape(contour)

    if len(shapeC) != 2:
        raise ValueError

    if shapeC[1] != 2:
        raise ValueError

    contour = contour.reshape((1, shapeC[0], 2))

    cv2.fillPoly(mask, contour, 1)
    return mask


def json2mask(json_objects: list, img_dim: tuple) -> np.ndarray:
    """
    Convert standard cytosmart format to binary mask

    Args:
        json_objects (list): json with annotations in standard cytosmart format
        img_dim (tuple): the dimensions of the mask

    Returns:
        np.ndarray: binary mask
    """
    mask = np.zeros(img_dim, dtype=np.uint8)
    for json_object in json_objects:

        contour = json2contours(json_object)
        contour = [x[0] for x in contour]
        mask = contour2mask(mask, contour)

    return mask