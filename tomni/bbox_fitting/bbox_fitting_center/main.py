from __future__ import absolute_import, division
from typing import List
from . import bbox_fitting
from math import ceil
import numpy as np


def bbox_fitting_center(img: np.ndarray, size, padding_value: int = 0) -> np.ndarray:
    """
    Creates an image of size 'size' in IMAGE-Coordinates by centering and padding the original image.

    Args:
        img (numpy.ndarray): The original image.
        size (List[int]): The target size of the output image as [x, y].
        padding_value (int, optional): The value used for padding. Defaults to 0.

    Returns:
        numpy.ndarray: The resulting image of the specified size.

    Raises:
        TypeError: If img is not a numpy.ndarray.
        ValueError: If size elements are not positive integers.

    Example::

        img = np.zeros((100, 100))
        size = [50, 50]
        result = bbox_fitting_center(img, size)
        result.shape
        (50, 50)  # The resulting image size.
    """
    if not isinstance(img, np.ndarray):
        raise TypeError("Img needs to be a numpy.ndarry not {}".format(type(img)))

    if not isinstance(size[0], int) or not isinstance(size[1], int):
        raise ValueError(
            "x1, y1, x2 and y2 need to be a positive int not {}, {}".format(
                type(size[0]), type(size[1])
            )
        )
    x1 = -(size[0] - img.shape[1]) / 2
    y1 = -(size[1] - img.shape[0]) / 2
    x2 = x1 + size[0]
    y2 = y1 + size[1]

    # Round the number to fit exactly with the pixels
    x1 = int(ceil(x1))
    y1 = int(ceil(y1))
    x2 = int(ceil(x2))
    y2 = int(ceil(y2))

    return bbox_fitting(img, x1=x1, y1=y1, x2=x2, y2=y2, padding_value=padding_value)
