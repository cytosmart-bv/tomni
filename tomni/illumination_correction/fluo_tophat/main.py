import cv2
import numpy as np
from scipy.stats import kurtosis, skew


def rescale_intensity(img, min_val, max_val):
    """
    Rescale pixel intensities of an image to the specified minimum and maximum values.

    Args:
        img (numpy.ndarray): The input image.
        min_val (int): The minimum pixel intensity value.
        max_val (int): The maximum pixel intensity value.

    Returns:
        numpy.ndarray: The rescaled image.

    Example:
        rescaled_image = rescale_intensity(image, 0, 255)
    """
    output_img = np.clip(img, min_val, max_val)
    output_img = (output_img - min_val) / (max_val - min_val) * 255
    return output_img.astype(np.uint8)


def fluo_tophat(img, normalize=0):
    """
    Perform background subtraction on a fluorescent channel image using a morphological
    white top-hat filter.

    Args:
        img (numpy.ndarray): A standard grayscale image.
        normalize (int, optional): Normalizes the image to the 0-255 range if set to 1.
                                   Defaults to 0.

    Returns:
        img (numpy.ndarray): The result image after background subtraction.
        p2 (float): The lower bound value where a percentage of pixels are included.
        p98 (float): The higher bound value where a percentage of pixels are included.

    The `p2` and `p98` values are used to normalize the image but are not automatically applied
    due to potential data loss. These values should be used later during integration to pass
    to the front-end.

    Example:
        result_image, lower_bound, upper_bound = fluo_tophat(image, normalize=1)
    """

    img = img.astype(np.uint8)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    filterSize = (25, 25)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, filterSize)
    img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel, iterations=10)

    kur = np.mean(kurtosis(img, fisher=True))
    skew1 = np.mean(skew(img))
    if kur > 1 and skew1 > 1:
        p2, p98 = np.percentile(img, (15, 99.5), interpolation="linear")
        if normalize == 1:
            img = rescale_intensity(img, p2, p98)
    else:
        p2, p98 = np.percentile(img, (15, 100), interpolation="linear")
        if normalize == 1:
            img = rescale_intensity(img, p2, p98)

    return img, p2, p98
