import numpy as np
import cv2


def positions2contour(
    positions: np.ndarray,
    simplify_error: float = 0,
    return_inner_contours: bool = False,
) -> np.ndarray:
    """Transforms a list of positions to opencv contour format

    Args:
        positions (np.ndarray): 2 dimensional array with shape [N, 2].
            For the N pixels of the shape given as x, y
        simplify_error ⚠️ (float, optional): Deprecated!!
        return_inner_contours (bool, optional): return the internal contours.
            These contours are around the holes with the contour
            default: False

    Raises:
        DeprecationWarning: simplification is no longer supported

    Returns:
        np.ndarray: Opencv contour
    """
    if simplify_error > 0:
        raise DeprecationWarning("As of Tomni 1.10 simplify is no longer supported")

    max_x = np.max(positions[:, 0])
    min_x = np.min(positions[:, 0])
    max_y = np.max(positions[:, 1])
    min_y = np.min(positions[:, 1])

    positions -= np.array([min_x, min_y])
    transposed_positions = positions.transpose()

    array_mask = np.zeros((max_y + 1 - min_y, max_x + 1 - min_x), dtype="uint8")
    array_mask[transposed_positions[1], transposed_positions[0]] = 255

    # Chose between RETR_CCOMP to retrieve all of the contours and organizes them into a two-level hierarchy
    # Or RETR_EXTERNAL retrieves only the extreme outer contours
    mode = cv2.RETR_CCOMP if return_inner_contours else cv2.RETR_EXTERNAL
    contours = cv2.findContours(array_mask, mode, cv2.CHAIN_APPROX_SIMPLE)[0]

    external_contour = contours[0] + [min_x, min_y]

    if not return_inner_contours:
        return external_contour

    if len(contours) == 1:
        internal_contours = []
    else:
        internal_contours = [i + [min_x, min_y] for i in contours[1:]]

    return external_contour, internal_contours
