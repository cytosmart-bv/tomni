import numpy as np


def mask2bbox(mask: np.ndarray, padding: int = 0) -> tuple:
    """
    Convert a binary image mask into bounding box coordinates (xmin, ymin, xmax, ymax).

    Args:
        mask (np.ndarray): A binary image mask represented as a NumPy array where 1 indicates the object
            of interest, and 0 indicates the background.
        padding (int, optional): Padding added or subtracted from the bounding box coordinates.
            The resulting bounding box coordinates will not exceed the image dimensions. If padding is positive,
            it adds padding to all sides of the bounding box; if negative, it subtracts padding.
            Defaults to 0.

    Returns:
        tuple: A tuple containing the bounding box coordinates (xmin, ymin, xmax, ymax).
            The coordinates represent the top-left and bottom-right corners of the bounding box.
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
