import numpy as np

from ...bbox_fitting import bbox_fitting_center


def bbox_fitting_center_by_scale(image: np.ndarray, scale: float = 1.0) -> np.ndarray:
    """Centered bounding fit of image by its scale. The bbox is determined by the scale. 
    For example a 100*100 image with a input scale of 0.5 will create a bbox in the center of the image with 50*50.

    Args:
        image (np.ndarray): Image to be resized.
        scale (int): Percentage to scale a bbox to. Scale must to be in (0,1]. Example: scale=0.75 fits a bbox that takes 75% of the original image.

    Raises:
        ValueError: If scale not in (0,1].

    Returns:
        np.ndarray: Cropped image.
    """
    if 0 < scale <= 1.0:
        width_scaled = int(image.shape[1] * scale)
        height_scaled = int(image.shape[0] * scale)
        cropped_img = bbox_fitting_center(image, (width_scaled, height_scaled))
        return cropped_img
    else:
        raise ValueError("Scale must be a float in (0,1].")
