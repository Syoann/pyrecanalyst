import struct

from Model.Player import Player
from Analyzers.Analyzer import Analyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer


class PlayerMetaAnalyzer(Analyzer):
    """
    Analyze the small player metadata block. Can be composed or run
    independently.
    """
    def run(self):
        """Run the analysis."""
        is_composed = self.position > 0
        if not is_composed:
            # If self analyzer was not called from another analyzer at a
            # specific position, we find the correct position here.
            self.seek()
            return self.read(PlayerMetaAnalyzer)

        players = []
        # The first player in self list will be the "main" co-op player.
        coop_partners = {}
        for i in range(0, 9):
            player = self.read_player_meta(i)
            if player.human_raw == 0 or player.human_raw == 1:
                continue

            players.append(player)

            if not player.index in coop_partners:
                coop_partners[player.index] = []
            coop_partners[player.index].append(player)

        for player in players:
            player.set_coop_partners(coop_partners[player.index])

        return players

    def read_player_meta(self, i):
        """
        Reads a player meta info block for a single player. self just includes
        their nickname, index and "human" status. More information about
        players is stored later on in the recorded game file and is read by the
        PlayerInfoBlockAnalyzer.

        Player meta structure:
            int32 index
            int32 human # indicates whether player is AI/human/spectator
            uint32 nameLength
            char name[nameLength]
        """
        player = Player(self.rec)
        player.number = i
        player.index = self.read_header('<l', 4)

        human = self.read_header('<l', 4)
        length = self.read_header('<L', 4)

        if length:
            player.name = self.read_header_raw(length).decode('latin-1')
        else:
            player.name = ''

        player.human_raw = human
        player.human = (human == 2)
        player.spectator = (human == 6)

        return player

    def seek(self):
        """Find the position of the small player metadata block."""
        version = self.get(VersionAnalyzer)

        constant2 = struct.pack('cccccccc', b'\x9A', b'\x99', b'\x99', b'\x99', b'\x99', b'\x99', b'\xF9', b'\x3F')
        separator = struct.pack('cccc', b'\x9D', b'\xFF', b'\xFF', b'\xFF')

        players_by_index = {}

        size = len(self.header)
        self.position = 0

        trigger_info_pos = self.header.rfind(constant2, self.position) + len(constant2)
        game_settings_pos = self.header[:trigger_info_pos].rfind(separator) + len(separator)

        self.position = game_settings_pos + 8
        if not version.is_aok:
            # Skip Map ID.
            self.position += 4

        # Skip difficulty & diplomacy lock.
        self.position += 8

        # TODO Is 12.3 the correct cutoff point?
        if version.sub_version >= 12.3:
            # TODO what are theeeese?
            self.position += 16
