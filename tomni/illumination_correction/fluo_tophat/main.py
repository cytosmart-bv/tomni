import cv2
import numpy as np
from scipy.stats import kurtosis, skew


def rescale_intensity(img, min_val, max_val):
    output_img = np.clip(img, min_val, max_val)
    output_img = (output_img - min_val) / (max_val - min_val) * 255
    return output_img.astype(np.uint8)


def fluo_tophat(img, normalize=0):
    """
    This is the background subtraction of the fluorescent channel.
    This subtraction can be used for the green and the red channel
    It uses a morphological white tophat filter to create a map of the subtraction.

    input:
        img: A standard grayscale image
        normalize: Normalizes the image from 0 to 255, this looks better but data will be lost
    
    output:
        img: The result image after background subtraction
        p2 : The lower bound value where an x-amount of pixels are included
        p98: The higher bound value where an y-amount of pixels are included  

    The p2 and p98 values are used to normalize the image, but won't be automatically applied
    due to loss of data. These values should be given later to the integration part so they can 
    pass these values to the front-end. 
    
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

