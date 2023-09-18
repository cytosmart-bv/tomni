from ...transformers import json2contours
from ...contour_operations import get_center


def add_center(json_object: dict):
    """
    Calculate and add the center coordinates to a JSON annotation object.

    This function takes a JSON object representing an annotation in standard AxionBio format (ellipse or polygon),
    calculates the center coordinates of the object, and adds them as the "center" key in the JSON object.

    Args:
        json_object (dict): A JSON object following the standard AxionBio format.

    Raises:
        ValueError: If the type of the annotation in the JSON object is not supported.

    Note:
        - Supported annotation types are "ellipse" and "polygon."
        - For ellipses, no action is taken as the center is already included in the JSON object.
        - For polygons, the center coordinates are calculated using the `get_center` function from the `contour_operations` module.
    """
    if json_object["type"] == "ellipse":
        pass
    elif json_object["type"] == "polygon":
        contour = json2contours(json_object)
        x, y = get_center(contour)
        json_object["center"] = {"x": x, "y": y}
    else:
        raise ValueError(f"No json type found of {json_object['type']}")
