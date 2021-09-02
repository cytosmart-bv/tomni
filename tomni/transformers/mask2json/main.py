import cv2
import numpy as np

from ..contours2json import contours2json
from ..labels2contours import labels2contours


def get_edges(mask: np.ndarray):
    """ get edges of the mask"""
    mask_copy = cv2.copyMakeBorder(
        mask,
        top=1,
        bottom=1,
        left=1,
        right=1,
        borderType=cv2.BORDER_CONSTANT,
        value=0,
    )
    edges = cv2.Canny(mask_copy, 50, 150)

    edges = cv2.dilate(edges, np.ones((5, 5)))

    edges = np.divide(edges, 255, dtype=np.float16)
    edges = edges.astype(np.uint8)
    edges = edges[1:-1, 1:-1]

    return edges


def mask2json(
    mask: np.ndarray, minimum_size_contours: int = 3, is_diagonal_connected=True
) -> list:
    """
    Converts binary mask to standard cytosmart format

    Args:
        mask (np.ndarray): binary mask
        minimum_size_contours (int, optional): The minimum number of points an contour should have to be included. Defaults to 3.
        is_diagonal_connected (bool, optional): If true diagonal pixels [[1, 0][0,1]] will be seen as the same object. Defaults to True.

    Returns:
        list: json_objects, e.g [{'type':'polygon', 'points':[{'x':1,'y':4},{'x':2,'y':3},{'x':4,'y':4} ]
    """
    connectivity = 4
    if is_diagonal_connected:
        connectivity = 8

    labels = cv2.connectedComponents(mask.astype(np.uint8), connectivity=connectivity)[
        1
    ]
    edges = get_edges(mask)

    edges = edges * labels
    del labels
    contours = labels2contours(edges)
    json_objects = contours2json(contours)
    json_objects = [
        json_object
        for i, json_object in enumerate(json_objects)
        if len(json_objects[i]["points"]) >= minimum_size_contours
    ]

    return json_objects
