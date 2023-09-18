mask2bbox
=========================
.. automodule:: tomni
   :members: mask2bbox
   :show-inheritance:

This function takes a binary image mask as input and calculates the bounding box coordinates (xmin, ymin, xmax, ymax) of the region covered by the mask. Optionally, you can specify padding to add or subtract from the bounding box coordinates.

Example Usage::

   import numpy as np

   # Create a binary mask
   mask = np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.uint8)

   # Get the bounding box coordinates with padding
   bbox = mask2bbox(mask, padding=1)

   # Process the bounding box coordinates as needed

.. note::
   - The function calculates the bounding box by finding the first and last non-zero rows and columns in the mask.
   - Padding can be used to adjust the size of the bounding box.

You can save this documentation in a `.rst` file, such as `mask2bbox.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
