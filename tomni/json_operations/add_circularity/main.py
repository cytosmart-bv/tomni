import math

import cv2

from ...contour_operations import circularity
from ...transformers import json2contours


def add_circularity(json_object: dict) -> None:
    """
    Calculate and add the circularity property to a JSON annotation object.
    The circularity is calculated by drawing a circle around the object and comparing
    the area of the circle with the area of the object.

    Args:
        json_object (dict): A JSON object of type "polygon" following the standard AxionBio format.

    Raises:
        ValueError: If the type of the annotation in the JSON object is not "polygon."

    Note:
        - Only polygon objects are supported for circularity calculation.
        - The circularity value is added as the "circularity" property to the JSON object.
        - The closer the circularity is to 1.0, the more circular the object is.
    """

    if json_object["type"] == "polygon":
        cnt = json2contours(json_object)

        _circularity = circularity(cnt)

        # Add results to current object
        json_object["circularity"] = _circularity
    else:
        raise ValueError(
            f"Currently only the polygon objects are supported; not {json_object['type']}"
        )
