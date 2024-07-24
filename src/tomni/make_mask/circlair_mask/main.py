from __future__ import division
import numpy as np
import cv2
from . import bbox_fitting_center


def make_mask_circle(img_shape: tuple, diameter: int) -> np.ndarray:
    """
    Create a boolean image with a circle of True surrounded by False.

    Args:
        img_shape (tuple): The shape of the image given in image coordinates, represented as (width, height).
        diameter (int): The diameter of the circle in pixels.

    Returns:
        np.ndarray: A boolean image where the area enclosed by the circle is True and the rest is False.

    Note:
        - The function uses either 'make_small_mask_circle' or 'make_big_mask_circle' based on the size of the circle.
        - In case the diameter is greater than or equal to 100 pixels, the 'make_big_mask_circle' function is used for memory efficiency.
    """
    if diameter < 100:
        return make_small_mask_circle(img_shape, diameter)
    else:
        return make_big_mask_circle(img_shape, diameter)


def make_small_mask_circle(img_shape, diameter):
    """
    Create a boolean image with a small circle of True surrounded by False.

    Args:
        img_shape (tuple): The shape of the image given in image coordinates, represented as (width, height).
        diameter (int): The diameter of the circle in pixels.

    Returns:
        np.ndarray: A boolean image with a small circle represented as True values surrounded by False values.

    """
    xx, yy = np.mgrid[: img_shape[1], : img_shape[0]] * 2

    xx = xx.astype(np.int32)
    yy = yy.astype(np.int32)

    xx -= img_shape[1] - 1
    yy -= img_shape[0] - 1

    circle = xx**2 + yy**2
    kernel = circle <= diameter**2

    return kernel


def make_big_mask_circle(img_shape, diameter):
    """
    Create a boolean image with a large circle of True surrounded by False.

    Args:
        img_shape (tuple): The shape of the image given in image coordinates, represented as (width, height).
        diameter (int): The diameter of the circle in pixels.

    Returns:
        np.ndarray: A boolean image with a large circle represented as True values surrounded by False values.

    """
    out = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (diameter, diameter))
    out = bbox_fitting_center(out, img_shape)
    return out.astype(bool)
