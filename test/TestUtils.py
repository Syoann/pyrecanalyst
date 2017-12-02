# coding: utf-8

import unittest
from Utils import Utils


class TestUtils(unittest.TestCase):
    def test_format_game_time(self):
        self.assertEqual(Utils.format_game_time(1000), "00:00:01")
        self.assertEqual(Utils.format_game_time(60000), "00:01:00")
        self.assertEqual(Utils.format_game_time(3600000), "01:00:00")

    def test_format_game_time_59(self):
        self.assertEqual(Utils.format_game_time(59000), "00:00:59")
        self.assertEqual(Utils.format_game_time(3599000), "00:59:59")
        self.assertEqual(Utils.format_game_time(215999000), "59:59:59")
