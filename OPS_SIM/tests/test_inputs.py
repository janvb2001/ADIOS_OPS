import inputs as inputs

import pytest
import unittest
import numpy as np

class test_inputs(unittest.TestCase):

    number_of_drone_types = 2

    def test_dict_keys(self):

        with self.subTest():
            actual_keys = list(inputs.litterInput)
            expected_keys = ["amount", "littern", "minvol", "maxvol", "seed"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

        with self.subTest():
            actual_keys = list(inputs.droneInput)
            expected_keys = ["dronetotal", "amountDrone", "vertv", "maxv", "drivev",
                             "maxvol", "power", "maxBat", "litPickT", "litDropT",
                             "b", "d", "k", "m", "Ixx", "Iyy", "Izz"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

        with self.subTest():
            actual_keys = list(inputs.groundStatInput)
            expected_keys = ["x", "y"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

        with self.subTest():
            actual_keys = list(inputs.areaInput)
            expected_keys = ["xsize", "ysize"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

        with self.subTest():
            actual_keys = list(inputs.simPar)
            expected_keys = ["runspeed", "maxplotloops", "dt"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

    def test_array_dimensions(self):

        with self.subTest():
            litterInput = inputs.litterInput
            actual_arrays_dims = [len(litterInput["littern"]), len(litterInput["minvol"]), len(litterInput["maxvol"])]
            expected_array_dims = 2 * np.ones(3)

            np.testing.assert_array_equal(expected_array_dims, actual_arrays_dims)

        with self.subTest():
            droneInput = inputs.droneInput
            actual_arrays_dims = [len(droneInput["amountDrone"]), len(droneInput["vertv"]), len(droneInput["maxv"]),
                                  len(droneInput["drivev"]), len(droneInput["maxvol"]), len(droneInput["power"]),
                                  len(droneInput["maxBat"]), len(droneInput["litPickT"]), len(droneInput["litDropT"]),
                                  len(droneInput["b"]), len(droneInput["d"]), len(droneInput["k"]),
                                  len(droneInput["m"]), len(droneInput["Ixx"]), len(droneInput["Iyy"]),
                                  len(droneInput["Ixx"])]
            expected_array_dims = self.number_of_drone_types * np.ones(16)

            np.testing.assert_array_equal(expected_array_dims, actual_arrays_dims)
