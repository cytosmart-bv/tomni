#%%
# from tomni.cytosmart_data_format import CytoSmartDataFormat
from dataclasses import asdict

from tomni.cytosmart_data_format.annotations import Ellipse, Point

# dummy = CytoSmartDataFormat([{}])

elli = Ellipse(
    radius=Point(1, 3),
    center=Point(0, 0),
    rotation=0,
    id="Hello Jan",
    label="cell",
    children=[],
    parents=[],
)
# print(elli)
# c = elli.center
# print(asdict(elli.center))
print(elli.to_dict())
# print(elli.center)
