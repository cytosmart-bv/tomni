contour_mask_maker
=================
.. function:: make_mask_contour(img_shape, contour)

   Produces a boolean image with the specified contour.

   :param tuple img_shape: The shape of the image given in image coordinates, represented as a tuple of the form (width, height).
   :param Union[list, numpy.ndarray] contour: The contour of the object in the form of a list or numpy array as outputted by OpenCV.

   :return: A numpy array with a boolean data type, where True represents the region enclosed by the contour, and False represents the background.
   :rtype: numpy.ndarray
