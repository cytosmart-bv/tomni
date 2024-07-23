from __future__ import division
import numpy as np
import cv2
from . import bbox_fitting


def make_mask_ellipse(image_size, x1, y1, rx, ry):
    """
    Create an image with an ellipse of True surrounded by False.

    Args:
        image_size (tuple): The size of the image (width, height).
        x1 (int): The x-coordinate of the center of the ellipse.
        y1 (int): The y-coordinate of the center of the ellipse.
        rx (int): The length of the radius on the x-axis of the ellipse.
        ry (int): The length of the radius on the y-axis of the ellipse.

    Returns:
        np.ndarray: An image with an ellipse represented as True values surrounded by False values.

    Note:
        - The function uses either 'make_small_mask_ellipse' or 'make_big_mask_ellipse' based on the size of the ellipse.
        - For rotated ellipses, additional support for 'alpha' can be added in future updates.

    """
    x1 = int(x1)
    y1 = int(y1)
    rx = int(rx)
    ry = int(ry)

    if rx < 1 or ry < 1:
        raise ValueError("Radii must be greater than 1.")
    else:
        if (rx < 100) and (ry < 100):
            return make_small_mask_ellipse(image_size, x1, y1, rx, ry)
        else:
            return make_big_mask_ellipse(image_size, x1, y1, rx, ry)


def make_small_mask_ellipse(image_size, x1, y1, rx, ry):
    """
    Create an image with a small ellipse of True surrounded by False.

    Args:
        image_size (tuple): The size of the image (width, height).
        x1 (int): The x-coordinate of the center of the ellipse.
        y1 (int): The y-coordinate of the center of the ellipse.
        rx (int): The length of the radius on the x-axis of the ellipse.
        ry (int): The length of the radius on the y-axis of the ellipse.

    Returns:
        np.ndarray: An image with a small ellipse represented as True values surrounded by False values.

    """
    yy, xx = np.mgrid[: image_size[1], : image_size[0]]

    xx = xx.astype(np.int32)
    yy = yy.astype(np.int32)

    # Center point of the ellipse becomes the (0, 0) point of the image
    xx -= x1
    yy -= y1

    # The ellipse formula used to calculate the points is
    # x^2 * (ry)^2 + y^2 * (rx)^2
    # Calculating the value of each point depending on the ellipse equation
    ellipse = (xx**2) * (ry**2) + (yy**2) * (rx**2)

    # The ellipse formula determines if a point is inside the ellipse or not
    # x^2 * (ry)^2 + y^2 * (rx)^2 <= (rx)^2 * (ry)^2
    kernel = ellipse <= (rx**2) * (ry**2)
    kernel = kernel * (np.abs(xx) <= rx)
    kernel = kernel * (np.abs(yy) <= ry)
    return kernel


def make_big_mask_ellipse(image_size, xe, ye, rex, rey):
    """
    Create an image with a large ellipse of True surrounded by False.

    Args:
        image_size (tuple): The size of the image (width, height).
        xe (int): The x-coordinate of the ellipse.
        ye (int): The y-coordinate of the ellipse.
        rex (int): The radius on the x-axis of the ellipse.
        rey (int): The radius on the y-axis of the ellipse.

    Returns:
        np.ndarray: An image with a large ellipse represented as True values surrounded by False values.

    """

    out = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (rex * 2, rey * 2))
    x0 = -(xe - rex)
    y0 = -(ye - rey)
    x1 = image_size[0] + x0
    y1 = image_size[1] + y0
    out = bbox_fitting(out, x0, y0, x1, y1)
    return out
