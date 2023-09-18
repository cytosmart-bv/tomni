from typing import List


def json2dict(
    json_list: List[dict], keywords: list = ["type", "area", "center", "id"]
) -> dict:
    """
    Transform a list of JSON objects in standard AxionBio format into a dictionary
    using a list of specified keywords. The resulting dictionary contains lists of values
    extracted from the JSON objects for each keyword, as well as an "index" list with object indexes.

    Args:
        json_list (List[dict]): A list of JSON objects in standard AxionBio format.
        keywords (List[str], optional): A list of keywords to extract from the JSON objects.
            Defaults to ["type", "area", "center", "id"].

    Returns:
        Dict[str, list]: A dictionary containing lists of values for each keyword extracted
            from the JSON objects, including an "index" list with object indexes.
    """

    keywords.append("index")
    json_dict = {}

    for key in keywords:
        json_dict[key] = []

    for i, json_object in enumerate(json_list):
        for key in keywords:
            if key == "index":
                json_dict[key].append(i)
            elif key not in json_object.keys() and key != "index":
                json_dict[key].append(None)
            else:
                if isinstance(json_object[key], dict):
                    variable = [json_object[key][x] for x in json_object[key].keys()]
                else:
                    variable = json_object[key]
                json_dict[key].append(variable)

    return json_dict
