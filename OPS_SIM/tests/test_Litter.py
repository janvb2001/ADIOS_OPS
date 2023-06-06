import OPS_SIM.litter as Litter

import unittest
import pytest

class test_Litter(unittest.TestCase):

    def test_init(self):
        litter = Litter.litter(1, 2, 3, 4, 5)

        with self.subTest():
            self.assertEqual(1, litter.x)
        with self.subTest():
            self.assertEqual(2, litter.y)
        with self.subTest():
            self.assertEqual(3, litter.z)
        with self.subTest():
            self.assertEqual(4, litter.typeL)
        with self.subTest():
            self.assertEqual(5, litter.vol)
        with self.subTest():
            self.assertEqual(True, litter.avail)
        with self.subTest():
            self.assertEqual(False, litter.picked)