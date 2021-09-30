import numpy as np


def mask2bbox(image: np.ndarray, padding: np.ndarray) -> tuple:
    max_x = np.max(image, axis=0)
    max_y = np.max(image, axis=1)

    x1, x2, y1, y2 = (0, -1, 0, -1)

    x_nonzeros = np.nonzero(max_x)
    y_nonzeros = np.nonzero(max_y)

    if x_nonzeros:
        if len(x_nonzeros[0] > 0):
            x1 = np.nonzero(max_x)[0][0]
            x2 = np.nonzero(max_x)[0][-1]
    else:
        return (x1, x2, y1, y2)

    if y_nonzeros:
        if len(y_nonzeros[0]) > 0:
            y1 = np.nonzero(max_y)[0][0]
            y2 = np.nonzero(max_y)[0][-1]
    else:
        return (x1, x2, y1, y2)

    if x1 == y1 == x2 == y2 == 0:
        return (x1, x2, y1, y2)

    if x1 - padding < 0:
        x1 = 0
    else:
        x1 -= padding

    if x2 + padding >= image.shape[1]:
        x2 = image.shape[1]
    else:
        x2 += padding

    if y1 - padding < 0:
        y1 = 0
    else:
        y1 -= padding

    if y2 + padding >= image.shape[0]:
        y2 = image.shape[0]
    else:
        y2 += padding

    return (x1, x2, y1, y2)
