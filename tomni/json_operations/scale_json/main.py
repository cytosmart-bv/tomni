def scale_json(json_object: dict, scaling_factor: float):
    """
    Scale a JSON object (ellipse or polygon) by a specified scaling factor.

    Args:
        json_object (dict): JSON object following the standard format (ellipse or polygon).
        scaling_factor (float): The multiplier to scale the object. A value of 1.0 keeps the object unchanged.

    Returns:
        dict: A new JSON object scaled by the provided factor.

    Raises:
        ValueError: If the JSON object type is not supported.

    Example::

        json_object = {
            "type": "ellipse",
            "center": {"x": 100, "y": 200},
            "radiusX": 50,
            "radiusY": 100,
            "angleOfRotation": 0,
            "id": "12345-abcde"}
        scaling_factor = 2

        result = {
            "type": "ellipse",
            "center": {"x": 200, "y": 400},
            "radiusX": 100,
            "radiusY": 200,
            "angleOfRotation": 0,
            "id": "12345-abcde"}
    """
    newjson_object = json_object.copy()
    if json_object["type"] == "ellipse":
        newjson_object["radiusX"] = int(round(json_object["radiusX"] * scaling_factor))
        newjson_object["radiusY"] = int(round(json_object["radiusY"] * scaling_factor))
        newjson_object["center"] = scale_coordinates(
            json_object["center"], scaling_factor
        )

    elif json_object["type"] == "polygon":
        newjson_object["points"] = [
            scale_coordinates(point, scaling_factor) for point in json_object["points"]
        ]
        if "inner_points" in json_object:
            newjson_object["inner_points"] = [
                [
                    scale_coordinates(inner_point, scaling_factor)
                    for inner_point in inner_points
                ]
                for inner_points in json_object["inner_points"]
            ]
    else:
        raise ValueError(f"type {json_object['type']} is not supported")

    return newjson_object


def scale_coordinates(point: dict, scaling_factor: float) -> dict:
    """Scale a 2D point by a specified scaling factor.

    Args:
        point (dict): A dictionary representing the 2D point with 'x' and 'y' coordinates.
        scaling_factor (float): The multiplier to scale the point.

    Returns:
        dict: A new dictionary representing the scaled 2D point.
    """
    return {
        "x": int(round(point["x"] * scaling_factor)),
        "y": int(round(point["y"] * scaling_factor)),
    }
