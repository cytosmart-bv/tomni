from __future__ import division
import numpy as np
import cv2
from . import bbox_fitting


def make_mask_ellipse(image_size, x1, y1, rx, ry):

    """
    :param image_size: the size of the image
    :param x1: x coordinate of the center of the ellipse
    :param y1: y coordinate of the center of the ellipse
    :param rx: the length of the radius on the x axis of the ellipse
    :param ry: the length of the radius on the y axis of the ellipse
    :return: an image with an ellipse of True surrounded by False

    The big ellipse function is less precise but better at memory management.
    The small ellipse function is more precise.

    """

    if rx < 3 or ry < 3:
        raise ValueError("Radii must be greater than 3.")
    else:
        if (rx < 100) or (ry < 100):
            return make_small_mask_ellipse(image_size, x1, y1, rx, ry)
        else:
            return make_big_mask_ellipse(image_size, x1, y1, rx, ry)


def make_small_mask_ellipse(image_size, x1, y1, rx, ry):
    """

    :param image_size: the size of the image
    :param x1: x coordinate of the center of the ellipse
    :param y1: y coordinate of the center of the ellipse
    :param rx: the length of the radius on the x axis of the ellipse
    :param ry: the length of the radius on the y axis of the ellipse
    :return: an image with an ellipse of True surrounded by False
    
    Futere request: Variable Alpha.
    
    For rotated ellipses, the alpha value is used to find the translated points
    alpha = angle of rotation (in degrees)
    alpha = 0 gives no rotation of the ellipse

    The sin() and cos() values are calculated using math library

    The following formula can be used to calculate the coordinates:
    circle = ((xx * math.cos(alpha) + yy * math.sin(alpha)) ** 2) * (rx ** 2) +\
             # ((xx * math.sin(alpha) - yy * math.cos(alpha)) ** 2) * (ry ** 2)
    """

    # Make sure everything is integers (no floats) -> double all values
    rx = 2 * rx
    ry = 2 * ry

    yy, xx = np.mgrid[:image_size[1], :image_size[0]] * 2

    xx = xx.astype(np.int32)
    yy = yy.astype(np.int32)

    # Center point of the ellipse becomes the (0, 0) point of the image
    xx -= 2 * x1
    yy -= 2 * y1

    # The ellipse formula used to calculate the points is
    # x^2 * (ry)^2 + y^2 * (rx)^2
    # Calculating the value of each point depending on the ellipse equation
    ellipse = (xx ** 2) * (ry ** 2) + (yy ** 2) * (rx ** 2)

    # The ellipse formula determines if a point is inside the ellipse or not
    # x^2 * (ry)^2 + y^2 * (rx)^2 <= (rx)^2 * (ry)^2
    kernel = ellipse <= (rx ** 2) * (ry ** 2)

    return kernel


def make_big_mask_ellipse(image_size, xe, ye, rex, rey):
    """

    :param image_size:
    :param xe: x coordinate of the ellipse
    :param ye: y coordinate of the ellipse
    :param rex: the radius on the x axis of the ellipse
    :param rey: the radius on the y axis of the ellipse
    :return: an array with True and False corresponding to the ellipse mask in the image
    """

    out = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (rex * 2, rey * 2))
    x0 = -(xe - rex)
    y0 = -(ye - rey)
    x1 = image_size[0] + x0
    y1 = image_size[1] + y0
    out = bbox_fitting(out, x0, y0, x1, y1)
    return out

