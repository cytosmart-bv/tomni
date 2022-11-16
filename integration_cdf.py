#%%
from tomni.cytosmart_data_format.annotations import Ellipse, Point

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
