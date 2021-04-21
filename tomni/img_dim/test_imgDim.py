from unittest import TestCase
import numpy as np 
from .main import img_dim

class Test_img_dim(TestCase):
    def test_happyflow_no_channel(self):
        inArr = np.zeros((10, 20))
        expected = [20, 10]
        result = img_dim(inArr, False)

        np.testing.assert_array_equal(result, expected)

    def test_happyflow_no_given_channel(self):
        inArr = np.zeros((10, 20))
        expected = [20, 10, 1]
        result = img_dim(inArr, True)

        np.testing.assert_array_equal(result, expected)

    def test_happyflow_with_channel(self):
        inArr = np.zeros((10, 20, 3))
        expected = [20, 10, 3]
        result = img_dim(inArr, True)

        np.testing.assert_array_equal(result, expected)

    def test_happyflow_with_noshow_channel(self):
        inArr = np.zeros((10, 20, 3))
        expected = [20, 10]
        result = img_dim(inArr, False)

        np.testing.assert_array_equal(result, expected)