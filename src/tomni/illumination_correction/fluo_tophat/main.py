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
    """
    output_img = np.clip(img, min_val, max_val)
    output_img = (output_img - min_val) / (max_val - min_val) * 255
    return output_img.astype(np.uint8)


def fluo_tophat(img, normalize=0):
    """
    Fluorescent Top-Hat Background Subtraction

    This function performs background subtraction on a fluorescent channel image using a morphological white top-hat filter.
    The white top-hat filter is effective at highlighting small bright structures against a darker background.

    Args:
        img (numpy.ndarray): A grayscale image where background subtraction will be applied.
        normalize (int, optional): If set to 1, the resulting image will be normalized to the 0-255 range. Defaults to 0.

    Returns:
        img (numpy.ndarray): The image after background subtraction.
        p2 (float): The lower bound value used for potential later normalization.
        p98 (float): The upper bound value used for potential later normalization.

    Note:
        The `p2` and `p98` values represent the lower and upper bounds for potential image normalization. They are not automatically applied to the image to avoid data loss. These values can be used during integration and passed to the front-end for further processing.

    Example:
        To perform background subtraction on an image and normalize the result, you can use this function as follows:

        >>> result_image, lower_bound, upper_bound = fluo_tophat(image, normalize=1)
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
