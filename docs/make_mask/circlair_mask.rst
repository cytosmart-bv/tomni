circlair_mask
=================
.. function:: make_mask_circle(img_shape, diameter)

   Produces a boolean image with a circle of True surrounded by False.

   :param tuple img_shape: The shape of the image given in image coordinates, represented as a tuple of the form (height, width).
   :param int diameter: The diameter of the circle given in pixels.

   :return: A numpy array with a boolean data type, where True represents the circle and False represents the background.
   :rtype: numpy.ndarray

.. function:: make_small_mask_circle(img_shape, diameter)

   Creates a boolean image with a small circle.

   :param tuple img_shape: The shape of the image given in image coordinates, represented as a tuple of the form (height, width).
   :param int diameter: The diameter of the circle given in pixels.

   :return: A numpy array with a boolean data type, where True represents the circle and False represents the background.
   :rtype: numpy.ndarray

.. function:: make_big_mask_circle(img_shape, diameter)

   Creates a boolean image with a large circle.

   :param tuple img_shape: The shape of the image given in image coordinates, represented as a tuple of the form (height, width).
   :param int diameter: The diameter of the circle given in pixels.

   :return: A numpy array with a boolean data type, where True represents the circle and False represents the background.
   :rtype: numpy.ndarray
