

def translation_json(json_object: dict, x_translation: int, y_translation: int):
    """
    Takes in a json object (ellipse or polygon) and translates it
    json_object: (dict) following the standard format
    x_translation: (int) The translation in the x-direction
    y_translation: (int) The translation in the y-direction

    example:
    json_object = {
        "type": "ellipse", 
        "center": {"x": 100, "y": 200}, 
        "radiusX": 50, 
        "radiusY": 100, 
        "angleOfRotation": 0, 
        "id": "12345-abcde"}
    x_translation = 100
    y_translation = -20

    result = {
        "type": "ellipse", 
        "center": {"x": 200, "y": 180}, 
        "radiusX": 50, 
        "radiusY": 100, 
        "angleOfRotation": 0, 
        "id": "12345-abcde"}

    """
    newjson_object = json_object.copy()
    if json_object["type"] == "ellipse":
        newjson_object["center"]["x"] = int(
            round(json_object["center"]["x"] + x_translation)
        )
        newjson_object["center"]["y"] = int(
            round(json_object["center"]["y"] + y_translation)
        )

    elif json_object["type"] == "polygon":
        all_points = []
        for point in json_object["points"]:
            all_points.append(
                {
                    "x": int(round(point["x"] + x_translation)),
                    "y": int(round(point["y"] + y_translation)),
                }
            )
        newjson_object["points"] = all_points
    else:
        raise ValueError(f"type {json_object['type']} is not supported")

    return newjson_object

