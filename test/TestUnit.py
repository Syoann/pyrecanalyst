# coding: utf-8

import unittest
from Model.Unit import Unit


class TestUnit(unittest.TestCase):
    def test_unit_creation(self):
        unit = Unit(None, 25)
        self.assertEqual(unit.id, 25)
        self.assertEqual(unit.owner, None)
        self.assertEqual(unit.position, (0, 0))
