translation
=================
.. autofunction:: your_module_name.translation_json
   :members:
   :undoc-members:

This function takes a JSON object (ellipse or polygon) and translates it by a specified amount in the x and y directions.

**Parameters:**

- ``json_object`` (dict): A JSON object following the standard format.
- ``x_translation`` (int): The translation in the x-direction.
- ``y_translation`` (int): The translation in the y-direction.

**Returns:**

- ``dict``: A new JSON object that has been translated.

**Raises:**

- ``ValueError``: If the object type is not supported.

