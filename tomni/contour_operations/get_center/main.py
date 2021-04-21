from typing import Tuple
from typing import Tuple

import cv2
import numpy as np

def get_center(contour: np.array) -> Tuple[int, int]:
    '''
    Return the center of a contour
    '''
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return contour[0][0][0], contour[0][0][1]
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY