from typing import List, Union
import copy
from ...transformers import json2contours
from ...contour_operations import get_center
from ..translation import translation_json


def json_object_to_keep(
    json_object: dict, new_x: tuple, new_y: tuple, crop_mode: str = "remove_objects"
) -> bool:
    """
    Check if a JSON object should be kept or removed based on its position relative to the cropped area.

    Args:
        json_object (dict): JSON object following the standard AxionBio format.
        new_x (tuple): Tuple (xmin_crop, xmax_crop) representing the x dimensions of the cropped image.
        new_y (tuple): Tuple (ymin_crop, ymax_crop) representing the y dimensions of the cropped image.
        crop_mode (str): Crop mode, either "remove_objects" (default) or "keep_objects".

    Returns:
        bool: True if the JSON object should be kept, False otherwise.

    Note:
        - In "remove_objects" mode, the JSON object is removed if its center is outside the crop area.
        - In "keep_objects" mode, JSON objects with centers outside the crop but with parts inside the
          crop are kept, and new JSON objects are created with adjusted centers.

    Raises:
        ValueError: If the type of the annotation in the JSON object is not "polygon" or "ellipse".
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
    Crop a list of JSON objects based on translation and crop dimensions.

    Args:
        json_list (List[dict]): A list of JSON objects in standard AxionBio format.
        x_translation (int): The translation in the x-direction of the cropped JSON relative to the original JSON.
        y_translation (int): The translation in the y-direction of the cropped JSON relative to the original JSON.
        crop_dim (Union[list, tuple]): Crop dimensions (x, y) of the cropped JSON.
        crop_mode (str): Crop mode, either "remove_objects" (default) or "keep_objects".

    Returns:
        List[dict]: A list of JSON objects after cropping and translation.

    Note:
        - In "remove_objects" mode, JSON objects with centers outside the crop area are removed.
        - In "keep_objects" mode, JSON objects with centers outside the crop area but with parts inside the
          crop area are kept, and new JSON objects are created with adjusted centers.
    """

    new_json_list = []

    json_list_copy = copy.deepcopy(json_list)

    for c, json_object in enumerate(json_list):
        json_copy = copy.deepcopy(json_object)
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
