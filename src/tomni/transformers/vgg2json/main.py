import numpy as np
from typing import List
from ..ellipse2json import ellipse2json
from ..list_of_points2json import list_of_points2json


def vgg2json(vgg_data: dict) -> List[dict]:
    """
    Transforms data created with 'VGG Image Annotator' into a list of JSON objects.

    Args:
        vgg_data (dict): A JSON dictionary created with VGG Image Annotator, which can contain annotations
            for multiple images.

    Returns:
        List[List[dict]]: A list of lists of JSON dictionaries, where each inner list represents
        annotations for a single image, and each JSON dictionary contains annotation data.
    """
    results = []

    for filename in vgg_data.keys():
        result = []

        for annotation_vgg in vgg_data[filename]["regions"]:
            json_object = {}
            vgg_type = annotation_vgg["shape_attributes"]["name"]
            if vgg_type == "polygon":
                x_list, y_list = (
                    annotation_vgg["shape_attributes"]["all_points_x"],
                    annotation_vgg["shape_attributes"]["all_points_y"],
                )
                list_of_points = np.array([x_list, y_list]).transpose()
                json_object = list_of_points2json(list_of_points)
            elif vgg_type == "circle":
                cx, cy = (
                    annotation_vgg["shape_attributes"]["cx"],
                    annotation_vgg["shape_attributes"]["cy"],
                )
                r = annotation_vgg["shape_attributes"]["r"]
                json_object = ellipse2json(cx, cy, r)
            elif vgg_type == "ellipse":
                cx, cy = (
                    annotation_vgg["shape_attributes"]["cx"],
                    annotation_vgg["shape_attributes"]["cy"],
                )
                rx, ry = (
                    annotation_vgg["shape_attributes"]["rx"],
                    annotation_vgg["shape_attributes"]["ry"],
                )
                alpha = annotation_vgg["shape_attributes"]["theta"]
                json_object = ellipse2json(cx, cy, rx, ry, alpha)
            result.append(json_object)
        results.append(result)

    return results
