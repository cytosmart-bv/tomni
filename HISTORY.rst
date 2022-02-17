# History
1.10.0 (2022-02-17)
------------------
- Add approximate_circle_by_area to contour operations
- BUGFIX: Change type np.array to np.ndarray
- DEPRECATE: Remove simplification so python 3.8+ can be used

1.9.2 (2022-01-03)
------------------
- BUGFIX: Bufferoverflow make_mask_ellipse (again/still) 
    remove times 2 for all values in the function

1.9.1 (2021-10-26)
------------------
- add ellipse to json2mask
- BUGFIX: Bufferoverflow make_mask_ellipse
- BUGFIX: Make make_mask_ellipse accept floats

1.9.0 (2021-10-01)
------------------
- add mask2bbox
- add contour2bbox
- add check_overlap_bbox

1.8.0 (2021-09-01)
------------------
- add mask2json
- add json2mask

1.7.4 (2021-07-02)
------------------
Upgrade/change requirements to work with python 3.9
Opencv needed fuzzy requirments
Remove scikit-image from requirements by replacing the function with numpy function

1.7.3 (2021-06-23)
------------------
speedup positions2contour by replacing for-loop with numpy slicing

1.7.2 (2021-04-21)
------------------
Migrate to github

1.7.1 (2020-12-23)
------------------
updated setup file simplification<0.6

1.7.0 (2020-12-03)
------------------
added new functions
- add_area
- summary_json 
- json2dict

1.6.4 (2020-11-26)
------------------
- add  missing requirements in setup file

1.6.3 (2020-11-25)
------------------
- bug fix. cropping now with deepcopy

1.6.2 (2020-11-10)
------------------
-add fluo_tophat background subtraction

1.6.1 (2020-11-04)
------------------
-add accuracy to json2vgg

1.6.0 (2020-11-03)
------------------
- add json2vgg

1.5.2
------------------
- add ellipse to vgg2json
1.5.1
------------------
- fix rotation, flipping, crop import

1.5.0
------------------
add json_operations
- add crop list of jsons
- add flipping json
- add rotation json

1.4.0
------------------
- add get center point contour
- add get center point json
- add vgg2json

1.3.0
------------------
Updating of relative illumination correction.
- add (optional) smoothing step
- add (optional) resize step
- add (optional) normalization 

1.2.0 (2020-07-02)
------------------
- Add translation of json functions

1.1.0 (2020-03-11)
------------------
Updating of illumination correction.
Splitting into two illumination correction:
- absolute difference
- relative difference

1.0.0 (2020-03-06)
------------------
(new function)
- add_circularity

1.0.0 (2020-02-28)
------------------
Restructuring of tomni:
- Migrated Visualization to cytoBoom
- Migrated validation to manVal
- Made sure every function followed:
    function_name
    - __init__.py 
    - main.py
    - test_function_name
- removed following function:
-- channel_selecting (was only used for old cell counter)
-- select_labels (complete replaceable by transformers.labels2listsOfPoints
- Added docstring to all functions
- Added typing to all functions
- Renamed everything to pep8

0.4.0 (2019-09-30)
------------------
Add transformer as category
- Add labels 2 list of points as function

0.3.3 (2019-09-17)
------------------
Draw_json (draw_json_mask_onto_image):
- rename it from draw_json_mask_onto_image to draw_json
- Make the Visualization of json shapes more dynamic.
- Callable directly from Visualization
- it return an image rather than manipulating it
- converts the color to the color type of input

0.2.1 (2019-07-24)
------------------
Remove f strings to prevent conflicts on python 3.5

0.2.0 (2019-07-09)
------------------
Visualization is now part of tomni.

STRUCTURE:
BGR: All colors are Gray, BGR or BGRA. This because tomni is mostly combined with openCV usage.

FUNCTION:
- Add color converter
- Add circle draw function that works with the input of the cell counter


0.1.8 (2019-02-21)
------------------
- imdim: Function what gives the dimensions of an image from a numpy.ndarray
- ellipse_mask: creates an ellipse at a given position, with given radius length but a fixed rotation

0.0.1 (2018-10-15)
------------------
- First release on PyPI.
