summary_json
=================
.. autofunction:: your_module_name.summary_json
   :members:
   :undoc-members:

This function creates a summary of a specified keyword variable inside JSON objects. The summary includes the number of objects, the total sum of the keyword in the JSON list, the mean, maximum, and minimum keyword values in the JSON list.

**Parameters:**

- ``json_list`` (List[dict]): A list of JSON objects in standard CytoSMART format.
- ``keyword`` (str): The keyword to summarize (e.g., 'area').
- ``do_copy`` (bool, optional): When True, copies the JSON list and does not change it (default is True).
- ``rounding`` (int, optional): The number of decimal places used in the summary (default is 2).

**Raises:**

- ``ValueError``: If an unsupported keyword is used.

**Returns:**

- ``tuple``: (Number of objects, Total sum of objects, Mean of objects, Max of objects, Min of objects)

