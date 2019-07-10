import os
import sys
import unittest

from pyrecanalyst.Model.VictorySettings import VictorySettings


class TestVictorySettings(unittest.TestCase):
    def test_get_victory_string(self):
        settings = VictorySettings(None)
        self.assertEqual(settings.get_victory_string(), "Standard")
