from typing import List


def json2vgg(
    json_list: List[dict],
    image_name: str,
    extension: str = ".jpg",
    add_accuracy: bool = True,
):
    """
    Transform a list of JSON annotations into a format compatible with 'VGG Image Annotator'.

    Args:
        json_list (List[dict]): A list of JSON objects representing annotations in the standard AxionBio format.
        image_name (str): The name of the image to which the annotations will be overlaid within 'VGG Image Annotator'.
        extension (str, optional): The file extension for the image. Defaults to ".jpg".
        add_accuracy (bool, optional): If True, include an "accuracy" attribute in the region attributes of each annotation.
            If False, omit the accuracy attribute. Defaults to True.

    Returns:
        dict: A JSON object compatible with 'VGG Image Annotator' format, containing the image filename,
            a list of regions (annotations), and file attributes.
    """
    file_name = f"{image_name}{extension}"
    regions = []

    for json_object in json_list:
        vgg_object = {"shape_attributes": {}}
        if json_object["type"] == "ellipse":
            vgg_object["shape_attributes"]["name"] = json_object["type"]
            vgg_object["shape_attributes"]["cx"] = json_object["center"]["x"]
            vgg_object["shape_attributes"]["cy"] = json_object["center"]["y"]
            vgg_object["shape_attributes"]["rx"] = json_object["radiusX"]
            vgg_object["shape_attributes"]["ry"] = json_object["radiusY"]
            vgg_object["shape_attributes"]["theta"] = json_object["angleOfRotation"]

        elif json_object["type"] == "polygon":
            vgg_object["shape_attributes"]["name"] = json_object["type"]
            vgg_object["shape_attributes"]["all_points_x"] = [
                f["x"] for f in json_object["points"]
            ]
            vgg_object["shape_attributes"]["all_points_y"] = [
                f["y"] for f in json_object["points"]
            ]
        else:
            raise ValueError(f"Object type {json_object['type']} not supported")
        if add_accuracy:
            vgg_object["region_attributes"] = {"accuracy": json_object["accuracy"]}
        else:
            vgg_object["region_attributes"] = {}
        regions.append(vgg_object)

    vgg_json = {
        file_name: {"filename": file_name, "regions": regions, "file_attributes": {}}
    }

    return vgg_json
