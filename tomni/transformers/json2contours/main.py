import numpy as np


def json2contours(json: dict) -> np.ndarray:
    '''
    Set a default json format object to a contour.
    json: (dict) the objects needs:
        'points': (if polygon) list of dict of form {x: ..., y: ...}
        'type': needs to be polygon 
    '''
    if json.get('type', '').lower() == 'polygon':
        result = [[[i["x"], i["y"]]] for i in json["points"]]
    else:
        raise ValueError(f"The type {json.get('type', 'NO TYPE GIVEN')} is not supported")
    return np.array(result, dtype=np.int32)
