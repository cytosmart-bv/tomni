#%%
from tomni.cytosmart_data_format.annotations import Ellipse, Point, Polygon

#%%
# Ellipse annotation
elli = Ellipse(
    radius=Point(1, 3),
    center=Point(0, 0),
    rotation=0,
    id="Hello Jan",
    label="cell",
    children=[],
    parents=[],
)

print(elli.to_dict())


#%%
# Polygon annotation
star_shaped_points = [
    Point(1, 3),
    Point(2, 3),
    Point(3, 5),
    Point(5, 3),
    Point(3, 1),
    Point(2, 2),
]
star_shaped_polygon = Polygon(
    points=star_shaped_points,
    id="132132132123132",
    children=[],
    parents=[],
    label="star",
)

star_shaped_polygon.to_dict()

# %%