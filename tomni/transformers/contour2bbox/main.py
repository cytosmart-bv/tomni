import cv2
import numpy as np


def contour2bbox(contour: np.ndarray) -> tuple:
    box_points_array = cv2.boundingRect(contour)
    x_min, y_min, w, h = box_points_array
    x_max = x_min + w - 1
    y_max = y_min + h - 1
    box_points = x_min, x_max, y_min, y_max
    return box_points
