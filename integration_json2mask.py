import cv2
import json

from tkinter import filedialog

from tomni.transformers import json2mask

file = filedialog.askopenfilename()
image_path = filedialog.askopenfilename()

with open(file, "r") as f:
    json_objects = json.load(f)

image = cv2.imread(image_path, 0)

mask = json2mask(json_objects, image.shape)

cv2.imwrite(file.replace(".json", "_mask.png"), mask * 255)
