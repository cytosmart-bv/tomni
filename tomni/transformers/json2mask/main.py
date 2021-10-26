import numpy as np

from ... import img_dim
from ...make_mask import make_mask_contour, make_mask_ellipse
from ..json2contours import json2contours


def contour2mask(mask: np.ndarray, contour: list) -> np.ndarray:
    """Converts contour to mask"""
    add_mask = make_mask_contour(img_dim(mask), contour)
    mask = mask + add_mask
    mask[mask > 1] = 1
    return mask


def ellipse2mask(mask: np.ndarray, x: int, y: int, r1: float, r2: float) -> np.ndarray:
    """Converts ellipse to mask"""
    add_mask = make_mask_ellipse(img_dim(mask), x, y, r1, r2)
    mask = mask + add_mask
    mask[mask > 1] = 1
    return mask


def json2mask(
    json_objects: list, img_shape: tuple, minimum_size_contours: int = 3
) -> np.ndarray:
    """
    Convert standard cytosmart format to binary mask
    WARNING(1): objects with less than 3 components will get filtered out as default.
    Put minimum_size_contours to 0 if you want them included.
    WARNING(2): small objects will get some extra pixels when it has certain angles
    e.g json_object:

            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 3, "y": 4},
                    {"x": 4, "y": 2},
                ],
            }

        expected result:

            [[0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 1 1 1 0 0 0 0 0]
            [0 0 0 1 0 0 0 0 0 0]
            [0 0 0 1 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]]

        result:

            [[0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 1 1 1 0 0 0 0 0]
            [0 0 1 1 0 0 0 0 0 0]
            [0 0 0 1 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]
            [0 0 0 0 0 0 0 0 0 0]]

    This is a bug that should be removed in the future

    Args:
        json_objects (list): json with annotations in standard cytosmart format
        img_shape (tuple): the dimensions of the mask
        minimum_size_contours (int): The minimum number of points an contour should have to be included. Defaults to 3.

    Returns:
        np.ndarray: binary mask
    """
    mask = np.zeros(img_shape, dtype=np.uint8)
    for json_object in json_objects:
        if json_object["type"] == "polygon":
            if len(json_object["points"]) >= minimum_size_contours:

                contour = json2contours(json_object)
                contour = [x[0] for x in contour]
                mask = contour2mask(mask, contour)
        elif json_object["type"] == "ellipse":
            x = json_object["center"]["x"]
            y = json_object["center"]["y"]
            r1 = json_object["radiusX"]
            r2 = json_object["radiusY"]
            mask = ellipse2mask(mask, x, y, r1, r2)
        else:
            raise TypeError(
                f"json object {json_object['type']} could not be converted to a mask"
            )

    return mask
