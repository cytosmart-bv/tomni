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
        dict: A JSON object representing a polygon.

    Example::

        # Define a list of points representing a polygon
        polygon_points = [[1, 1], [2, 1], [2, 2], [1, 2]]

        # Convert the list of points to a JSON object
        polygon_json = list_of_points_to_json(polygon_points)

        # Print the resulting JSON object
        polygon_json = {
            'type': 'polygon',
            'points': [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 2, 'y': 2}, {'x': 1, 'y': 2}]
        }


    Note:
        - The input `list_of_points` should be a list or NumPy array where each element is a point represented as [x, y].
        - The resulting JSON object represents a polygon with type 'polygon' and a list of points.

    """
    contours = np.array(list_of_points)
    contours = contours.reshape((1, contours.shape[0], 1, contours.shape[1]))

    json_object = contours2json(contours)[0]
    return json_object
