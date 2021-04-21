from typing import List


def json2dict(
    json_list: List[dict], keywords: list = ["type", "area", "center", "id"]
) -> dict:
    """Transforms a list of standard CytoSMART format jsons to a dict using a list of given keywords.
       This dict contains list of each keyword extracted from the json objects and a list with indexes.
       e.g json_dict{"area": [100, 33,44], 'type': ["ellipse", "polygon", "ellipse"], "index":[0,1,2]}

    Args:
        json_list (List[dict]):the jsons are in the standard CytoSMART format.
        keywords (list, optional): a list with keywords you want to extract from the json_objects.
                Defaults to ["type", "area", "center", "id"].

    Returns:
        dict: a dict containing list of each keyword extracted from the json objects
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