import struct

from Analyzers.Analyzer import Analyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer
from Analyzers.PlayerObjectsListAnalyzer import PlayerObjectsListAnalyzer
from Model.Player import Player


class Players(object):
    def __init__(self):
        self.gaia = None
        self.players = []
        self.gaia_objects = []
        self.player_objects = []
        self.position = None


class PlayerInfoBlockAnalyzer(Analyzer):
    """
    Analyze extended player information blocks. Should only be composed with the
    HeaderAnalyzer for now.
    """

    def __init__(self, analysis):
        # Parent analysis.
        self.analysis = analysis

        # Game version information.
        self.version = None

        # Units owned by GAIA at the start of the game.
        self.gaia_objects = []

        # Units owned by players at the start of the game.
        self.player_objects = []

    def run(self):
        """Run the analysis."""
        self.version = self.get(VersionAnalyzer)

        # try:
        return self.analyze_extended()
        # except Exception as e:
        #     return self.analyze_simple()

    def analyze_extended(self):
        """Analyze an extended player info block, including unit data."""
        exist_object_separator = struct.pack('ccccccccc', '\x0B', '\x00', '\x08', '\x00', '\x00', '\x00', '\x02', '\x00', '\x00')

        pack = self.rec.get_resource_pack()

        (map_size_x, map_size_y) = self.analysis.map_size

        version = self.version
        players = self.analysis.players

        players_by_index = {}
        for player in players:
            players_by_index[player.index] = player

        # Add GAIA
        num_players = self.analysis.num_players + 1
        gaia = Player(self.rec)
        gaia.name = 'GAIA'

        # Player -1 is GAIA.
        players_with_gaia = list(players)

        players_with_gaia.insert(0, gaia)
        for player in players_with_gaia:
            # Co-op partners do not have an info block.
            if player.is_coop_partner():
                coop_main = player.get_coop_main()
                player.civ_id = coop_main.civ_id
                player.color_id = coop_main.color_id
                player.team = coop_main.team
                continue

            if version.is_trial:
                self.position += 4

            self.position += num_players + 43

            # skip playername
            player_name_len = self.read_header('<H', 2)

            self.position += player_name_len

            self.position += 1  # always 22?
            num_resources = self.read_header('l', 4)
            self.position += 1  # always 33?
            resources_end = self.position + 4 * num_resources

            # Interesting resources
            food = self.read_header('f', 4)
            wood = self.read_header('f', 4)
            stone = self.read_header('f', 4)
            gold = self.read_header('f', 4)

            # headroom = (house capacity - population)
            headroom = self.read_header('f', 4)
            self.position += 4
            # Post-Imperial Age = Imperial Age here
            starting_age = self.read_header('f', 4)
            self.position += 4 * 4
            population = self.read_header('f', 4)
            self.position += 25 * 4
            civilian_pop = self.read_header('f', 4)
            self.position += 2 * 4
            military_pop = self.read_header('f', 4)

            self.position = resources_end
            self.position += 1  # 1 byte

            init_camera_x = self.read_header('f', 4)
            init_camera_y = self.read_header('f', 4)
            if version.is_mgx:
                self.position += 9
            else:
                self.position += 5

            civilization = ord(self.header[self.position])
            self.position += 1

            if not civilization:
                civilization = 1
            self.position += 3

            player_color = ord(self.header[self.position])
            self.position += 1

            player.civ_id = civilization

            player.color_id = player_color
            player.initial_state.position = [round(init_camera_x), round(init_camera_y)]
            player.initial_state.food = round(food)
            player.initial_state.wood = round(wood)
            player.initial_state.stone = round(stone)
            player.initial_state.gold = round(gold)
            player.initial_state.starting_age = round(starting_age)
            player.initial_state.house_capacity = round(headroom) + round(population)
            player.initial_state.population = round(population)
            player.initial_state.civilian_pop = round(civilian_pop)
            player.initial_state.military_pop = round(military_pop)
            player.initial_state.extra_pop = player.initial_state.population - (player.initial_state.civilian_pop + player.initial_state.military_pop)

            if version.is_trial:
                self.position += 4

            self.position += num_players + 70
            if version.is_mgx:
                self.position += 792
            else:
                self.position += 756

            if version.is_mgx:
                self.position += 41249
            else:
                self.position += 34277

            self.position += map_size_x * map_size_y

            # getting exist_object_pos
            exist_object_pos = self.header.index(exist_object_separator, self.position+1)
            if not exist_object_pos:
                raise Exception('Could not find existObjectSeparator')
            else:
                self.position = exist_object_pos + len(exist_object_separator)

            players_by_index_with_gaia = players_by_index
            players_by_index_with_gaia.update({0: gaia})
            objects = self.read(PlayerObjectsListAnalyzer, {
                'players': players_by_index_with_gaia
            })

            for obj in objects.gaia_objects:
                self.gaia_objects.append(obj)

            for obj in objects.player_objects:
                self.player_objects.append(obj)

        p = Players()
        p.gaia = players[0]
        p.players = players[1:]
        p.gaia_objects = self.gaia_objects
        p.player_objects = self.player_objects

        return p

    def analyze_simple(self, e=None):
        """Analyze a simple player info block, in case the extended analysis fails."""
        raise Exception('Unimplemented', 0, e)
