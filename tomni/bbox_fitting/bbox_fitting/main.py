import cv2
import numpy as np 

def bbox_fitting(img, x1, y1, x2, y2, padding_value=0):
    """
    Bounding box fitting:
    Using cropping and padding to fit an image to the bounding box.
    Relative to the 0,0 of the input image the image gets cropped and padded to fit with x1, y1, x2 and y2.
    The result is including the pixels x1, x2, y1 and y2.
    So a 0, 0, 9, 9 gives an 10x10 result.

    WARNING:
    Coordinates are IMAGE-coordinates. So that is the same pillow and OpenCV uses but swapped from what Numpy and Scipy use (ARRAY-coordinates).
    Yes, I hate it too.
    """

    if not isinstance(img, np.ndarray):
        raise TypeError("Img needs to be a numpy.ndarry not {}".format(type(img)))
    
    if not isinstance(x1, int) or not isinstance(x2, int) or not isinstance(y1, int) or not isinstance(y2, int):
        raise ValueError("x1, y1, x2 and y2 need to be a positive int not {}, {}, {}, {}".format(type(x1), type(y1), type(x2), type(y2)))

    # if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
    #     raise ValueError("x1, y1, x2 and y2 needs to be a possitive int. Given: {}, {}, {}, {}".format(x1, y1, x2, y2))

    if x2 < 0:
        return np.zeros((y2 - y1, x2 -x1))
    if y2 < 0:
        return np.zeros((y2 - y1, x2 -x1))
    if x1 >= img.shape[1]:
        return np.zeros((y2 - y1, x2 -x1))
    if y1 >= img.shape[0]:
        return np.zeros((y2 - y1, x2 -x1))

    cy1 = max(0, y1)
    cy2 = min(img.shape[0], y2)
    cx1 = max(0, x1)
    cx2 = min(img.shape[1], x2)
    
    pad_left = - min(0, x1)
    pad_right = max(x2 - img.shape[1], 0)
    pad_top = - min(0, y1)
    pad_bottom = max(y2 - img.shape[0], 0)
    
    img = img[cy1:cy2, cx1:cx2]
    
    img = cv2.copyMakeBorder(img,
                            top=pad_top, 
                            bottom=pad_bottom,
                            left=pad_left, 
                            right=pad_right, 
                            borderType=cv2.BORDER_CONSTANT, 
                            value=padding_value)

    return img
