import numpy as np

from ..labels2listsOfPoints import labels2listsOfPoints
from ..positions2contour import positions2contour


def labels2contours(
    labels: np.ndarray, simplify_error: float = 0, return_inner_contours: bool = False
) -> list:
    """
    Transforms an image with labels into opencv contours

    labels: (numpy.array) An array where every pixels is label to which object it belongs
    simplify_error ⚠️: (float) DEPRECATED the amount of error allowed well simplifying the contours
    return_inner_contours (bool, optional): return the internal contours.
            These contours are around the holes with the contour
            default: False

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
