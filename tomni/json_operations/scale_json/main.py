def scale_json(json_object: dict, scaling_factor: float):
    """
    Takes in a json object (ellipse or polygon) and makes it scaling_factor bigger
    json_object: (dict) following the standard format
    scaling_factor: (float) the multiplier of the object

    example:
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
        newjson_object["center"]["x"] = int(
            round(json_object["center"]["x"] * scaling_factor)
        )
        newjson_object["center"]["y"] = int(
            round(json_object["center"]["y"] * scaling_factor)
        )

    elif json_object["type"] == "polygon":
        all_points = []
        for point in json_object["points"]:
            all_points.append(
                {
                    "x": int(round(point["x"] * scaling_factor)),
                    "y": int(round(point["y"] * scaling_factor)),
                }
            )
        newjson_object["points"] = all_points
    else:
        raise ValueError(f"type {json_object['type']} is not supported")

    return newjson_object

