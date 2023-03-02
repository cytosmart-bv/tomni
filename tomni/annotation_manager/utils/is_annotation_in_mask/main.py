import gc

import cv2
import numpy as np

from tomni.annotation_manager.annotations import Annotation, Ellipse, Polygon


def is_annotation_in_mask(
    annotation: Annotation, mask: np.ndarray, min_overlap: 0.9
) -> bool:
    """
    Check if a annotation is within a binary mask.

    Args:
        annotation (list of lists): List of lists containing the vertices of the annotation.
        mask (numpy.ndarray): Binary array of the same shape as the annotation indicating the mask.
        min_overlap (float, optional): Minimum overlap in percent required between the annotation and the mask. Defaults to 0.5.

    Returns:
        bool: True if the annotation is within the masked area with at least the specified overlap, False otherwise.
    """

    annotation_mask = np.zeros_like(mask)

    if isinstance(annotation, Polygon):
        # Convert the polygon to a numpy array of shape (N, 2)
        points = np.array(
            [[point.x, point.y] for point in annotation.points], dtype=np.int32
        )
        annotation_mask = cv2.fillPoly(annotation_mask, [points], color=1)
    elif isinstance(annotation, Ellipse):
        cv2.ellipse(
            annotation_mask,
            center=(annotation.center.x, annotation.center.y),
            axes=(annotation.radius_x, annotation.radius_y),
            angle=annotation.rotation,
            startAngle=0,
            endAngle=360,
            color=1,
            thickness=-1,
        )

    # Calculate the intersection of the annotation and the mask
    intersection = np.logical_and(mask, annotation_mask)
    # Calculate the overlap ratio between the polygon and the mask
    overlap_ratio = intersection.sum() / annotation_mask.sum()

    del annotation_mask
    del intersection
    gc.collect()

    # Check if the polygon is within the masked area with at least the specified overlap
    return overlap_ratio >= min_overlap

