import copy


def flip_json(json_object: dict, img_dim: int) -> dict:
    """
    Takes in a json object (ellipse or polygon, standard CytoSMART format)
    and flips it over the y axis.
    json_object: (dict) following the standard CytoSMART format
    img_dim: (int) the y dimension of the image that is related to the json_object.

    input_json = {
            "type": "ellipse",
            "center": {"x": 9, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

    expected_json = {
        "type": "ellipse",
        "center": {"x": 9, "y": 6},
        "radiusX": 5,
        "radiusY": 5,
        "angleOfRotation": 0,
    }
    """
    newjson_object = copy.deepcopy(json_object)
    if json_object["type"] == "ellipse":
        newjson_object["center"]["y"] = img_dim - json_object["center"]["y"] - 1

    elif json_object["type"] == "polygon":
        for point_n in range(len(newjson_object["points"])):
            newjson_object["points"][point_n]["y"] = (
                img_dim - json_object["points"][point_n]["y"] - 1
            )
    else:
        raise TypeError(
            f"The type {json_object['type']} is not found in flipping augmentation"
        )

    return newjson_object