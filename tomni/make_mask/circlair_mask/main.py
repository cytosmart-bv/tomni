from __future__ import division
import numpy as np
import cv2
from . import bbox_fitting_center


def make_mask_circle(img_shape: tuple, diameter: int) -> np.ndarray:
    """
    This function produces a boolean image with a circle of True surrounded by False.
    img_shape is in image-coordinates. Diameter is in pixels.
    In case the circle is bigger than 100 pixels a different function is used.
    The big circle function is less precise but better at memory management.

    img_shape: (tuple, shape (2,) ) the shape of the image given in image coordinates.
        These can be obtained with img_dim.
    diameter: (int) the diameter of the circle given in pixels.

    return:
        numpy array with type boolean
    """
    if diameter < 100:
        return make_small_mask_circle(img_shape, diameter)
    else:
        return make_big_mask_circle(img_shape, diameter)


def make_small_mask_circle(img_shape, diameter):
    xx, yy = np.mgrid[: img_shape[1], : img_shape[0]] * 2

    xx = xx.astype(np.int32)
    yy = yy.astype(np.int32)

    xx -= img_shape[1] - 1
    yy -= img_shape[0] - 1

    circle = xx ** 2 + yy ** 2
    kernel = circle <= diameter ** 2

    return kernel


def make_big_mask_circle(img_shape, diameter):
    out = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (diameter, diameter))
    out = bbox_fitting_center(out, img_shape)
    return out.astype(np.bool)
