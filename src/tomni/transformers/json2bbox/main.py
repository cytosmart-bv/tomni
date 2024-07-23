from ...shape_fitting.fit_rect_ellipse import fit_rect_around_ellipse


def json2bbox(scf_object: dict) -> tuple:
    """
    Convert a standard AxionBio format object (polygon, ellipse, or circle) into bounding box coordinates
    (x_min, y_min, x_max, y_max). All bounding box values are rounded using Python's internal 'round' function
    (https://wiki.c2.com/?BankersRounding).

    Args:
        scf_object (Dict[str, any]): A single annotation in standard AxionBio format. Allowed types are polygon, ellipse, or circle.

    Returns:
        Tuple[int, int, int, int]: Bounding box coordinates in the format (x_min, y_min, x_max, y_max).

    Note:
        - The angle of rotation for an ellipse is taken into account.

    Raises:
        ValueError: If the type of the object is not supported.

    Example::

        object = {
            "type": "polygon",
            "points": [{'x': 0, 'y': 0}, {'x': 20, 'y': 0}, {'x': 20, 'y': 30}, {'x': 0, 'y': 30}]
        }
        bbox = json2bbox(object)
        print(bbox)
        (0, 0, 20, 30)

    """

    if "type" in scf_object:
        if scf_object["type"] == "polygon":
            x_values, y_values = [val["x"] for val in scf_object["points"]], [
                val["y"] for val in scf_object["points"]
            ]
            return (
                int(round(min(x_values))),
                int(round(min(y_values))),
                int(round(max(x_values))),
                int(round(max(y_values))),
            )
        elif scf_object["type"] in ["circle", "ellipse"]:
            x1, y1, x2, y2 = fit_rect_around_ellipse(
                scf_object["center"]["x"],
                scf_object["center"]["y"],
                scf_object["radiusX"],
                scf_object["radiusY"],
                scf_object["angleOfRotation"],
            )
            return x1, y1, x2, y2
        else:
            raise ValueError(f"{scf_object['type']} is not a supported type")

    else:
        raise KeyError(
            f"The scf_object does not have the key 'type'. dict is in the wrong format. {scf_object}"
        )
