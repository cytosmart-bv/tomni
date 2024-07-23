import numpy as np


def json2contours(json: dict) -> np.ndarray:
    """
    Convert a JSON object in a default AxionBio format to a contour represented as a NumPy array.

    Args:
        json (dict): A JSON object containing 'points' in the form of a list of dictionaries
                     with keys 'x' and 'y', and 'type' set to 'polygon'.

    Returns:
        np.ndarray: A contour represented as a NumPy array.

    Raises:
        ValueError: If the 'type' in the JSON object is not 'polygon' or missing.
    """

    if json.get("type", "").lower() == "polygon":
        result = [[[i["x"], i["y"]]] for i in json["points"]]
    else:
        raise ValueError(
            f"The type {json.get('type', 'NO TYPE GIVEN')} is not supported"
        )
    return np.array(result, dtype=np.int32)
