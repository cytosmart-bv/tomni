import math

import cv2

from ...contour_operations import circularity
from ...transformers import json2contours


def add_circularity(json_object: dict) -> None:
    """
    This function adds the property 'circularity' to the current json object.
    circularity is calculated by drawing a circle around the object,
    and then compare the area of the circle with area of the object.
    The bigger the difference between those 2 areas, the lower the circularity.

    json_object: (dict) a json object of type polygon
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
