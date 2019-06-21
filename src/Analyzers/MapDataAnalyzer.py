from Analyzers.Analyzer import Analyzer
from Analyzers.TerrainAnalyzer import TerrainAnalyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer


class MapDataAnalyzer(Analyzer):
    def run(self):
        self.version = self.get(VersionAnalyzer)

        self.map_size_x = self.read_header('<l', 4)
        self.map_size_y = self.read_header('<l', 4)

        # If we went wrong somewhere, throw now so we don't end up in a near-
        # infinite loop later.
        if self.map_size_x > 10000 or self.map_size_y > 10000:
            raise Exception('Got invalid map size')

        self.skip_zones()

        all_visible = self.read_header('<B', 1)
        fog_of_war = self.read_header('<B', 1)

        terrain = self.read(TerrainAnalyzer, [self.map_size_x, self.map_size_y])

        self.skip_obstructions()
        self.skip_visibility_map()

        self.position += 4
        num_data = self.read_header('<l', 4)
        self.position += num_data * 27

        return {
            'map_size': [self.map_size_x, self.map_size_y],
            'all_visible': all_visible,
            'fog_of_war': fog_of_war,
            'terrain': terrain,
        }

    def skip_zones(self):
        num_map_zones = self.read_header('<l', 4)
        size = self.map_size_x * self.map_size_y
        for i in range(0, num_map_zones):
            if self.version.sub_version >= 11.93:
                self.position += 2048 + size * 2
            else:
                self.position += 1275 + size

            num_floats = self.read_header('<l', 4)
            self.position += (num_floats * 4) + 4

    def skip_obstructions(self):
        num_data = self.read_header('<l', 4)
        self.position += 4  # Some ID relating to the previous line...
        self.position += num_data * 4
        for i in range(0, num_data):
            num_obstructions = self.read_header('<l', 4)
            # Two signed int32s.
            self.position += num_obstructions * 8

    def skip_visibility_map(self):
        map_size_x = self.read_header('<l', 4)
        map_size_y = self.read_header('<l', 4)
        # Visibility map. Can we use this for something?
        self.position += map_size_x * map_size_y * 4
