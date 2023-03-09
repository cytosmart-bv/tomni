import uuid
from typing import Union
import warnings


def ellipse2json(
    x: int, y: int, radius: int, secondRadius: Union[None, int] = None, alpha: float = 0
) -> dict:
    """
    x: (int) center x position
    y: (int) center y position
    radius: (int) the radius of the circle
    secondRadius: (int, None) (optional) In case of an ellipse, this is the smallest radius of the two.
    alpha: (float) (optional) In case of an ellipse. This is the angle between the biggest radius and the x-axis.
    """
    warnings.warn("Function is deprecated and will be removed in the future. Use the `AnnotationManager` instead.", DeprecationWarning)

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
