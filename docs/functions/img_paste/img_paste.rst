img_paste
=================

.. automodule:: tomni
   :members: img_paste
   :show-inheritance:

.. This function adds a smaller image to a larger image by translating it to a specified position (x, y) in image coordinates.

.. **Parameters:**

.. - ``big_img`` (numpy.ndarray): The larger image that gets altered.
.. - ``small_img`` (numpy.ndarray): The smaller image that gets added to the `big_img`.
.. - ``x`` (int): Image coordinate x.
.. - ``y`` (int): Image coordinate y.

.. **Returns:**

.. - None: `big_img` gets altered in-place.

.. This function calculates the position of the smaller image in the larger image, taking into account boundaries and cropping as necessary.
