#! /usr/bin/env python
# coding: utf-8

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from Model.Player import Player


class TestPlayer(unittest.TestCase):
    def test_player(self):
        player = Player(None)
        self.assertFalse(player.is_human())
