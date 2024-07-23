import uuid
import numpy as np
from typing import List, Union


def contours2json(contours: Union[np.ndarray, List[list]]) -> List[dict]:
    """
    Convert a list or array of contours into a list of JSON objects in standard AxionBio format.

    Args:
        contours (numpy.ndarray or list): Contours produced by OpenCV, represented as a NumPy array or a list.

    Returns:
        List[dict]: A list of JSON objects, where each JSON object represents a contour as a polygon.

    """
    result = []
    for contour in contours:
        shape = {"type": "polygon", "points": []}
        for point in contour:
            shape["points"].append(dict(x=int(point[0][0]), y=int(point[0][1])))
        shape["id"] = str(uuid.uuid4())
        shape["parents"] = []
        shape["children"] = []
        result.append(shape)
    return result
