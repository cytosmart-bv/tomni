import numpy as np
import cv2
import json

from tomni.transformers import json2vgg

# README
# To test in VIA, first import the json file and than add the image

img_name = "test_vgg"
extension = ".jpg"
img = np.zeros((100, 100))

json_list = [
    {
        "type": "polygon",
        "accuracy": 0.4,
        "parents": [],
        "children": [],
        "id": "unicorn",
        "points": [{"x": 50, "y": 74}, {"x": 47, "y": 75}, {"x": 44, "y": 89}],
    },
    {
        "type": "ellipse",
        "accuracy": 0.32,
        "id": "unicorn",
        "center": {"x": 76, "y": 64},
        "radiusX": 5,
        "radiusY": 5,
        "angleOfRotation": 0,
    },
]

vgg_json = json2vgg(json_list, img_name, extension)

cv2.imwrite(f"{img_name}{extension}", img)

with open(f"{img_name}.json", "w") as f:
    json.dump(vgg_json, f)
