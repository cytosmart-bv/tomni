import numpy as np
import cv2
from simplification.cutil import simplify_coords

def positions2contour(positions: np.ndarray, simplify_error: float = 0):
    max_x = np.max(positions[:, 0])
    min_x = np.min(positions[:, 0])
    max_y = np.max(positions[:, 1])
    min_y = np.min(positions[:, 1])

    positions -= np.array([min_x, min_y])
    transposed_positions = positions.transpose()
    
    array_mask = np.zeros((max_y + 1 - min_y, max_x + 1 - min_x), dtype="uint8")
    array_mask[transposed_positions[1], transposed_positions[0]] = 255

    contours = cv2.findContours(array_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
        0
    ][0] + [min_x, min_y]

    simple_contours = simplify_coords(contours[:, 0, :], simplify_error)

    contours = simple_contours.reshape([simple_contours.shape[0], 1, simple_contours.shape[1]])
    return contours