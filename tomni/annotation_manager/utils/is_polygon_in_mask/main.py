import gc

import cv2
import numpy as np

from tomni.annotation_manager.annotations import Annotation, Ellipse, Point, Polygon


def get_mask_from_ellipse(ellipse: Ellipse) -> np.ndarray:
    if (
        ellipse.rotation == 0
        and ellipse.radius_x <= ellipse.center.x
        and ellipse.radius_y <= ellipse.center.y
    ):
        # assume the mask fits into image!?
        # calculate im size
        # fill im with masked area
        width = (2 * ellipse.radius_x) + (ellipse.center.x - ellipse.radius_x) + 1
        height = (2 * ellipse.radius_y) + (ellipse.center.y - ellipse.radius_y) + 1
        mask = np.zeros((width, height), dtype=np.uint8)
        cv2.ellipse(
            mask,
            center=(ellipse.center.x, ellipse.center.y),
            axes=(ellipse.radius_x, ellipse.radius_y),
            angle=ellipse.rotation,
            startAngle=0,
            endAngle=360,
            color=1,
            thickness=-1,
        )

    elif ellipse.center.x == ellipse.radius_x:
        print(2)
        # calculate intersection with axis

    else:
        raise ValueError("cry a little and move on")

    return mask


def get_mask_from_polygon(polygon: Polygon) -> np.ndarray:
    width = max(polygon.points, key=lambda point: point.x).x + 1
    height = max(polygon.points, key=lambda point: point.y).y + 1
    mask = np.zeros((width, height), dtype=np.uint8)

    points = np.array([[point.x, point.y] for point in polygon.points], dtype=np.int32)
    cv2.fillPoly(mask, [points], color=1)
    return mask


def is_annotation_in_mask(
    annotation: Annotation, mask: np.ndarray, overlap: 1.0
) -> bool:
    """
    Check if a annotation is within a binary mask.

    Args:
        annotation (list of lists): List of lists containing the vertices of the annotation.
        mask (numpy.ndarray): Binary array of the same shape as the annotation indicating the mask.
        overlap (float, optional): Minimum overlap in percent required between the annotation and the mask. Defaults to 0.5.

    Returns:
        bool: True if the annotation is within the masked area with at least the specified overlap, False otherwise.
    """
    # Create a binary mask image from the annotation
    annotation_mask = np.zeros_like(mask)

    if type(annotation) is Polygon:
        # Convert the polygon to a numpy array of shape (N, 2)
        points = np.array(
            [[point.x, point.y] for point in annotation.points], dtype=np.int32
        )
        annotation_mask = cv2.fillPoly(annotation_mask, [points], color=1)
    elif type(annotation) is Ellipse:
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
    return overlap_ratio >= overlap

