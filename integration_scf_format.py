import imp
from tomni import SCFJson
scf_json = [{
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 10, "y": 10},
                {"x": 10, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 20, "y": 10},
                {"x": 20, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 30, "y": 10},
                {"x": 30, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 40, "y": 10},
                {"x": 40, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 50, "y": 10},
                {"x": 50, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        },
        {
            "type": "ellipse",
            "center": {"x": 20, "y": 30},
            "radiusX": 10,
            "radiusY": 12,
            "angleOfRotation": 0,
            "id": "unicorn",
        }
        ]

scf_json2 = [{
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 10, "y": 10},
                {"x": 10, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn2",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 20, "y": 10},
                {"x": 20, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn2",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 30, "y": 10},
                {"x": 30, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn2",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 40, "y": 10},
                {"x": 40, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn2",
            "parents": [],
            "children": [],
        },
        {
            "type": "polygon",
            "points": [
                {"x": 0, "y": 10},
                {"x": 50, "y": 10},
                {"x": 50, "y": 0},
                {"x": 0, "y": 0},
            ],
            "id": "unicorn2",
            "parents": [],
            "children": [],
        },
        {
            "type": "ellipse",
            "center": {"x": 20, "y": 30},
            "radiusX": 10,
            "radiusY": 12,
            "angleOfRotation": 0,
            "id": "unicorn2",
        }
        ]

A = SCFJson(scf_json)
B = SCFJson(scf_json2)

print(A==B)