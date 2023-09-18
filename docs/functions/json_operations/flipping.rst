flipping
=================
.. autofunction:: your_module_name.flip_json
   :members:
   :undoc-members:

This function takes a JSON object (ellipse or polygon, standard CytoSMART format) and flips it over the y-axis.

**Parameters:**

- ``json_object`` (dict): A JSON object following the standard CytoSMART format.
- ``img_dim`` (int): The y-dimension of the image related to the JSON object.

**Returns:**

- ``dict``: A new JSON object with flipped coordinates.

**Raises:**

- ``TypeError``: If the object type is not supported.

