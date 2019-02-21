import struct

from Analyzers.Analyzer import Analyzer


class Aoe2RecordHeaderAnalyzer(Analyzer):
    def run(self):
        data = {}

        version = self.read_header('f', 4)  # float 1000, 1004, 1005, 1006...
        self.position += 4  # int 1000


        # Unknown, AoK HD.exe string "mrefDlcOptions" may be related.
        self.position += 4

        datasets_count = self.read_header('<l', 4)
        datasets = []
        for i in range(0, datasets_count):
            # Not sure what these stand for yet.
            datasets.append(self.read_header('<l', 4))

        data['datasets'] = datasets
        data['difficulty'] = self.read_header('<l', 4)
        data['map_size'] = self.read_header('<l', 4)

        # Unknown value (added in HD 5.7)
        if version >= 1006.0:
            x = self.read_header('<l', 4)

        data['map_id'] = self.read_header('<l', 4)
        data['reveal_map'] = self.read_header('<l', 4)
        data['victory_type'] = self.read_header('<l', 4)
        data['starting_resources'] = self.read_header('<l', 4)
        data['starting_age'] = self.read_header('<l', 4)
        data['ending_age'] = self.read_header('<l', 4)
        data['game_type'] = self.read_header('<l', 4)

        # Separator
        self.position += 4

        if version == 1000.0:
            self.map_name = self.read_aoe2_record_string()
            self.read_aoe2_record_string()

        # Separator again
        self.position += 4

        data['game_speed'] = self.read_header('f', 4)
        data['treaty_length'] = self.read_header('<l', 4)
        data['pop_limit'] = self.read_header('<l', 4)
        data['num_players'] = self.read_header('<l', 4)


        num_players = data['num_players']

        # Maybe:
        #    unusedPlayerColor <- 8 one-byte flags?
        #    mVictory.getAmount() <- int?
        #
        self.position += 8

        # Separator.
        self.position += 4

        for key in ('trading_enabled', 'team_bonuses_disabled', 'randomize_positions',
                    'full_tech_tree_enabled', 'number_of_starting_units', 'teams_locked',
                    'speed_locked', 'is_multi_player', 'cheats_enabled', 'record_game_enabled',
                    'animals_enabled', 'predators_enabled'):
            data[key] = ord(str(self.header[self.position])) != 0
            self.position += 1

        # Separator.
        self.position += 4

        # Unknowns.
        self.position += 8


        if version >= 1006.0:
            # Version 12.50, patch 5.7, 5.8.
            players = self.read_players1006(version, num_players)
        elif version >= 1004.0:
            # Version 12.49, 12.50, maybe others.
            players = self.read_players1004(version, num_players)
        else:
            separator = struct.pack('cccc', b'\xA3', b'\x5F', b'\x02', b'\x00')
            self.position = self.header.index(separator, self.position) + 4
            self.position = self.header.index(separator, self.position) + 4
            self.position += 10
            return data

        data['players'] = players

        # Unknown flag.
        self.position += 1
        data['fog_of_war_enabled'] = self.header[self.position]
        self.position += 1
        data['cheat_notifications_enabled'] = self.header[self.position]
        self.position += 1
        data['colored_chat_enabled'] = self.header[self.position]
        self.position += 1

        # Separator.
        self.position += 4

        data['is_ranked'] = self.header[self.position]
        self.position += 1
        data['allow_spectators'] = self.header[self.position]
        self.position += 1

        data['lobby_visibility'] = self.read_header('<l', 4)
        data['custom_random_map_file_crc'] = self.read_header('<l', 4)

        # Few unknown-ishes.
        self.read_aoe2_record_string()  # customScenarioOrCampaignFile
        self.position += 8
        self.read_aoe2_record_string()  # customRandomMapFile
        self.position += 8
        self.read_aoe2_record_string()  # customRandomMapScenarioFile
        self.position += 8

        data['guid'] = self.read_guid()
        data['gameTitle'] = self.read_aoe2_record_string()
        data['moddedDatasetTitle'] = self.read_aoe2_record_string()
        # Not sure if self should be inside the v1005.0 `if`.
        data['moddedDatasetWorkshopId'] = self.read_header('<Q', 8)

        if version >= 1005.0:
            self.read_aoe2_record_string()
            self.position += 4
        elif version >= 1004.0:
            self.position += 8

        # TODO decide on a format to output self stuff.
        return data


    def read_players1006(self, version, num_players):
        players = []
        for i in range(0, 8):
            if i >= num_players:
                # Skip empty players.
                self.position += 61
                continue

            self.position += 2

            # Unknown value
            unknown = self.header[self.position]  # Added in HD 5.7
            self.position += 1

            # Player's data
            player = {}

            # Hash of data files.
            player['dat_crc'] = self.read_header('<l', 4)
            player['mp_version'] = self.header[self.position]
            self.position += 1
            player['team_index'] = self.read_header('<l', 4)
            player['civ_id'] = self.read_header('<l', 4)
            player['ai_base_name'] = self.read_aoe2_record_string()
            player['ai_civ_name_index'] = int(self.header[self.position])
            self.position += 1
            player['unknown_name'] = self.read_aoe2_record_string()

            player['player_name'] = self.read_aoe2_record_string()
            player['humanity'] = self.read_header('<l', 4)
            player['steam_id'] = self.read_header('<Q', 8)
            player['player_index'] = self.read_header('<l', 4)
            player['unknown'] = self.read_header('<l', 4)  # Seems to be constant among all players so far...
            player['player_elo'] = self.read_header('<l', 4)  # Added in HD 5.7
            player['scenario_index'] = self.read_header('<l', 4)
            player['unknown_value'] = self.read_header('<l', 4)  # TODO: Determine what it stands for

            players.append(player)

        return players


    def read_players1004(self, version, num_players):
        players = []
        for i in range(0, 8):
            if i >= num_players:
                # Skip empty players.
                self.position += 48
                if version >= 1005.0:
                    self.position += 4
                continue

            self.position += 2

            # Player's data
            player = {}

            # Hash of data files.
            player['dat_crc'] = self.read_header('<l', 4)
            player['mp_version'] = self.header[self.position]
            self.position += 1
            player['team_index'] = self.read_header('<l', 4)
            player['civ_id'] = self.read_header('<l', 4)
            player['ai_base_name'] = self.read_aoe2_record_string()
            player['ai_civ_name_index'] = int(self.header[self.position])
            self.position += 1
            player['unknown_name'] = None
            if version >= 1005.0:
                player['unknown_name'] = self.read_aoe2_record_string()

            player['player_name'] = self.read_aoe2_record_string()
            player['humanity'] = self.read_header('<l', 4)
            player['steam_id'] = self.read_header('<Q', 8)
            player['player_index'] = self.read_header('<l', 4)
            player['unknown'] = self.read_header('<l', 4)  # Seems to be constant among all players so far...
            player['scenario_index'] = self.read_header('<l', 4)

            players.append(player)

        return players

    def read_aoe2_record_string(self):
        length = self.read_header('<H', 2)
        self.position += 2  # short 0x60 0xA0
        return self.read_header_raw(length)

    def read_guid(self):
        guid_data = struct.unpack('BBBBBBBBBBBBBBBB', self.read_header_raw(16))
        guid = ''
        for byte in guid_data:
            if byte < 16:
                guid += '0'
            guid += hex(byte)
        return guid
