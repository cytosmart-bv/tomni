import numpy as np


def mask2bbox(mask: np.ndarray, padding: int = 0) -> tuple:
    """
    Convert a binary image mask into bounding box coordinates (xmin, ymin, xmax, ymax).

    Args:
        mask (np.ndarray): a binary image mask.
        padding (int, optional): Padding add/subtracted from the bounding box
            (xmin-padding, ymin-padding, xmax+padding, ymax+padding). The bounding box coordinates
            do not get outside the image dimensions. e.g bbox (1,3,1,3) image_dim (2,2), padding 2;
            resulting bbox (0, 3, 0,3). Defaults to 0.

    Returns:
        tuple: (xmin, ymin, xmax, ymax)
    """
    x1, x2, y1, y2 = (0, 0, 0, 0)

    max_x = np.max(mask, axis=0)
    max_y = np.max(mask, axis=1)

    x_nonzeros = np.nonzero(max_x)
    y_nonzeros = np.nonzero(max_y)

    if x_nonzeros:
        if len(x_nonzeros[0] > 0):
            x1 = np.nonzero(max_x)[0][0]
            x2 = np.nonzero(max_x)[0][-1] + 1
    else:
        return (x1, y1, x2, y2)

    if y_nonzeros:
        if len(y_nonzeros[0]) > 0:
            y1 = np.nonzero(max_y)[0][0]
            y2 = np.nonzero(max_y)[0][-1] + 1
    else:
        return (x1, y1, x2, y2)

    if x1 == y1 == x2 == y2 == 0:
        return (x1, y1, x2, y2)

    # Add padding to bounding box
    if x1 - padding < 0:
        x1 = 0
    else:
        x1 -= padding

    if x2 + padding >= mask.shape[1]:
        x2 = mask.shape[1]
    else:
        x2 += padding

    if y1 - padding < 0:
        y1 = 0
    else:
        y1 -= padding

    if y2 + padding >= mask.shape[0]:
        y2 = mask.shape[0]
    else:
        y2 += padding

    return (x1, y1, x2, y2)
