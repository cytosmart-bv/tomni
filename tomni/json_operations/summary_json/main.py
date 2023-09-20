from typing import List
from copy import deepcopy
import numpy as np

from ...transformers import json2dict
from .. import add_area, add_circularity


def summary_json(
    json_list: List[dict], keyword: str, do_copy: bool = True, rounding: int = 2
) -> tuple:
    """
    Create a summary of a specified keyword variable inside JSON objects.

    Args:
        json_list (List[dict]): A list of JSON objects in standard AxionBio format.
        keyword (str): The keyword for which to create the summary (e.g., 'area').
        do_copy (bool, optional): When True, copies the JSON list and does not modify it. Defaults to True.
        rounding (int, optional): The number of decimals used in the summary. Defaults to 2.

    Raises:
        ValueError: If an unsupported keyword is provided.

    Returns:
        tuple: A tuple containing:
            - Number of objects
            - Total sum of the keyword in objects
            - Mean value of the keyword in objects
            - Maximum value of the keyword in objects
            - Minimum value of the keyword in objects

    Example::

        json_list = [
            {"area": 10},
            {"area": 15},
            {"area": 20},
        ]
        keyword = "area"

        output = summary_json(json_list, keyword)

        result = (3, 45, 15.0, 20, 10)
    """

    if do_copy:
        copy_json_list = deepcopy(json_list)
    else:
        copy_json_list = json_list

    if keyword == "area":
        if not keyword in json_list[0]:
            for json_object in copy_json_list:
                add_area(json_object)
    else:
        raise ValueError(f"summary for {keyword} is not supported")

    keyword_list = json2dict(copy_json_list, [keyword])[keyword]

    return (
        len(keyword_list),  # Number of objects
        round(np.sum(keyword_list), rounding),  # Total sum of objects
        round(np.mean(keyword_list), rounding),  # Mean of objects
        round(np.max(keyword_list), rounding),  # Max of objects
        round(np.min(keyword_list), rounding),  # Min of objects
    )
