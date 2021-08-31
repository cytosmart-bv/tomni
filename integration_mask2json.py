import json
import cv2
from tkinter import filedialog

from tomni.transformers import mask2json

file = filedialog.askopenfilename()
mask = cv2.imread(file, 0)
json_objects = mask2json(mask)

json_objects = [
    x for i, x in enumerate(json_objects) if len(json_objects[i]["points"]) >= 3
]

with open(file.replace(".png", ".json"), "w") as f:
    json.dump(json_objects, f)
