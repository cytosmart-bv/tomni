import cv2
import math
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

        # Calculate the area of enclosing circle
        enclosing_circle = cv2.minEnclosingCircle(cnt)
        radius = enclosing_circle[1]
        area_circle = radius ** 2 * math.pi

        # Calculate the area of contour
        area_contour = cv2.contourArea(cnt)
        circularity = area_contour / area_circle

        # Add results to current object
        json_object["circularity"] = circularity
    else:
        raise ValueError(
            f"currently only the polygon objects are supported not {json_object['type']}"
        )
