from typing import Union


def check_overlap_bbox(bb1: Union[tuple, list], bb2: Union[tuple, list]) -> bool:
    """
    Checks if two bounding boxes overlap with each other. Bounding boxes are represented
    as tuples or lists in the format (xmin, ymin, xmax, ymax).

    Args:
        bb1 (Union[tuple, list]): Bounding box 1, specified as (x1, y1, x2, y2).
        bb2 (Union[tuple, list]): Bounding box 2, specified as (x1, y1, x2, y2).

    Raises:
        ValueError: If the length of either bounding box is not 4.

    Returns:
        bool: True if the bounding boxes overlap, False otherwise.

    Example::

        bb1 = (1, 1, 4, 4)
        bb2 = (3, 3, 6, 6)
        check_overlap_bbox(bb1, bb2)
        True  # The bounding boxes overlap.
    """
    if len(bb1) != 4 or len(bb2) != 4:
        raise ValueError("The bounding boxes must be tuples or list of length 4")

    if (bb1[0] >= bb2[2]) or (bb2[0] >= bb1[2]):
        return False
    elif (bb1[1] >= bb2[3]) or (bb2[1] >= bb1[3]):
        return False
    else:
        return True
