from .positions2contour import positions2contour
from ..labels2listsOfPoints import labels2listsOfPoints
import numpy as np


def labels2contours(labels: np.ndarray, simplify_error: float = 0) -> list:
    '''
    Transforms an image with labels into opencv contours

    labels: (numpy.array) An array where every pixels is label to which object it belongs
    simplify_error: (float) the amount of error allowed well simplifying the contours
    '''
    listPoints = labels2listsOfPoints(labels)
    contours = [
        positions2contour(p, simplify_error=simplify_error)
        for p in listPoints
        if len(p) > 0
    ]
    return contours
