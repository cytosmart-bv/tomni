def translation_json(json_object: dict, x_translation: int, y_translation: int):
    """
    Translate a JSON object (ellipse or polygon) by specified amounts in the x and y directions.

    Args:
        json_object (dict): A JSON object following the standard format.
        x_translation (int): The translation in the x-direction.
        y_translation (int): The translation in the y-direction.

    Raises:
        ValueError: If the JSON object type is not supported.

    Returns:
        dict: A translated JSON object.

    Example::

        json_object = {
            "type": "ellipse",
            "center": {"x": 100, "y": 200},
            "radiusX": 50,
            "radiusY": 100,
            "angleOfRotation": 0,
            "id": "12345-abcde"
        }
        x_translation = 100
        y_translation = -20

        result = {
            "type": "ellipse",
            "center": {"x": 200, "y": 180},
            "radiusX": 50,
            "radiusY": 100,
            "angleOfRotation": 0,
            "id": "12345-abcde"
        }
    """
    newjson_object = json_object.copy()
    if json_object["type"] == "ellipse":
        newjson_object["center"] = translate_coordinates(
            json_object["center"], x_translation, y_translation
        )
    elif json_object["type"] == "polygon":
        newjson_object["points"] = [
            translate_coordinates(point, x_translation, y_translation)
            for point in json_object["points"]
        ]
        if "inner_points" in json_object:
            newjson_object["inner_points"] = [
                [
                    translate_coordinates(point, x_translation, y_translation)
                    for point in inner_points
                ]
                for inner_points in json_object["inner_points"]
            ]
    else:
        raise ValueError(f"type {json_object['type']} is not supported")

    return newjson_object


def translate_coordinates(point: dict, x_translation: int, y_translation: int) -> dict:
    """Translate 2D coordinates by adding specified translations.

    Args:
        point (dict): A dictionary representing 2D coordinates with 'x' and 'y' keys.
        x_translation (int): The amount to translate in the x-axis.
        y_translation (int): The amount to translate in the y-axis.

    Returns:
        dict: A new dictionary with translated coordinates.
    """
    return {
        "x": int(round(point["x"] + x_translation)),
        "y": int(round(point["y"] + y_translation)),
    }
