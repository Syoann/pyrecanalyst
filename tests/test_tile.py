import os
import sys
import unittest

from pyrecanalyst.Model.Tile import Tile


class TestTile(unittest.TestCase):
    def test_tile_creation(self):
        tile = Tile(5, -5, 1, 0)
        self.assertEqual(tile.x, 5)
        self.assertEqual(tile.y, -5)
        self.assertEqual(tile.terrain, 1)
        self.assertEqual(tile.elevation, 0)
