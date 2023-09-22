import cv2
import numpy as np

from ..contours2json import contours2json
from ..labels2contours import labels2contours


def get_edges(mask: np.ndarray):
    """
    Extracts and returns the edges of a binary mask image.

    This function uses the Canny edge detection algorithm to identify edges in the input binary mask image.

    Args:
        mask (np.ndarray): A binary mask represented as a NumPy array, where 1 indicates the object of interest,
            and 0 indicates the background.

    Returns:
        np.ndarray: A binary image representing the edges of the input mask. Pixels along edges are set to 1,
            while non-edge pixels are set to 0.
    """
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
    mask: np.ndarray,
    minimum_size_contours: int = 3,
    is_diagonal_connected=True,
    return_inner_contours: bool = False,
) -> list:
    """
    Converts a binary mask into a list of JSON objects representing contours.

    Args:
        mask (np.ndarray): A binary mask represented as a NumPy array.
        minimum_size_contours (int, optional): The minimum number of points a contour should have to be included.
            Contours with fewer points will be excluded. Defaults to 3.
        is_diagonal_connected (bool, optional): If True, diagonal pixels (e.g., [[1, 0], [0, 1]]) will be considered
            part of the same object during contour extraction. Defaults to True.
        return_inner_contours (bool, optional): If True, include internal contours (holes within the shape).
            If False, only return the external contours (outlines of the shapes). Defaults to False.

    Returns:
        list: A list of JSON objects representing contours in the mask.

    Example output::

            {
                'type': 'polygon',
                'points': [{'x': x1, 'y': y1}, {'x': x2, 'y': y2}, ...],
                'innerObjects': [
                    {
                        'type': 'polygon',
                        'points': [{'x': x3, 'y': y3}, {'x': x4, 'y': y4}, ...],
                    },
                ],
            }
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
    contours = labels2contours(edges, return_inner_contours=return_inner_contours)

    if return_inner_contours:
        json_objects = []
        for contour in contours:
            json_object = contours2json([contour[0]])[0]
            json_object["innerObjects"] = contours2json(contour[1])
            json_objects.append(json_object)
    else:
        json_objects = contours2json(contours)
    json_objects = [
        json_object
        for i, json_object in enumerate(json_objects)
        if len(json_objects[i]["points"]) >= minimum_size_contours
    ]

    return json_objects
