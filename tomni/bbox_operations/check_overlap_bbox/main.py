def check_overlap_bbox(bb1, bb2):
    if len(bb1) > 4 or len(bb2) > 4:
        raise TypeError("The bounding boxes must be arrays of 4 points.")
    if (bb1[0] >= bb2[1]) or (bb2[0] >= bb1[1]):
        return False
    elif (bb1[2] >= bb2[3]) or (bb1[3] <= bb2[2]):
        return False
    else:
        return True