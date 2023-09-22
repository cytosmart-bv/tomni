# History
2.0.0-b3 (2023-09-08) 
------------------
- Added check for rectangled contours.
    - Adds extra point if rectangle.
    - This allows us to initialize masks (of wells) that only consist of 4 points if required in the future.
- Added unittests for empty and full masks from binary_mask and from_labeled_mask
- Changed variable name in `ellipse` class from r1/r2 to diameter_1/diameter_2 etc for naming clarity.
- BUGFIX: Multiplied minor axis and major axis by 2 in `ellipse` class, which was currently calculated as radii instead of diameters.
- BUGFIX: Fixed average diameter in `ellipse` class, which was calculated with radii instead of diameters.
- BUGFIX: removed assert, which took over half the time of the entire `from_binary_mask`.
- BUGFIX: Fixed unittest labels2listsOfPoints

2.0.0-b2 (2023-08-04) 
------------------
- Moved feature_multiplier and metric_unit to to_dict() from from_dict(). 
- Added inner contours options 
- added binary2contours
- change parameters for from_binary_mask
- made contours2polygon

2.0.0-b1 (2023-07-06)
------------------
- AnnotationManager function from_dict is called with an optional list of features
- Changed Polygon and Ellipse classes to include the list of features initialized by AnnotationManager
- to_dict function now only returns features in the dictionary that were asked for in the feature list
- Added `feature_multiplier` and `metric_unit` as inputs to apply to the features' name and value outputs.
- Added all features to `ellipse` and `polygon`.
- Features are now in camelCasing when output `to_dict`

2.0.0-b0 (2022-11-29)
------------------
- CDF-Main: Implement `filter` to allow filtering of annotations by feature values (aka gating).
- CDF-Main: Implement `from_contours`.
- CDF-Main: Implement `to_contours`.
- CDF-Main: Implement `from_dict`.
- CDF-Main: Implement `to_dict`. Includes rounding.
- CDF-Main: Implement `__len__`.
- CDF-Main: Implement `__iter__` and `__next__`.
- Add polygon annotation class.
- CDF-polygon: Implement `__eq__`
- CDF-polygon: Remove useless point
- Add ellipse annotation class.
- CDF-ellipse: Implement `__eq__`
- CDF-ellipse: Set all rotations between 0 and 90, flip radii if needed
- Renamed `CytoSmartDataFormat` to `AnnotationManager`
- Add `is_in_mask` for `Ellipse` and `Polygon`
- Add `min_overlap`-parameter in `to_dict` to apply masks to filter annotations
- Add `to_binary_mask` and `to_labeled_mask` for `AnnotationManager`, `Ellipse` and `Polygon`
- Add init-function `from_binary_mask` and `from_labeled_mask` to `AnnotationManager`
- Bugfix: Fixed a bug where `simplify_line` returns empty list when passing two points.
- Add option to to compress polygons in `to_dict()`.
1.17.0 (2023-07-26)
- Add binary2contours

1.16.1 (2023-05-10)
- make it possible to set n_iter to 0. 

1.16.0 (2023-05-08)
- Add iterative_downsampling for downsampling polygon points in 'naive' way

1.15.0 (2022-12-05)
------------------
- Add json2bbox for ellipse with angle of rotation

1.14.0 (2022-11-11)
------------------
- Add convert to color

1.13.0 (2022-10-24)
------------------
- Add json2bbox for polygon and ellipse

1.12.1 (2022-10-06)
------------------
- Update Json-circularity with circularity calculation from contour ops.

1.12.0 (2022-04-15)
------------------
- BUGFIX: Import approximate_circle_by_area
- Add roundness
- Add contour operation circularity

1.11.0 (2022-04-11)
------------------
- Add inner contours to labels2contours
- Add inner contours to mask2json

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
