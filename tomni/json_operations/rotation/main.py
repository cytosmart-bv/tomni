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
        if angle == 0:
            newjson_object["center"]["x"] = json_object["center"]["x"]
            newjson_object["center"]["y"] = json_object["center"]["y"]
        elif angle == 90:
            newjson_object["center"]["x"] = (
                img_shape[0] - json_object["center"]["y"] - 1
            )
            newjson_object["center"]["y"] = json_object["center"]["x"]

        elif angle == 180:
            newjson_object["center"]["x"] = (
                img_shape[1] - json_object["center"]["x"] - 1
            )
            newjson_object["center"]["y"] = (
                img_shape[0] - json_object["center"]["y"] - 1
            )

        elif angle == 270:
            newjson_object["center"]["x"] = json_object["center"]["y"]
            newjson_object["center"]["y"] = (
                img_shape[1] - json_object["center"]["x"] - 1
            )

        else:
            raise ValueError("Unkown Angle should be 0, 90, 180 or 270")
    elif json_object["type"] == "polygon":
        if angle == 0:
            newjson_object["points"] = json_object["points"]

        elif angle == 90:
            for point_n in range(len(newjson_object["points"])):
                newjson_object["points"][point_n]["x"] = (
                    img_shape[0] - json_object["points"][point_n]["y"] - 1
                )
                newjson_object["points"][point_n]["y"] = json_object["points"][point_n][
                    "x"
                ]

        elif angle == 180:
            for point_n in range(len(newjson_object["points"])):
                newjson_object["points"][point_n]["x"] = (
                    img_shape[1] - json_object["points"][point_n]["x"] - 1
                )
                newjson_object["points"][point_n]["y"] = (
                    img_shape[0] - json_object["points"][point_n]["y"] - 1
                )

        elif angle == 270:
            for point_n in range(len(newjson_object["points"])):
                newjson_object["points"][point_n]["x"] = json_object["points"][point_n][
                    "y"
                ]
                newjson_object["points"][point_n]["y"] = (
                    img_shape[1] - json_object["points"][point_n]["x"] - 1
                )

        else:
            raise ValueError("Unkown Angle should be 0, 90, 180 or 270")

    return newjson_object
