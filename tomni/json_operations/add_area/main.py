import math
import cv2
from ...transformers import json2contours


def add_area(json_object: dict) -> None:
    """
    Calculate and add the area of a geometric object to a JSON annotation object.

    This function takes a JSON object representing a geometric annotation in standard AxionBio format (ellipse, polygon, or circle),
    calculates the area of the object, and adds it as the "area" key in the JSON object.

    Args:
        json_object (dict): A JSON object following the standard AxionBio format.

    Raises:
        ValueError: If the type of the annotation in the JSON object is not supported.

    Example::

        circle_json = {
            "type": "circle",
            "center": {"x": 10, "y": 10},
            "radiusX": 5
        }
        add_area(circle_json)
        print(circle_json)
        {
            "type": "circle",
            "center": {"x": 10, "y": 10},
            "radiusX": 5,
            "area": 78.53981633974483
        }

    Note:
        - Supported annotation types are "circle," "ellipse," and "polygon."
        - The area is calculated based on the properties of the geometric object:
          - For circles, it uses the formula: π * (radiusX^2)
          - For ellipses, it uses the formula: π * radiusX * radiusY
          - For polygons, it calculates the area using OpenCV's `cv2.contourArea` function.
    """
    type_anno = json_object["type"]

    if type_anno == "circle":
        area = math.pi * (json_object["radiusX"] ** 2)

    elif type_anno == "ellipse":
        area = math.pi * json_object["radiusX"] * json_object["radiusY"]

    elif type_anno == "polygon":
        contour = json2contours(json_object)
        area = cv2.contourArea(contour)
    else:
        raise ValueError(f"{type_anno} is not supported")

    json_object["area"] = area
