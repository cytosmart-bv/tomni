import cv2
import numpy as np


def circularity(contour: np.ndarray) -> float:
    """
    Calculates the circularity of a contour.
    This is based on the perimeter and area of the contour.
    A circle will give the smallest area for a given perimeter, so this is 1.

    The smaller the area is for a perimeter the less circular the contour is.
    So the closer is get to 0.

    The formula works from calculating the r**2 based on Area and Perimeter
    Area based:
    r**2 = A/pi

    Perimeter based:
    r**2 = (p/2*pi)**2

    Dividing these two gives circularity
    c = (A/pi) / (p/2*pi)**2 = (4 * pi * A) / (p**2)

    Args:
        contour (np.ndarray): Contour as given by opencv

    Returns:
        float: circularity (0 < c <= 1)
    """
    # calculate size
    area = cv2.contourArea(contour)

    # calculate shape
    perimeter = cv2.arcLength(contour, True)

    circularity = (4 * np.pi * area) / (perimeter**2)

    return circularity
