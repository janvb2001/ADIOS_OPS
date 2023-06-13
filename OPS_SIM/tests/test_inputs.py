import inputs as inputs

import pytest
import unittest
import numpy as np

class test_inputs(unittest.TestCase):

    number_of_drone_types = 2

    def test_dict_keys(self):

        with self.subTest():
            actual_keys = list(inputs.litterInput)
            expected_keys = ["amount", "littern", "minvol", "maxvol", "drivingdist",  "seed"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

        with self.subTest():
            actual_keys = list(inputs.droneInput)
            expected_keys = ["dronetotal", "amountDrone", "vertv", "maxv", "drivev",
                             "maxvol", "battothrusteff", "powerFlightcom", "powergrabbing", "powerDriving",
                             "powerObjDetec",  "maxBat", "litPickT", "litDropT",
                             "recharget", "b", "d", "k", "m", "S_blade", "Ixx", "Iyy", "Izz"]

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
            expected_keys = ["runspeed", "maxplotloops", "dt", "plotOperation", "printErrors"]

            np.testing.assert_array_equal(expected_keys, actual_keys)

        with self.subTest():
            actual_keys = list(inputs.pathplanningPar)
            expected_keys = ["gridresolution", "buildingresolution", "animation", "obstacles",
                             "obstacleHeight", "alpha_obst", "factor_animation"]

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
                                  len(droneInput["drivev"]), len(droneInput["maxvol"]), len(droneInput["battothrusteff"]),
                                  len(droneInput["powerFlightcom"]), len(droneInput["powergrabbing"]), len(droneInput["powerDriving"]),
                                  len(droneInput["powerObjDetec"]), len(droneInput["maxBat"]), len(droneInput["litPickT"]),
                                  len(droneInput["litDropT"]), len(droneInput["b"]), len(droneInput["d"]),
                                  len(droneInput["k"]), len(droneInput["m"]), len(droneInput["S_blade"]),
                                  len(droneInput["Ixx"]), len(droneInput["Iyy"]), len(droneInput["Ixx"])]
            expected_array_dims = self.number_of_drone_types * np.ones(21)

            np.testing.assert_array_equal(expected_array_dims, actual_arrays_dims)
