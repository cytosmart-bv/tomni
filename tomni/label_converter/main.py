import numpy as np
import uuid

from tomni.transformers import mask2json, json2mask


class LabelConverter:

    label_formats = ["scf", "scfcls", "azure", "deepai", "mask"]

    def __init__(self, format1: str, format2: str) -> None:
        if not format1 in self.label_formats:
            raise ValueError(f"format {format1} is not supported")

        if not format2 in self.label_formats:
            raise ValueError(f"format {format2} is not supported")

        self.base_format = "scf"
        self.format1 = format1
        self.format2 = format2

    def scf2scfcls(self, scf_label, class_name="object", *args, **kwargs):
        return {class_name: scf_label}

    def scfcls2scf(self, label, *args, **kwargs):
        keys = list(label.keys())
        return label[keys[0]]

    def mask2scf(self, mask: np.ndarray, *args, **kwargs):
        return mask2json(
            mask,
            kwargs.get("minimum_size_contours", 3),
            kwargs.get("is_diagonal_connected", True),
        )

    def scf2mask(self, scf_label, image_size, *args, **kwargs) -> np.ndarray:
        return json2mask(scf_label, image_size, kwargs.get("minimum_size_contours", 3))

    def deepai2scf(self, label, *args, **kwargs):
        scf_label = []
        for json_object in label["objects"]:
            scf_object = {
                "type": "polygon",
                "id": str(uuid.uuid4()),
                "label": json_object["labels"]["label"],
            }
            points = []
            for coords in json_object["mask_vertices"][0]:
                points.append({"x": coords[0], "y": coords[1]})

            scf_object["points"] = points
            scf_label.append(scf_object)

        return scf_label

    def scf2deepai(self, scf_label, *args, **kwargs):
        return scf_label

    def azure2scf(self, label, image_size=(1024, 1024), *args, **kwargs):
        scf_label = []

        for object in label:
            prob = object["probability"]
            object = object["boundingBox"]
            left = object["left"] * image_size[0]
            width = object["width"] * image_size[0]
            top = object["top"] * image_size[1]
            height = object["height"] * image_size[1]

            new_object = {
                "id": str(uuid.uuid4()),
                "type": "ellipse",
                "center": {
                    "x": np.round(left + width / 2),
                    "y": np.round(top + height / 2),
                },
                "radiusX": np.round(width / 2),
                "radiusY": np.round(height / 2),
                "accuracy": prob,
            }
            scf_label.append(new_object)

        return scf_label

    def convert(self, label, *args, **kwargs):
        if self.format1 == self.format2:
            return label

        if self.format1 == self.base_format or self.format2 == self.base_format:
            return getattr(self, f"{self.format1}2{self.format2}")(
                label, *args, **kwargs
            )

        else:
            inter_label = getattr(self, f"{self.format1}2{self.base_format}")(
                label, *args, **kwargs
            )
            return getattr(self, f"{self.base_format}2{self.format2}")(
                inter_label, *args, **kwargs
            )


if __name__ == "__main__":
    import json
    import cv2
    from tkinter import filedialog

    path = filedialog.askopenfilename()
    with open(path, "r") as f:
        scf_json = json.load(f)

    conv = LabelConverter("deepai", "mask")
    mask = conv.convert(scf_json, image_size=(500, 500))
    cv2.imwrite("test.png", mask * 255)
