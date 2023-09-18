from typing import Union
import numpy as np
from ..contours2json import contours2json


def list_of_points2json(list_of_points: Union[list, np.array]) -> dict:
    """
    Convert a list of points into a JSON object representing a polygon.

    Args:
        list_of_points (Union[list, np.ndarray]): The list of points describing a polygon in the form of
            a list or NumPy array, where each point is represented as [x, y].

    Returns:
        dict: A JSON object representing a polygon with the following structure:
            {
                'type': 'polygon',
                'points': [{'x': x1, 'y': y1}, {'x': x2, 'y': y2}, ..., {'x': xn, 'y': yn}]
            }
    """
    contours = np.array(list_of_points)
    contours = contours.reshape((1, contours.shape[0], 1, contours.shape[1]))

    json_object = contours2json(contours)[0]
    return json_object
