from typing import List, Union
import copy
from ...transformers import json2contours
from ...contour_operations import get_center
from ..translation import translation_json


def json_object_to_keep(
    json_object: dict, new_x: tuple, new_y: tuple, crop_mode: str = "remove_objects"
) -> bool:
    """
    Checks if json_object is inside the cropped image.
    json_object: (dict) following the standard cytosmart format
    new_x (tuple) (xmin_crop, xmax_crop) the x dimensions of the cropped image
    new_y (tuple) (ymin_crop, ymax_crop) the y dimensions of the cropped images
    crop_mode: (string) "remove_objects" & "keep_objects". Default mode is 'remove_objects'
                using this mode removes json_object if center is outside the crop. "keep_objects"
                mode keeps the json objects where the center is outside the crop but parts of the
                objects are inside the crop. For these cases creates a new json object with a new center.
                Warning: mode "keep_objects" is still not included.
    """
    if crop_mode == "remove_objects":
        x, y = 0, 0
        if json_object["type"] == "polygon":
            contour = json2contours(json_object)
            x, y = get_center(contour)
        elif json_object["type"] == "ellipse":
            x, y = json_object["center"]["x"], json_object["center"]["y"]
        else:
            raise ValueError(f"No json type found of {json_object['type']}")

        within_crop = True
        if x < new_x[0] or x > new_x[1] or y < new_y[0] or y > new_y[1]:
            within_crop = False
    else:
        within_crop = True

    return within_crop


def crop_json(
    json_list: List[dict],
    x_translation: int,
    y_translation: int,
    crop_dim: Union[list, tuple],
    crop_mode: str = "remove_objects",
) -> List[dict]:
    """
    Takes a list of json objects (ellipse or polygon, standard cytosmart format)
    and removes or/and translates json object in the list. If the center of a
    json object lays outside the croped dimensions it removes the json objects.
    json_list: (list[dict]) a list of jsons in standard cytosmart format
    x_translation: (int) The translation in the x-direction of the cropped image
                relative to the original image
    y_translation: (int) The translation in the y-direction of the cropped image
                relative to the original image
    crop_dim: (list or tuple) (x,y) dimensions of the the cropped image
            that relate to the list of jsons
    crop_mode: (string) "remove_objects" & "keep_objects". Default mode is 'remove_objects'
                using this mode removes json_object if center is outside the crop. "keep_objects"
                mode keeps the json objects where the center is outside the crop but parts of the
                objects are inside the crop. For these cases creates a new json object with a new center.
                Warning: mode "keep_objects" is still not included.

    input_json_list = [
            {
                "type": "ellipse",
                "center": {"x": 2, "y": 3},
                "radiusX": 5,
                "radiusY": 5,
                "angleOfRotation": 0,
            },
            {   "type": "ellipse",
                "center": {"x": 4, "y": 7},
                "radiusX": 6,
                "radiusY": 6},
        ]

    crop_dim = (5, 6)
    x_translation = 2
    y_translation = 0

    expected_json_list = [
        {
            "type": "ellipse",
            "center": {"x": 0, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }
    ]
    """

    new_json_list = []

    json_list_copy = copy.deepcopy(json_list)

    for c, json_object in enumerate(json_list):
        json_copy= copy.deepcopy(json_object)
        to_keep = json_object_to_keep(
            json_copy,
            (x_translation, x_translation + crop_dim[0]),
            (y_translation, y_translation + crop_dim[1]),
            crop_mode,
        )
        if to_keep:
            json_list_copy[c] = translation_json(
                json_copy, -x_translation, -y_translation
            )

        else:
            continue

        new_json_list.append(json_list_copy[c])

    return new_json_list