import numpy as np
import cv2
import warnings


def absolute_difference(
    img: np.array, gauss_size: int = 21, new_median: int = 128
) -> np.array:
    """
    Remove big blurry artifact from the image.
    It will do this by taking the absolute difference between the blurred and raw image.

    # Usage
    Best not to use this for human vision.
    The algorithm can have weird artifacts.
    This is good as algorithm input for algorithms that rely on absolute pixel difference.

    # Fractal
    This algorithm is fractal. 
    Meaning the illumination correction followed by cropping will given the same result than first cropping.

    img (np.array): input image
    gauss_size (int): needs to be an odd number. 
        This is corralated to the size of the big artifact to remove.
    """

    img = np.array(img, dtype=np.int16)

    if gauss_size % 2 == 0:
        gauss_size += 1  # Only works with odd gauss size
        warnings.warn(
            "the gauss_size needs to be odd. It is {}. One is added to it".format(
                gauss_size
            ),
            SyntaxWarning,
        )

    """
    The illumination is every detail bigger than the gauss_size. 
    This includes the inside of square bigger than gauss_size, but not its borders.
    """
    img -= cv2.GaussianBlur(img, (gauss_size, gauss_size), 0)

    img += new_median

    # All overhead needs to be rounded down
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)
