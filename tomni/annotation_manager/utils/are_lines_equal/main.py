from typing import List

from tomni.annotation_manager.annotations.point import Point


def are_lines_equal(l1: List[Point], l2: List[Point], is_enclosed: bool = True):
    if is_enclosed == False:
        raise NotImplemented()

    if len(l1) != len(l2):
        return False

    # Find the first element in l2 that is the same as l1[0]
    # This is the start of the comparing
    start_l2 = 0
    for i in range(len(l1)):
        if l1[0] == l2[i]:
            start_l2 = i
            break

    # sliced_l2 and l1 have the same starting point
    sliced_l2 = l2[start_l2:] + l2[:start_l2]
    print(sliced_l2)

    for i in range(len(l1)):
        if l1[i] != sliced_l2[i]:
            return False

    return True
