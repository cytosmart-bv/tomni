import numpy as np


def fit_rect_around_ellipse(
    x: int, y: int, r1: float, r2: float, alpha: float
) -> (int, int, int, int):
    """
    This function gives the boundingbox around an ellipse.
    x, y: (int, int) middle point of ellipse
    r1: (float) longest radius
    r2: (float) shortest radius. By definition 90 degrees away from r1
    alpha: (float) degrees between r1 and x-axis.
    Special thanks to: https://math.stackexchange.com/questions/91132/how-to-get-the-limits-of-rotated-ellipse
    """
    alpha = alpha / 180 * np.pi
    a = np.sqrt(r1 ** 2 * np.cos(alpha) ** 2 + r2 ** 2 * np.sin(alpha) ** 2)
    b = np.sqrt(r1 ** 2 * np.sin(alpha) ** 2 + r2 ** 2 * np.cos(alpha) ** 2)
    x1 = int(round(x - a))
    y1 = int(round(y - b))
    x2 = int(round(x + a))
    y2 = int(round(y + b))
    return x1, y1, x2, y2
