import uuid
from typing import Union


def ellipse2json(
    x: int, y: int, radius: int, secondRadius: Union[None, int] = None, alpha: float = 0
) -> dict:
    """
    Convert ellipse parameters into a JSON object in standard AxionBio format.

    Args:
        x (int): The center x-position of the ellipse.
        y (int): The center y-position of the ellipse.
        radius (int): The radius of the ellipse.
        secondRadius (int, None, optional): The smallest radius of the ellipse. Defaults to None.
            In case of a circle or when not provided, it is assumed to be equal to 'radius'.
        alpha (float, optional): This is the angle between the biggest radius and the x-axis.
            Defaults to 0.

    Returns:
        dict: A JSON object representing the ellipse in standard AxionBio format.
    """
    result = []
    result = {
        "type": "ellipse",
        "center": {"x": int(x), "y": int(y)},
        "radiusX": int(radius),
        "radiusY": int(secondRadius) if secondRadius else int(radius),
        "angleOfRotation": alpha,
        "id": str(uuid.uuid4()),
    }
    return result
