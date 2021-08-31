import cv2
import numpy as np

from tomni.transformers.contours2json import contours2json
from tomni.transformers.labels2contours import labels2contours


def mask2json(mask: np.ndarray):
    labels = cv2.connectedComponents(mask.astype(np.uint8))[1]
    contours = labels2contours(labels)
    json_objects = contours2json(contours)

    return json_objects
