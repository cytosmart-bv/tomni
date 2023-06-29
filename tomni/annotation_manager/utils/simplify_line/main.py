from typing import List

from tomni.annotation_manager.annotations.point import Point


def simplify_line(line: List[Point], is_enclosed=True):
    if is_enclosed == False:
        raise NotImplemented()

    # returns empty list if `line` has exactly two elements
    if len(line) == 2:
        return line

    filtered_points = []

    # Remove point that do no add new information
    for i in range(len(line)):
        prev_p = line[i - 1]
        cur_p = line[i]
        next_p = line[i + 1] if (i + 1) < len(line) else line[0]

        """
        If ratio heigh width for prev-cur and cur-next is the same.
        The point is on a straight line
        Comparing is done with division for optimization
        """
        prev_cur_width = prev_p.x - cur_p.x
        prev_cur_height = prev_p.y - cur_p.y
        cur_next_width = cur_p.x - next_p.x
        cur_next_height = cur_p.y - next_p.y

        if prev_cur_width * cur_next_height == prev_cur_height * cur_next_width:
            continue

        filtered_points.append(cur_p)

    return filtered_points
