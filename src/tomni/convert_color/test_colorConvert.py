from unittest import TestCase
import numpy as np
from numpy import array
from .main import convert_color


class Testconvert_color(TestCase):
    def test_gray2grey(self):
        inputArr = np.zeros((30, 40), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, "grey")

        np.testing.assert_array_equal(result, expected)

    def test_BGR2grey(self):
        inputArr = np.zeros((30, 40, 3), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, 1)

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_BGR2grey_no_int_type(self):
        inputArr = np.zeros((30, 40, 3), dtype=np.float16)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, 1)

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_BGRa2grey(self):
        inputArr = np.zeros((30, 40, 4), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, "gray")

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_gray2BGR(self):
        inputArr = np.zeros((30, 40), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40, 3), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, 3)

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_gray2BGR_3dimension_input(self):
        inputArr = np.zeros((30, 40, 1), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40, 3), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, "colour")

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_BGRa2BGR(self):
        inputArr = np.zeros((30, 40, 4), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40, 3), dtype=np.uint8)
        expected[3, 4] = 40

        result = convert_color(inputArr, "BGr")

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_gray2BGRA(self):
        inputArr = np.zeros((30, 40), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40, 4), dtype=np.uint8)
        expected[3, 4] = 40
        expected[:, :, 3] = 255

        result = convert_color(inputArr, 4)

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_BGR2BGRA(self):
        inputArr = np.zeros((30, 40, 3), dtype=np.uint8)
        inputArr[3, 4] = 40

        expected = np.zeros((30, 40, 4), dtype=np.uint8)
        expected[3, 4] = 40
        expected[:, :, 3] = 255

        result = convert_color(inputArr, "TranspaREnt")

        print(result)
        np.testing.assert_array_equal(result, expected)

    def test_unkownInputColor(self):
        inputArr = np.zeros((30, 40, 7), dtype=np.uint8)
        inputArr[3, 4] = 40

        self.assertRaises(ValueError, convert_color, inputArr, 3)

    def test_unkownInputShape(self):
        inputArr = np.zeros((30, 40, 3, 2), dtype=np.uint8)
        inputArr[3, 4] = 40

        self.assertRaises(ValueError, convert_color, inputArr, 3)

    def test_unkownOutputColorStr(self):
        inputArr = np.zeros((30, 40, 3), dtype=np.uint8)
        inputArr[3, 4] = 40

        self.assertRaises(ValueError, convert_color, inputArr, "Unicorn")

    def test_unkownOutputColorInt(self):
        inputArr = np.zeros((30, 40, 3), dtype=np.uint8)
        inputArr[3, 4] = 40

        self.assertRaises(ValueError, convert_color, inputArr, 42)
