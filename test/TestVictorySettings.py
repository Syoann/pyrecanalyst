#! /usr/bin/env python
# coding: utf-8

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from Model.VictorySettings import VictorySettings


class TestVictorySettings(unittest.TestCase):
    def test_get_victory_string(self):
        settings = VictorySettings(None)
        self.assertEqual(settings.get_victory_string(), "Standard")
