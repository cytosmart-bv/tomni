AxionBio JSON format
=========================

Example JSON containing Ellipse and Polygon annotations::

    JSON = [
        {
            "label" : "cell",
            "id": "13468814-15b8-4417-a6cb-322c48a51ec4",
            "type": "ellipse",
            "center": {"x": 500, "y": 500},
            "radiusX": 500,
            "radiusY": 500,
            "angleOfRotation": 0,
            "name": "A1",
        },
        {
        "label": "organoid,
        "children": [],
        "parents": [],
        "type": "polygon",
        "points": [
                {
                    "x": 2127.0,
                    "y": 1351.0
                },
                {
                    "x": 2092.0,
                    "y": 1359.0
                },
                {
                    "x": 2083.0,
                    "y": 1370.0
                },
                {
                    "x": 2083.0,
                    "y": 1370.0
                },
                {
                    "x": 2083.0,
                    "y": 1370.0
                }
            ],
            "inner_points": []
        },
    ]