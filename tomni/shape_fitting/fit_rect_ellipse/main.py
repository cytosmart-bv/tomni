import numpy as np
from typing import Tuple


def fit_rect_around_ellipse(
    x: int, y: int, r1: float, r2: float, alpha: float
) -> Tuple[int, int, int, int]:
    """
    Compute the bounding box coordinates of an ellipse given its parameters.

    Args:
        x (int): The x-coordinate of the center of the ellipse.
        y (int): The y-coordinate of the center of the ellipse.
        r1 (float): The longest radius of the ellipse.
        r2 (float): The shortest radius of the ellipse, which is 90 degrees away from r1.
        alpha (float): The degrees between r1 and x-axis.

    Returns:
        Tuple[int, int, int, int]: A tuple containing the coordinates of the bounding box in the format (x1, y1, x2, y2).

    Special thanks to: https://math.stackexchange.com/questions/91132/how-to-get-the-limits-of-rotated-ellipse
    """
    alpha = alpha / 180 * np.pi
    a = np.sqrt(r1**2 * np.cos(alpha) ** 2 + r2**2 * np.sin(alpha) ** 2)
    b = np.sqrt(r1**2 * np.sin(alpha) ** 2 + r2**2 * np.cos(alpha) ** 2)
    x1 = int(round(x - a))
    y1 = int(round(y - b))
    x2 = int(round(x + a))
    y2 = int(round(y + b))
    return x1, y1, x2, y2
