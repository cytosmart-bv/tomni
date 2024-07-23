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
        newjson_object["center"] = flip_coordinates(json_object["center"], img_dim)

    elif json_object["type"] == "polygon":
        newjson_object["points"] = [
            flip_coordinates(point, img_dim) for point in json_object["points"]
        ]

        if "inner_points" in json_object:
            newjson_object["inner_points"] = [
                [
                    flip_coordinates(inner_point, img_dim)
                    for inner_point in inner_contour
                ]
                for inner_contour in json_object["inner_points"]
            ]

    else:
        raise ValueError(
            f"The type '{json_object['type']}' is not supported for flipping augmentation."
        )

    return newjson_object


def flip_coordinates(coordinates: dict, img_dim: int) -> dict:
    """
    Flip a dictionary representing 2D coordinates over the y-axis.

    Args:
        coordinates (dict): A dictionary representing 2D coordinates with 'x' and 'y' keys.
        img_dim (int): The y-dimension of the image.

    Returns:
        dict: A new dictionary with coordinates flipped over the y-axis.
    """
    return {"x": coordinates["x"], "y": img_dim - coordinates["y"] - 1}
