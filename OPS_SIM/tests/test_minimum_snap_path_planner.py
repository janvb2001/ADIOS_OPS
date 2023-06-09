import pytest
import unittest

import minimum_snap_path_planner

class test_minimum_snap_path_planner(unittest.TestCase):

    def test_get_A(self):
        expected_output = minimum_snap_path_planner.get_A()