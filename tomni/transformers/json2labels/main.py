import cv2
import numpy as np
from typing import List


def json2labels(json_list: List[dict], output_dim: tuple) -> np.ndarray:
    """
    Converts a json file with objects to a segmentation map.
    Here every object will have a unique number

    json_list: (list[dict]) a list of objects in the json format
    output_dim: (tulpe (2,)) The dimensions of the output image.
        Given in image coordinates
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
