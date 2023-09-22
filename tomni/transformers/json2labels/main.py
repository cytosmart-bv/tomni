import cv2
import numpy as np
from typing import List


def json2labels(json_list: List[dict], output_dim: tuple) -> np.ndarray:
    """
    Convert a list of JSON objects representing objects to a labeled segmentation map.

    Args:
        json_list (list of dict): A list of objects in JSON format, each describing an object to be labeled.
        output_dim (tuple of int): The dimensions of the output image in image coordinates, specified as (width, height).

    Returns:
        np.ndarray: A segmentation map where each object has a unique label.

    Raises:
        ValueError: If an unsupported object type is encountered in the JSON list.
    """

    seg_map = np.zeros((output_dim[1], output_dim[0]), dtype=np.uint8)

    for i, obj in enumerate(json_list):
        if obj["type"] == "ellipse":
            cv2.ellipse(
                seg_map,
                (obj["center"]["x"], obj["center"]["y"]),
                (obj["radiusX"], obj["radiusY"]),
                obj["angleOfRotation"],
                0,
                360,
                color=i + 1,
                thickness=-1,
            )
        elif obj["type"] == "polygon":
            points = np.empty((len(obj["points"]), 2))
            for j in range(len(obj["points"])):
                points[j,] = [obj["points"][j]["x"], obj["points"][j]["y"]]
            cv2.fillConvexPoly(seg_map, np.int32([points]), i + 1)
        else:
            raise ValueError("Object type not supported")

    return seg_map
