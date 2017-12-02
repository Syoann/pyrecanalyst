# coding: utf-8

from Analyzers.Analyzer import Analyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer
from Model.Tile import Tile


class TerrainAnalyzer(Analyzer):
    def __init__(self, size):
        self.size_x = size[0]
        self.size_y = size[1]

    def run(self):
        version = self.get(VersionAnalyzer)

        map_data = []

        for y in range(0, self.size_y):
            map_data.append([])
            for x in range(0, self.size_x):
                terrain_id = ord(self.header[self.position])
                self.position += 1

                if terrain_id == int('0xFF', 16):
                    terrain_id = ord(self.header[self.position])
                    self.position += 1
                    elevation = ord(self.header[self.position])
                    self.position += 1
                    # Skip UserPatch "original terrain ID" data.
                    self.position += 1
                else:
                    elevation = ord(self.header[self.position])
                    self.position += 1

                map_data[y].append(Tile(x, y, terrain_id, elevation))
        return map_data
