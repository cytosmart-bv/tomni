cropping
=================
.. autofunction:: your_module_name.json_object_to_keep
   :members:
   :undoc-members:

This function checks if a JSON object is inside the cropped image and determines whether it should be kept based on the specified crop mode.

**Parameters:**

- ``json_object`` (dict): A JSON object following the standard CytoSMART format.
- ``new_x`` (tuple): The x dimensions of the cropped image (xmin_crop, xmax_crop).
- ``new_y`` (tuple): The y dimensions of the cropped image (ymin_crop, ymax_crop).
- ``crop_mode`` (str): The crop mode, either "remove_objects" or "keep_objects" (default is "remove_objects").

**Returns:**

- ``bool``: True if the JSON object should be kept; otherwise, False.

**Raises:**

- ``ValueError``: If the object type is not supported.

.. autofunction:: your_module_name.crop_json
   :members:
   :undoc-members:

This function takes a list of JSON objects (ellipse or polygon, standard CytoSMART format), removes or translates JSON objects in the list, and returns a modified list based on the specified crop parameters and mode.

**Parameters:**

- ``json_list`` (List[dict]): A list of JSON objects in standard CytoSMART format.
- ``x_translation`` (int): The translation in the x-direction of the cropped image relative to the original image.
- ``y_translation`` (int): The translation in the y-direction of the cropped image relative to the original image.
- ``crop_dim`` (list or tuple): The dimensions (x, y) of the cropped image that relate to the list of JSONs.
- ``crop_mode`` (str): The crop mode, either "remove_objects" or "keep_objects" (default is "remove_objects").

**Returns:**

- ``List[dict]``: A modified list of JSON objects after cropping and translation.

