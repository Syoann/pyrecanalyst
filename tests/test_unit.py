import os
import sys
import unittest

from pyrecanalyst.Model.Unit import Unit


class TestUnit(unittest.TestCase):
    def test_unit_creation(self):
        unit = Unit(None, 25)
        self.assertEqual(unit.id, 25)
        self.assertEqual(unit.owner, None)
        self.assertEqual(unit.position, (0, 0))
