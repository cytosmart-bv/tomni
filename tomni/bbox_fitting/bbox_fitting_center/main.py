from __future__ import absolute_import, division
from . import bbox_fitting
from math import ceil, floor
import numpy as np

def bbox_fitting_center(img, size, padding_value=0):
    '''
    Creates an image of size 'size' ([(int) x, (int) y]) in IMAGE-Coordinates).
    The orignal image will be centered and padded and/or cropped to fit the size.

    img: numpy.ndarray
    size: [int, int]

    output: numpy.ndarray
    '''
    if not isinstance(img, np.ndarray):
        raise TypeError("Img needs to be a numpy.ndarry not {}".format(type(img)))
    
    if not isinstance(size[0], int) or not isinstance(size[1], int):
        raise ValueError("x1, y1, x2 and y2 need to be a positive int not {}, {}".format(type(size[0]), type(size[1])))
    x1 = - (size[0] - img.shape[1])/2
    y1 = - (size[1] - img.shape[0])/2
    x2 = x1 + size[0]
    y2 = y1 + size[1]

    # Round the number to fit exactly with the pixels
    x1 = int(ceil(x1))
    y1 = int(ceil(y1))
    x2 = int(ceil(x2))
    y2 = int(ceil(y2))

    return bbox_fitting(img, x1=x1, y1=y1, x2=x2, y2=y2, padding_value=padding_value)