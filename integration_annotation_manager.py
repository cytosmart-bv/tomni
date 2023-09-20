import json
import os
from tkinter import filedialog
import numpy as np

import cv2
import cytoBoom as CB

from tomni.annotation_manager import AnnotationManager
from tomni.transformers.json2contours import json2contours


# %%
json_fp = filedialog.askopenfilename(title="Select CDF JSONs.")

with open(json_fp, "rb") as f:
    dicts = json.load(f)
    print(f"Found {len(dicts)} dictionaries in json file.")


# %%
manager = AnnotationManager.from_dicts(dicts=dicts)
dicts_ = manager.to_dict(
    features=["area", "circularity", "major_axis", "average_diameter"],
    feature_multiplier=1 / 742,
    metric_unit="mm",
)
print(dicts_[0])

# %%
contours = [json2contours(d) for d in dicts]
manager = AnnotationManager.from_contours(contours=contours)

# %%
shape = (2072, 2072)
bin_mask_fp = filedialog.askopenfilename(title="Select binary mask.")
mask = cv2.imread(bin_mask_fp, cv2.IMREAD_GRAYSCALE)
manager = AnnotationManager.from_binary_mask(mask=mask)
cv2.imwrite("to_binary_mask.png", manager.to_binary_mask(shape))

# %%
shape = (2072, 2072)
labeled_mask_fp = filedialog.askopenfilename(title="Select labeled mask.")
mask = cv2.imread(labeled_mask_fp, cv2.IMREAD_GRAYSCALE)
manager = AnnotationManager.from_labeled_mask(mask=mask)
cv2.imwrite("to_labeled_mask.png", manager.to_labeled_mask(shape))

# %%
print(f"__len__: {len(manager)}")

# %%
# manager creates a generator.
count = 0
for annotation in manager:
    count += 1
print(f"Count: {count}")


# %%
dicts_ = manager.to_dict()

with open("temp.json", "w") as f:
    json.dump(dicts_, f)

# %% #simplify polygons
dicts_ = manager.to_dict(do_compress=True, epsilon=3)
with open("temp.json", "w") as f:
    json.dump(dicts_, f)


# %% to_dict with masked rois.
# define masks for a lux image, ideally you use a lux json but whatever floats your boat.

size = int(2072 / 2)
rad = int(2072 / 3)
mask_json = [
    {
        "type": "ellipse",
        "center": {"x": size, "y": size},
        "radiusX": rad,
        "radiusY": rad,
        "angleOfRotation": 0,
        "name": "A1",
    }
]

_dicts = manager.to_dict(mask_json=mask_json, min_overlap=0.9)
print(_dicts)
img_path = json_fp.replace("json", "jpg")
if os.path.exists(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    for _dict in _dicts:
        CB.over_draw_json(img, _dict, stroke_width=3, color=(0, 255, 0))

    CB.over_draw_json(img, mask_json[0], stroke_width=3, color=(255, 0, 0))
    cv2.imwrite("to_dict_with_mask.png", img)

# %%
# Replace with the dimensions of your image.
bin_mask = manager.to_binary_mask(shape=(2072, 2072))
cv2.imwrite("binary_mask.png", bin_mask * 255)


# %%
conts = manager.to_contours()
print(conts)


# %%
annotations = manager.filter(feature="roundness", min_val=0.5, max_val=1.0)
print(annotations)

# %%
Filter with inplace=True: manager object is updated internally. Returns manager object to allow chaining.
updated_manager = manager.filter(
    # The return does not have to be used. This is merely to show difference between inplace.
    feature="roundness",
    min_val=0.5,
    max_val=1.0,
    inplace=True,
).filter(feature="area", min_val=0, max_val=1000, inplace=True)
print(type(updated_manager))


# %%
# Filter: inplace=False returns a new list of annotations.
annotations = manager.filter(
    feature="roundness", min_val=0.5, max_val=1.0, inplace=False
)
print(type(annotations))

%%
