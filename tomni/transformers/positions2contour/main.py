import numpy as np
import cv2


def positions2contour(
    positions: np.ndarray,
    simplify_error: float = 0,
    return_inner_contours: bool = False,
) -> np.ndarray:
    """
    Transform a list of positions into an OpenCV contour format.

    Args:
        positions (np.ndarray): A 2-dimensional array with shape [N, 2], representing the x and y coordinates
            of N pixels in the shape.
        simplify_error (float, optional): ⚠️ Deprecated parameter. No longer used.
        return_inner_contours (bool, optional): If True, return the internal contours (holes within the shape).
            If False (default), return only the external contour (the outline of the shape).

    Raises:
        DeprecationWarning: The `simplify_error` parameter is deprecated and no longer supported.

    Returns:
        Union[np.ndarray, Tuple[np.ndarray, List[np.ndarray]]]: If `return_inner_contours` is False, returns the
        external contour as an OpenCV-style np.ndarray.
        If `return_inner_contours` is True and there are internal contours, returns a tuple containing the
        external contour as the first element and a list of internal contours as the second element.
        Each contour is represented as an np.ndarray of shape [M, 2], where M is the number of points in the contour.

    Note:
        - The `simplify_error` parameter has been deprecated and is no longer used. Please update your code accordingly.
        - The input `positions` should be a 2D array with two columns, where each row represents the (x, y) coordinates
          of a pixel in the shape.
        - The `return_inner_contours` parameter controls whether internal contours (holes within the shape) are included.
          If set to True, both external and internal contours are returned as a tuple.
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
