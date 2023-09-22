import cv2
import numpy as np


def bbox_fitting(
    img: np.ndarray, x1: int, y1: int, x2: int, y2: int, padding_value: int = 0
) -> np.ndarray:
    """
    This function extracts a region of interest (ROI) from an input image based on a specified bounding box.
    It is particularly useful for isolating specific areas of interest within an image.

    Parameters:
        - img (np.ndarray): The input image from which the bounding box will be extracted.
        - x1 (int): The lowest value of X-coordinate for the bounding box.
        - y1 (int): The lowest value of Y-coordinate for the bounding box.
        - x2 (int): The highest value of X-coordinate for the bounding box.
        - y2 (int): The highest value of Y-coordinate for the bounding box.
        - padding_value (int, optional): The value assigned to pixels outside the image but within the bounding box. Defaults to 0.

    Returns:
        - np.ndarray: The extracted image patch within the specified bounding box.

    Raises:
        - TypeError: If img is not a numpy.ndarray.
        - ValueError: If x1, y1, x2, or y2 are not positive integers.

    Note:
        The coordinates used in this function are in IMAGE coordinates, which follow the convention used by Pillow and OpenCV but are swapped compared to the Numpy and Scipy convention (ARRAY coordinates). Please be mindful of this difference.

    """

    if not isinstance(img, np.ndarray):
        raise TypeError("Img needs to be a numpy.ndarry not {}".format(type(img)))

    if (
        not isinstance(x1, int)
        or not isinstance(x2, int)
        or not isinstance(y1, int)
        or not isinstance(y2, int)
    ):
        raise ValueError(
            "x1, y1, x2 and y2 need to be a positive int not {}, {}, {}, {}".format(
                type(x1), type(y1), type(x2), type(y2)
            )
        )

    if x2 < 0:
        return np.zeros((y2 - y1, x2 - x1))
    if y2 < 0:
        return np.zeros((y2 - y1, x2 - x1))
    if x1 >= img.shape[1]:
        return np.zeros((y2 - y1, x2 - x1))
    if y1 >= img.shape[0]:
        return np.zeros((y2 - y1, x2 - x1))

    cy1 = max(0, y1)
    cy2 = min(img.shape[0], y2)
    cx1 = max(0, x1)
    cx2 = min(img.shape[1], x2)

    pad_left = -min(0, x1)
    pad_right = max(x2 - img.shape[1], 0)
    pad_top = -min(0, y1)
    pad_bottom = max(y2 - img.shape[0], 0)

    img = img[cy1:cy2, cx1:cx2]

    img = cv2.copyMakeBorder(
        img,
        top=pad_top,
        bottom=pad_bottom,
        left=pad_left,
        right=pad_right,
        borderType=cv2.BORDER_CONSTANT,
        value=padding_value,
    )

    return img
