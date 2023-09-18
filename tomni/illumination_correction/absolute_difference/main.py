import numpy as np
import cv2
import warnings


def absolute_difference(
    img: np.ndarray, gauss_size: int = 21, new_median: int = 128
) -> np.ndarray:
    """
    Remove large blurry artifacts from an image by taking the absolute difference
    between the blurred and original image.

    Args:
        img (numpy.ndarray): The input image.
        gauss_size (int, optional): The size of the Gaussian filter kernel for blurring.
                                    Must be an odd number. Defaults to 21.
        new_median (int, optional): The target median value for the resulting image.
                                    Defaults to 128.

    Returns:
        numpy.ndarray: The processed image with blurry artifacts removed.

    Warning:
        - This function is not suitable for human vision and may produce artifacts.
        - The `gauss_size` should be an odd number; if it's even, it will be incremented by 1.

    Note:
        This algorithm is fractal, meaning that applying illumination correction
        followed by cropping will yield the same result as cropping first.
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
