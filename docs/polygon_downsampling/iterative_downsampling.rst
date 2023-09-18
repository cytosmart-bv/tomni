.. function:: iterative_downsampling(points, n_iter)

   Compresses a list of 2D points by reducing the number of points by half iteratively.

   :param list points: A list of 2D points, each represented as a dictionary with {"x": 1, "y": 0}.
   :param int n_iter: An integer representing the number of times to apply the recursive compression method.

   :return: A list of 2D points, each represented as a dictionary with {"x": 1, "y": 0}. The number of points in the output
      list is half the number of points in the input list, repeated `n_iter` times.
   :rtype: list
