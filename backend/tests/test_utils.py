import os
import unittest
import tempfile
from core.utils import get_dir_size, bbox


class TestGetDirSize(unittest.TestCase):
    # Set up temporary directory and create subdirectories and files
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = self.test_dir.name

        os.mkdir(os.path.join(self.test_dir_path, "subdir"))
        with open(os.path.join(self.test_dir_path, "file1.txt"), "w") as f:
            f.write("12345")
        with open(os.path.join(self.test_dir_path, "subdir", "file2.txt"), "w") as f:
            f.write("1234567890")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_get_dir_size(self):
        expected_size = 5 + 10
        calculated_size = get_dir_size(self.test_dir_path)
        self.assertEqual(calculated_size, expected_size)


class TestBBox(unittest.TestCase):
    # Tests of areas with different coordinates/polygon types

    def test_simple_rectangle(self):
        coords = [(10.0, 20.0), (10.0, 30.0), (20.0, 30.0), (20.0, 20.0)]
        expected = [10.000001, 20.000001, 19.999999, 29.999999]
        self.assertEqual(bbox(coords), expected)

    def test_complex_polygon(self):
        coords = [(10.0, 20.0), (10.0, 30.0), (20.0, 25.0), (15.0, 20.0)]
        expected = [10.000001, 20.000001, 19.999999, 29.999999]
        self.assertEqual(bbox(coords), expected)

    def test_negative_coordinates(self):
        coords = [(-10.0, -20.0), (-10.0, -30.0), (-20.0, -30.0), (-20.0, -20.0)]
        expected = [-19.999999, -29.999999, -10.000001, -20.000001]
        self.assertEqual(bbox(coords), expected)

    def test_with_correction_factor(self):
        coords = [(0.0, 0.0), (0.0, 10.0), (10.0, 10.0), (10.0, 0.0)]
        expected = [0.000001, 0.000001, 9.999999, 9.999999]
        self.assertEqual(bbox(coords), expected)

    def test_zero_and_near_zero_values(self):
        coords = [(-0.000001, -0.000002), (0.000001, 0.000002)]
        expected = [0.0, -1e-06, 0.0, 1e-06]
        self.assertEqual(bbox(coords), expected)
