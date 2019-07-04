
import os
import sys
import unittest

from pyrecanalyst.Model.Player import Player


class TestPlayer(unittest.TestCase):
    def test_player(self):
        player = Player(None)
        self.assertFalse(player.is_human())
