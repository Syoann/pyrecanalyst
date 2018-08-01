#! /usr/bin/env python
# coding: utf-8

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from Model.Tribute import Tribute


class TestTribute(unittest.TestCase):
    def test_tribute_creation(self):
        tribute = Tribute()
        self.assertEqual(Tribute.FOOD, 0)
        self.assertEqual(Tribute.WOOD, 1)
        self.assertEqual(Tribute.STONE, 2)
        self.assertEqual(Tribute.GOLD, 3)
