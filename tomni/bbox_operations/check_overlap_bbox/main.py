from typing import Union


def check_overlap_bbox(bb1: Union[tuple, list], bb2: Union[tuple, list]) -> bool:

    """
    Checks if two bounding boxes overlap with eachother.
    The bounding boxes are assumed the be structured as follows:
    (xmin, ymin, xmax, ymax).
    Warning: Touching bounding boxes are not seen as overlapping

    Args:
        bb1 (Union[tuple, list]): boundingbox 1, (x1, y1, x2 ,y2)
        bb2 (Union[tuple, list]): boundingbox 2, (x1, y1, x2 ,y2)

    Raises:
        ValueError: Length of bounding box is the wrong size

    Returns:
        bool: if the bounding boxes are touching
    """
    if len(bb1) != 4 or len(bb2) != 4:
        raise ValueError("The bounding boxes must be tuples or list of length 4")

    if (bb1[0] >= bb2[2]) or (bb2[0] >= bb1[2]):
        return False
    elif (bb1[1] >= bb2[3]) or (bb2[1] >= bb1[3]):
        return False
    else:
        return True