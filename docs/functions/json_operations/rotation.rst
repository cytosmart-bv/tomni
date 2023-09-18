rotation
=================
.. autofunction:: your_module_name.rotate_json
   :members:
   :undoc-members:

This function takes a JSON object (ellipse or polygon, standard CytoSMART format) and rotates it by 0, 90, 180, or 270 degrees.

**Parameters:**

- ``json_object`` (dict): A JSON object following the standard CytoSMART format.
- ``angle`` (int): The angle of rotation, which can be 0, 90, 180, or 270 degrees.
- ``img_shape`` (list or tuple): The shape of the image that the JSON object is related to.

**Returns:**

- ``dict``: A new JSON object with rotated coordinates.

**Raises:**

- ``ValueError``: If an unknown angle is provided (should be 0, 90, 180, or 270).
- ``AssertionError``: If the image shape is not a 2-element list or tuple.

