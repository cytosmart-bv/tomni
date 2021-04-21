from typing import List
from copy import deepcopy
import numpy as np

from ...transformers import json2dict
from .. import add_area, add_circularity


def summary_json(
    json_list: List[dict], keyword: str, do_copy: bool = True, rounding: int = 2
) -> tuple:
    """Makes a summary of the keyword variable inside of the json objects. Function works
       for the keyword 'area'. The summary consists of the number of objects,
       the total sum of keyword in json_list, the mean, maximum and average keyword in json_list.

    Args:
        json_list (List[dict]): a list of jsons in standard cytosmart forma
        keyword (str): 'area'
        do_copy (bool, optional): When true copies the json_list and does not change it.
                Defaults to True.
        rounding (int, optional): the number of decimals are used in the summary. Defaults to 2.

    Raises:
        ValueError: If a keyword is used that is not supported

    Returns:
        tuple: (Number of objects, Total sum of objects, Mean of objects, Max of objects, Min of objects)
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
