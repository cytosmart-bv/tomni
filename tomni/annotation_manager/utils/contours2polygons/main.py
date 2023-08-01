import cv2
import numpy as np

from typing import List, Union
from tomni.annotation_manager.annotations import Polygon, Point
import uuid

MIN_NR_POINTS_POLYGON = 5


def contours2polygons(
    contours: List[np.ndarray],
    include_inner_contours: bool = False,
    hierarchy: Union[np.ndarray, None] = None,
    label: str = "",
) -> List[Polygon]:
    """transforms contours from cv2 contours to Polygon objects.
    Contours' shape must be [N, 1, 2] with dtype of np.int32.

    Args:
        contours (List[np.ndarray]): Collection of cv2 contours.
        include_inner_contours (bool, optional): whether to return inner contours.
        hierarchy (bool, optional): the hierarchy from cv2.findContours using the RETR_CCOMP mode.
            Defaults to None.
            !!!!!Currently, only the hierarchy returned by mode: RETR_CCOMP is supported!!!!!
            If none, no hierarchy will be used.
        label(str, optional): The label of the polygon. Defaults to "".
    Returns:
        List[np.ndarray]: A list of Polygon objects.
    """
    annotations = []
    # Check whether inner contours are present
    if include_inner_contours:
        if hierarchy is None:
            raise ValueError(
                "hierarchy must be provided if include_inner_contours is True"
            )
        # Iterate over all contours and their hierarchies
        for idx, contour in enumerate(contours):
            current_hierarchy = hierarchy[0][idx]
            if current_hierarchy[-1] == -1:
                # If the contour has no parent, it is an outer contour
                if len(contour) < MIN_NR_POINTS_POLYGON:
                    continue

                # change shape from [N, 1, 2] to [N, 2]
                contour = np.vstack(contour)
                outer_points = [Point(x=int(pt[0]), y=int(pt[1])) for pt in contour]

                # Find the indices of the inner contours
                inner_indices = [i for i, h in enumerate(hierarchy[0]) if h[3] == idx]
                # Add the corresponding inner contours
                inner_contours = [contours[inner_idx] for inner_idx in inner_indices]
                inner_contours = [
                    np.vstack(inner_contour) for inner_contour in inner_contours
                ]
                list_of_inner_points = [
                    [
                        Point(x=int(pt[0]), y=int(pt[1]))
                        for pt in inner_contour.reshape(-1, 2)
                    ]
                    for inner_contour in inner_contours
                ]

                annotations.append(
                    Polygon(
                        label=label,
                        id=str(uuid.uuid4()),
                        children=[],
                        parents=[],
                        points=outer_points,
                        inner_points=list_of_inner_points,
                    ),
                )
    elif not include_inner_contours:
        for contour in contours:
            if len(contour) < MIN_NR_POINTS_POLYGON:
                continue
            contour = np.vstack(contour)
            points = [Point(x=int(pt[0]), y=int(pt[1])) for pt in contour]

            annotations.append(
                Polygon(
                    label=label,
                    id=str(uuid.uuid4()),
                    children=[],
                    parents=[],
                    points=points,
                    inner_points=[],
                ),
            )
    return annotations
