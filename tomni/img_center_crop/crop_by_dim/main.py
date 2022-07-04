import numpy as np

from ...bbox_fitting import bbox_fitting_center


def crop_image_by_dim(image: np.ndarray, max_dimension: int) -> np.ndarray:
    """Center crop of image by dimension.

    Args:
        image (np.ndarray): Image to be cropped.
        max_dimension (int): The maximum dimension of the crop. Width*Height are max_dimension*max_dimension.

    Raises:
        ValueError: If the image is smaller than the dimension passed.
    Returns:
        np.ndarray: Cropped image.
    """
    if (
        image.shape[0] > max_dimension
        and image.shape[1] > max_dimension
        and max_dimension >= 0
    ):
        cropped_img = bbox_fitting_center(image, (max_dimension, max_dimension))
        return cropped_img
    elif image.shape[0] == max_dimension and image.shape[1] == max_dimension:
        return image
    else:
        raise ValueError(f"Invalid max_dimension of {max_dimension} passed.")
