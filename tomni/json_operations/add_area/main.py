import math
import cv2
from ...transformers import json2contours


def add_area(json_object: dict) -> None:
    """Takes in a json object (ellipse, polygon and circle, standard cytosmart format)
        add the objects area to the json object.

    Args:
        json_object (dict): following the standard CytoSMART format

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
