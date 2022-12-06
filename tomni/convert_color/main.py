from typing import Union
import numpy as np
import cv2


def convert_color(img: np.ndarray, new_color: Union[str, int]) -> np.ndarray:
    """
    Convert a the color of an image to a wanted color, without needed to know the current color.
    It will assume only gray, BGR, and BGRA exists (these are the common openCV color types)

    Args:
        img (np.ndarray uint8): The image that needs to be converted. This image is gray, BGR or BGRA
        new_color (Union[str, int]): Color the new image should be gray (1), BGR (2) or BGRA (3)

    Raises:
        ValueError: new_color is not supported
        ValueError: img has more then 3 dimensions or less then 2
        ValueError: img as a number of channels that is not 1, 3, or 4

    Returns:
        np.ndarray: converted image
    """
    img = img.astype(np.uint8)
    # Not getting into that debate
    if type(new_color) is str:
        if new_color.upper() in ["GRAY", "GREY"]:
            new_color = 1
        # Also not getting into that debate
        elif new_color.upper() in ["BGR", "COLOR", "COLOUR"]:
            new_color = 3
        elif new_color.upper() in ["BGRA", "TRANSPARENT"]:
            new_color = 4
        else:
            new_color = -1

    if new_color not in [1, 3, 4]:
        raise ValueError(
            "The image type {} is not supported. Currently supported: GRAY (1), BGR (3) and BGRA (4)".format(
                new_color
            )
        )

    # Determine the color type of current image
    if len(img.shape) == 2:
        currentType = 1
    elif len(img.shape) != 3:
        raise ValueError(
            "The image does not have known dimensions ({}). It should have 2 or 3 dimensions.".format(
                img.shape
            )
        )
    elif img.shape[2] == 1:
        img = img[:, :, 0]
        currentType = 1
    elif img.shape[2] == 3:
        currentType = 3
    elif img.shape[2] == 4:
        currentType = 4
    else:
        raise ValueError(
            "The image type {} is not supported. Currently supported: GRAY (1), BGR (3) and BGRA (4)".format(
                img.shape[2]
            )
        )

    # That was easy
    if currentType == new_color:
        return img

    if currentType == 1 and new_color == 3:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if currentType == 1 and new_color == 4:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)

    if currentType == 3 and new_color == 1:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if currentType == 3 and new_color == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    if currentType == 4 and new_color == 1:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    if currentType == 4 and new_color == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
