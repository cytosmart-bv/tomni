from typing import Union
import numpy as np
from ..contours2json import contours2json


def list_of_points2json(list_of_points: Union[list, np.array]) -> dict:
    ''''
    From a list of points in the form of [[x1, y1], [x2, y2], ... ,[xn, yn]] a json is made

    list_of_points: (list or numpy array) the list of points that discripe a polygon.
        In the form of [[x1, y1], [x2, y2], ... ,[xn, yn]].
    '''
    contours = np.array(list_of_points)
    contours = contours.reshape((
        1,
        contours.shape[0],
        1,
        contours.shape[1]
    ))

    json_object = contours2json(contours)[0]
    return json_object