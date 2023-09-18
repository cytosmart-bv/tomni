import cv2
import numpy as np

from typing import List


def binary2contours(
    binary_img: np.ndarray, return_inner_contours: bool = True
) -> List[np.ndarray]:
    """
    Convert a binary image to a list of outer contours and their corresponding inner contours
    if 'return_inner_contours' is True. If 'return_inner_contours' is False, only outer contours
    are returned.

    Args:
        binary_img (np.ndarray): A binary image.
        return_inner_contours (bool): boolean to check if inner contours are desired. Defaults to True.

    Returns:
        List[np.ndarray]: A list of outer contours with their corresponding inner contours.
    """

    mode = cv2.RETR_CCOMP if return_inner_contours else cv2.RETR_EXTERNAL

    contours, hierarchy = cv2.findContours(binary_img, mode, cv2.CHAIN_APPROX_SIMPLE)

    if not return_inner_contours:
        return contours

    combined_contours = []
    # Iterate over all contours and their hierarchies
    for idx, contour in enumerate(contours):
        current_hierarchy = hierarchy[0][idx]

        if current_hierarchy[-1] == -1:
            # If the contour has no parent, it is an outer contour
            combined_contour = [contour]
            inner_contours = []
            # Find the indices of the inner contours
            inner_indices = [i for i, h in enumerate(hierarchy[0]) if h[3] == idx]

            # Add the corresponding inner contours
            for inner_idx in inner_indices:
                inner_contours.append(contours[inner_idx])

            combined_contour.append(inner_contours)
            combined_contours.append(combined_contour)

    return combined_contours
