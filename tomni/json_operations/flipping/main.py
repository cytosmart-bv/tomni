import copy


def flip_json(json_object: dict, img_dim: int) -> dict:
    """
    Flip a JSON object over the y-axis.

    Args:
        json_object (dict): JSON object following the standard AxionBio format (ellipse or polygon).
        img_dim (int): The y-dimension of the image related to the JSON object.

    Raises:
        ValueError: If the JSON object type is not "ellipse" or "polygon".

    Returns:
        dict: A new JSON object with coordinates flipped over the y-axis.
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
