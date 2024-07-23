def iterative_downsampling(points: list, n_iter: int) -> list:
    """
    Compress a list of 2D points by reducing the number of points by half iteratively.

    Args:
        points (list): A list of 2D points, where each point is represented as a dictionary with {"x": 1, "y": 0}.
        n_iter (int): An integer representing the number of times to apply the recursive compression method.

    Returns:
        list: A list of 2D points, where each point is represented as a dictionary with {"x": 1, "y": 0}.
            The number of points in the output list is half the number of points in the input list, repeated `n_iter` times.

    """

    assert n_iter >= 0, "Nr of iterations must be zero or positive."

    for _ in range(n_iter):
        points = points[::2]

    return points
