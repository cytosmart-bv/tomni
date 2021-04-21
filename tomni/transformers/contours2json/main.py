import uuid
import numpy as np
from typing import List, Union

def contours2json(contours: Union[np.ndarray, List[list]]) -> List[dict]:
    """
    Transforms a list or array of contours into list of jsons
    contours: (numpy.array, list) needs to be the contours produced by opencv
    """ 
    result = []
    for contour in contours:
        shape = {"type": "polygon", "points": []}
        for point in contour:
            shape["points"].append(dict(x = int(point[0][0]), y = int(point[0][1])))
        shape['id'] = str(uuid.uuid4())
        shape['parents'] = []
        shape['children'] = []
        result.append(shape)
    return result