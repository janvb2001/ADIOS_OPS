import pytest
import unittest
import numpy as np

import minimum_snap_path_planner

class test_minimum_snap_path_planner(unittest.TestCase):

    def test_get_A(self):
        expected_output = minimum_snap_path_planner.get_A(0, 1)
        actual_output = np.array([[0, 0, 0, 0, 0, 0, 0, 1],
                                  [0, 0, 0, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0, 2, 0, 0],
                                  [0, 0, 0, 0, 6, 0, 0, 0],
                                  [1, 1, 1, 1, 1, 1, 1, 1],
                                  [7, 6, 5, 4, 3, 2, 1, 0],
                                  [42, 30, 20, 12, 6, 2, 0, 0],
                                  [210, 120, 60, 24, 6, 0, 0, 0]])

        np.testing.assert_array_equal(expected_output, actual_output)

    def test_get_polynomial_from_coeffs(self):
        coefficients = np.array([1, 2, 3, 4, 5, 6, 7, 8])

        r_t = minimum_snap_path_planner.get_polynomial_from_coeffs(coefficients)
        t_array = np.array([0, 1, 2])
        actual_output = r_t(t_array)

        expected_output = np.array([8, 36, 502])

        np.testing.assert_array_equal(expected_output, actual_output)

    def test_create_setpoints_from_A_star(self):
        pass

    def test_get_wind_direction(self):
        positions_array = np.array([[[0, 1], [0, 2]],
                                    [[2, 6], [3, 7]],
                                    [[1, 5], [2, 5]],
                                    [[2, 0], [3, -1]],
                                    [[3, 6], [3, 5]],
                                    [[2, 5], [1, 4]],
                                    [[0, 0], [-1, 0]],
                                    [[3, 6], [2, 7]]])

        expected_directions_values = np.array([0, 1, 2, 3, 4, 5, 6, 7])

        for i in range(len(positions_array)):
            x_1 = positions_array[i][0][0]
            x_2 = positions_array[i][1][0]

            y_1 = positions_array[i][0][1]
            y_2 = positions_array[i][1][1]

            actual_direction = minimum_snap_path_planner.get_wind_direction(x_1, x_2, y_1, y_2)

            with self.subTest():
                self.assertEqual(expected_directions_values[i], actual_direction)