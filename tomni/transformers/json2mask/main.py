import numpy as np

from ...img_dim import img_dim
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
    Convert a list of JSON objects in standard AxionBio format to a binary mask.

    Args:
        json_objects (list): A list of JSON objects with annotations in the standard AxionBio format.
        img_shape (tuple): The dimensions (height, width) of the mask.
        minimum_size_contours (int, optional): The minimum number of points a contour should have to be included.
            Defaults to 3. Set to 0 to include all contours regardless of size.

    Returns:
        np.ndarray: A binary mask as a NumPy array.

    Raises:
        TypeError: If a JSON object of an unsupported type is encountered.

    Example::

        json_objects = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 0},
                    {"x": 0, "y": 5},
                    {"x": 5, "y": 5},
                    {"x": 5, "y": 0},
                ],
            }
        ]
        img_shape = (10, 10)
        minimum_size_contours = 3
        result = json2mask(json_objects, img_shape, minimum_size_contours)
        print(result)
        [[1 1 1 1 1 0 0 0 0 0]
         [1 1 1 1 1 0 0 0 0 0]
         [1 1 1 1 1 0 0 0 0 0]
         [1 1 1 1 1 0 0 0 0 0]
         [1 1 1 1 1 0 0 0 0 0]
         [0 0 0 0 0 0 0 0 0 0]
         [0 0 0 0 0 0 0 0 0 0]
         [0 0 0 0 0 0 0 0 0 0]
         [0 0 0 0 0 0 0 0 0 0]
         [0 0 0 0 0 0 0 0 0 0]]
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
