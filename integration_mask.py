import cv2

from tomni.annotation_manager.annotations.ellipse.main import Ellipse
from tomni.annotation_manager.annotations.point.main import Point
from tomni.annotation_manager.annotations.polygon.main import Polygon
from tomni.annotation_manager.utils.is_annotation_in_mask.main import (
    get_mask_from_ellipse,
    get_mask_from_polygon,
    is_annotation_in_mask,
)

# Create a mask
ellipse = Ellipse(
    radius_x=20,
    radius_y=20,
    center=Point(500, 500),
    rotation=0,
    id="",
    label="",
    children=[],
    parents=[],
)
polygon = Polygon(
    points=[Point(500, 505), Point(500, 495), Point(505, 500)],
    id="",
    label="",
    children=[],
    parents=[],
)
# mask = get_mask_from_ellipse(ellipse)
mask = get_mask_from_polygon(polygon)


# annotation = Polygon(
#     points=[Point(500, 505), Point(500, 495), Point(505, 500)],
#     id="",
#     label="",
#     children=[],
#     parents=[],
# )
annotation = Ellipse(
    radius_x=5,
    radius_y=5,
    center=Point(500, 500),
    rotation=0,
    id="",
    label="",
    children=[],
    parents=[],
)

is_annotation_in_mask(annotation, mask, 1.0)
