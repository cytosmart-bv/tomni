# %%
from typing import Tuple, Union

from shapely import affinity
from shapely.geometry import MultiPolygon, Polygon, point
from shapely.ops import polygonize


def get_boundingbox(annotation_object: dict) -> Tuple[int, int, int, int]:
    """Calculate the bounding box of the dict annotation object.

    Args:
        object (dict): A JSON annotation object.

    Raises:
        ValueError: If object type is not known.

    Returns:
        Tuple[int,int,int,int]: A tuple containing the min_x, min_y, max_x and max_y of the bounding box.
    """
    if annotation_object["type"] == "polygon":
        all_x = [j["x"] for j in annotation_object["points"]]
        all_y = [j["y"] for j in annotation_object["points"]]
        return (min(all_x), min(all_y), max(all_x), max(all_y))
    elif annotation_object["type"] == "ellipse":
        return (
            annotation_object["center"]["x"] - annotation_object["radiusX"],
            annotation_object["center"]["y"] - annotation_object["radiusY"],
            annotation_object["center"]["x"] + annotation_object["radiusX"],
            annotation_object["center"]["y"] + annotation_object["radiusY"],
        )
    else:
        raise ValueError(f"Object 1 has an unkown type of {annotation_object['type']}")


def are_boundingboxes_overlapping(
    bbox1: Tuple[int, int, int, int], bbox2: Tuple[int, int, int, int]
) -> bool:
    """Checks if bounding boxes are overlapping and returns truth value.

    Args:
        bbox1 (Tuple[int,int,int,int]): A tuple containing the min_x, min_y, max_x and max_y of bounding box 1.
        bbox2 (Tuple[int,int,int,int]): A tuple containing the min_x, min_y, max_x and max_y of bounding box 2.

    Returns:
        bool: Returns a truth value indicating whether the bounding boxes are overlapping.
    """
    if bbox1[0] >= bbox2[2]:
        return False
    elif bbox2[0] >= bbox1[2]:
        return False
    elif bbox1[1] >= bbox2[3]:
        return False
    elif bbox1[3] <= bbox2[1]:
        return False
    else:
        return True


def create_ellipse(
    center: Tuple[int, int], radii: Tuple[int, int], angle: Union[int, None] = 0
):
    if radii[0] < 0 or radii[1] < 0:
        raise ValueError("Radi cannot be negative")
    circ = point.Point(center).buffer(1)
    ell = affinity.scale(circ, int(radii[0]), int(radii[1]))
    ellr = affinity.rotate(ell, angle)

    return ellr


def object2shape(annotation_object: dict):
    """Convert object dict to shapely shape.

    Args:
        object (dict): An annotation object in AxionBio format.

    Raises:
        ValueError: If type of the annotation object is unknown.

    Returns:
        Returns a shapely shape.
    """
    if annotation_object["type"] == "polygon":
        object_points = [[j["x"], j["y"]] for j in annotation_object["points"]]
        if len(object_points) < 3:
            return Polygon()

        polygon = Polygon(object_points)
        if polygon.is_valid:
            return polygon
        else:
            be = polygon.exterior
            mls = be.intersection(be)
            polygons = polygonize(mls)
            multi_polygons = MultiPolygon(polygons)
            return multi_polygons

    elif annotation_object["type"] == "ellipse":
        return create_ellipse(
            (annotation_object["center"]["x"], annotation_object["center"]["y"]),
            (annotation_object["radiusX"], annotation_object["radiusY"]),
            annotation_object["angleOfRotation"],
        )
    else:
        raise ValueError(f"Object 1 has an unkown type of {annotation_object['type']}")


def overlap_object(object_1: dict, object_2: dict) -> float:
    """This function calculates the overlap percentage of the first object with the second object.

    Args:
        object1 (dict): JSON object1 in AxionBio format
        object2 (dict): JSON object2 in AxionBio format

    Returns:
        int: overlap percentage.
    """

    bbox1 = get_boundingbox(object_1)
    bbox2 = get_boundingbox(object_2)

    if not are_boundingboxes_overlapping(bbox1, bbox2):
        return 0

    shape1 = object2shape(object_1)
    shape2 = object2shape(object_2)

    intersect = shape1.intersection(shape2)
    overlap_percentage = intersect.area / (shape1.area + 1e-17)
    return overlap_percentage
