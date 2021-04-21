from ...transformers import json2contours
from ...contour_operations import get_center

def add_center(json_object: dict):


    if json_object['type']=='ellipse':
        pass
    elif json_object['type']=='polygon':
        contour = json2contours(json_object)
        x, y = get_center(contour)
        json_object['center'] = {"x": x, "y": y}
    else:
        raise ValueError(f"No json type found of {json_object['type']}")
