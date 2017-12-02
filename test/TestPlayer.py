#! /usr/bin/env python
# coding: utf-8

import unittest
from Model.Player import Player


class TestPlayer(unittest.TestCase):
    def test_player(self):
        player = Player(None)
        self.assertFalse(player.is_human())
