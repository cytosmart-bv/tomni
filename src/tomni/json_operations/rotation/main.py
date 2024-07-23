import copy
from typing import Union


def rotate_json(json_object: dict, angle: int, img_shape: Union[list, tuple]) -> dict:
    """
    Rotate a JSON object (ellipse or polygon) by 0, 90, 180, or 270 degrees.

    Args:
        json_object (dict): JSON object following the standard AxionBio format (ellipse or polygon).
        angle (int): The angle of rotation. Choose from 0, 90, 180, or 270 degrees.
        img_shape (list or tuple): The shape of the image related to the JSON object, represented as (width, height).

    Returns:
        dict: A new JSON object with the specified rotation.

    Raises:
        ValueError: If the angle is not one of 0, 90, 180, or 270 degrees.
    """

    assert len(img_shape) == 2

    newjson_object = copy.deepcopy(json_object)

    if json_object["type"] == "ellipse":
        if angle != 0:
            newjson_object["center"] = rotate_point(
                json_object["center"], angle, img_shape
            )

    elif json_object["type"] == "polygon":
        if angle != 0:
            newjson_object["points"] = [
                rotate_point(point, angle, img_shape) for point in json_object["points"]
            ]
            if "inner_points" in json_object:
                newjson_object["inner_points"] = [
                    [
                        rotate_point(inner_point, angle, img_shape)
                        for inner_point in inner_contour
                    ]
                    for inner_contour in json_object["inner_points"]
                ]

    else:
        raise ValueError(
            "Unknown JSON object type. Supported types are 'ellipse' and 'polygon'."
        )

    return newjson_object


def rotate_point(point: dict, angle_deg: int, img_shape: Union[list, tuple]) -> dict:
    """Rotate a 2D point by a specified angle in degrees.

    Args:
        point (dict): A dictionary representing the 2D point with 'x' and 'y' coordinates.
        angle_deg (int): The angle of rotation in degrees. Valid values are 0, 90, 180, or 270 degrees.
        img_shape (Union[list, tuple]): The shape of the image related to the JSON object, represented as (width, height).

    Raises:
        ValueError: If the angle_deg is not one of 0, 90, 180, or 270 degrees.

    Returns:
        dict: A new dictionary representing the rotated 2D point.
    """
    x, y = point["x"], point["y"]
    if angle_deg == 90:
        return {"x": img_shape[0] - y - 1, "y": x}
    elif angle_deg == 180:
        return {"x": img_shape[1] - x - 1, "y": img_shape[0] - y - 1}
    elif angle_deg == 270:
        return {"x": y, "y": img_shape[1] - x - 1}
    else:
        raise ValueError("Unknown angle. Angle should be 0, 90, 180, or 270 degrees.")
