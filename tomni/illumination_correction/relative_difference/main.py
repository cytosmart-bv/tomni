import numpy as np
import cv2


def relative_difference(
    img: np.ndarray,
    gauss_size: int = 301,
    smooth_size=None,
    do_normalize: bool = False,
    resize_ratio=None,
) -> np.array:
    """
    Remove large blurry artifacts from an image by calculating the relative difference
    between the blurred and raw image.

    Args:
        img (numpy.ndarray): The input image.
        gauss_size (int, optional): The size of the Gaussian filter kernel for artifact removal.
                                    Must be an odd number. Defaults to 301.
        smooth_size (int, optional): The size of the Gaussian filter kernel applied to the image
                                    before division. Must be an odd number. Defaults to None.
        do_normalize (bool, optional): If True, the output image is normalized between the minimum
                                       and maximum values of the smoothed image. Defaults to False.
        resize_ratio (float, optional): Resize ratio for the input image before applying Gaussian blur.
                                       Used to increase processing speed. Defaults to None.

    Returns:
        numpy.ndarray: The result image after artifact removal.

    Warning:
        - The `gauss_size` should be an odd number; if it's even, it will be incremented by 1.
        - This algorithm is not fractal, meaning that applying illumination correction followed by cropping will produce a different result than cropping first.

    Note:
        This function can be used for human vision and as input for algorithms relying on relative pixel differences.
    """

    img = np.float32(img)

    if gauss_size % 2 == 0:
        gauss_size += 1

    if smooth_size:
        img = cv2.GaussianBlur(img, (smooth_size, smooth_size), 0)

    max_img = np.max(img)
    min_img = np.min(img)

    if resize_ratio:
        gb = cv2.resize(
            img,
            (0, 0),
            fx=resize_ratio,
            fy=resize_ratio,
            interpolation=cv2.INTER_LINEAR,
        )
        gb = cv2.GaussianBlur(
            gb, (gauss_size, gauss_size), 0, borderType=cv2.BORDER_REPLICATE
        )
        gb = cv2.resize(
            gb, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR
        )
    else:
        gb = cv2.GaussianBlur(img, (gauss_size, gauss_size), 0)
        gb = np.float32(gb)

    img = np.divide(img, gb + 1e-15, dtype=np.float32)

    if do_normalize:
        img = cv2.normalize(img, img, max_img, min_img, cv2.NORM_MINMAX)
    else:
        img = np.divide(img, np.max(img) + 1e-15, dtype=np.float32) * 255

    return img.astype(np.uint8)
