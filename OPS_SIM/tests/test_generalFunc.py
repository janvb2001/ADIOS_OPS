import OPS_SIM.generalFunc as generalFunc
import unittest
import pytest

class test_generalFunc(unittest.TestCase):

    def test_dist2d(self):
        actual_distance = generalFunc.dist2d(2, 5, 7, 11)
        expected_distance = 5

        self.assertEqual(expected_distance, actual_distance)

    def test_dist_3d(self):
        actual_distance = generalFunc.dist3d(1, 2, 6, 8, 3, 5)
        expected_distance = 3

        self.assertEqual(expected_distance, actual_distance)