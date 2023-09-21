import numpy as np

from ..labels2listsOfPoints import labels2listsOfPoints
from ..positions2contour import positions2contour


def labels2contours(
    labels: np.ndarray, simplify_error: float = 0, return_inner_contours: bool = False
) -> list:
    """
    Convert a labeled image into a list of OpenCV contours.

    Args:
        labels (np.ndarray): An array where every pixel is labeled to indicate which object it belongs to.
            The labels should be non-negative integers.
        return_inner_contours (bool, optional): If True, return the internal contours (contours around holes within objects).
            If False (default), return only the external contours (outlines of objects).

    Returns:
        List[np.ndarray]: A list of OpenCV-style contours represented as NumPy arrays. Each contour is a 2D array
            with shape (N, 1, 2), where N is the number of points in the contour, and each point has (x, y) coordinates.
            The list contains contours for each labeled object in the input image.

    Warnings:
        - The parameter 'simplify_error' has been deprecated and is no longer used.
          Please update your code to remove references to 'simplify_error'.
    """
    listPoints = labels2listsOfPoints(labels)
    contours = [
        positions2contour(
            p,
            simplify_error=simplify_error,
            return_inner_contours=return_inner_contours,
        )
        for p in listPoints
        if len(p) > 0
    ]
    return contours
