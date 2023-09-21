Annotation Manager Workflow
=================================


Example using binary image as input::

    import cv2
    from tkinter import filedialog
    from tomni.annotation_manager import AnnotationManager

    mask_path = filedialog.askopenfilename(title="Select mask.")
    mask = cv2.imread(mask_path, 0)

    manager = AnnotationManager.from_binary_mask(mask=mask, include_inner_contours=True)
    output_dicts = manager.to_dict(
        features=["area", "circularity", "major_axis", "average_diameter"],
        feature_multiplier=1 / 742,
        metric_unit="mm",
    )

Example using list of dictionaries as input::

    import json
    import cv2
    from tkinter import filedialog
    from tomni.annotation_manager import AnnotationManager

    json_path = filedialog.askopenfilename(title="Select JSON.")
    with open(json_path, "rb") as f:
        dicts = json.load(f)

    manager = AnnotationManager.from_dicts(dicts=dicts)
    output_dicts = manager.to_dict(
        features=["area", "circularity", "major_axis", "average_diameter"],
        feature_multiplier=1 / 742,
        metric_unit="mm",
    )

Example how to filter feature values::

    manager.filter(
        feature="roundness",
        min_val=0.5,
        max_val=1.0,
        inplace=True,
    )