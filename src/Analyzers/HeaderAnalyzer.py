import struct

from Model.Team import Team
from Model.ChatMessage import ChatMessage
from Model.GameSettings import GameSettings
from Model.GameInfo import GameInfo
from Analyzers.Analyzer import Analyzer
from Analyzers.PlayerInfoBlockAnalyzer import PlayerInfoBlockAnalyzer
from Analyzers.PlayerMetaAnalyzer import PlayerMetaAnalyzer
from Analyzers.MapDataAnalyzer import MapDataAnalyzer
from Analyzers.VictorySettingsAnalyzer import VictorySettingsAnalyzer
from Analyzers.Aoe2RecordHeaderAnalyzer import Aoe2RecordHeaderAnalyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer


class Analysis(object):
    def __init__(self):
        self.num_players = None
        self.map_size = None
        self.map_data = None
        self.scenario_filename = None
        self.messages = None
        self.victory = None
        self.teams = None
        self.pregame_chat = None
        self.game_settings = None
        self.game_info = None
        self.player_info = None


class HeaderAnalyzer(Analyzer):
    """Analyzer for most things in a recorded game file header."""

    def __init__(self, *args):
         self.args = args

    def run(self):
        """Run the analysis."""

        constant2 = struct.pack('cccccccc', b'\x9A', b'\x99', b'\x99', b'\x99', b'\x99', b'\x99', b'\xf9', b'\x3F')
        separator = struct.pack('cccc', b'\x9D', b'\xFF', b'\xFF', b'\xFF')
        scenario_constant = struct.pack('cccc', b'\xf6', b'\x28', b'\x9C', b'\x3F')
        aok_separator = struct.pack('cccc', b'\x9A', b'\x99', b'\x99', b'\x3F')
        aoe2record_scenario_separator = struct.pack('cccc', b'\xaE', b'\x47', b'\xa1', b'\x3F')
        aoe2record_header_separator = struct.pack('cccc', b'\xa3', b'\x5F', b'\x02', b'\x00')

        rec = self.rec
        self.analysis = Analysis()
        analysis = self.analysis

        players_by_index = {}
        game_type = -1

        size = len(self.header)
        self.position = 0

        self.version = self.read(VersionAnalyzer)
        version = self.version

        trigger_info_pos = self.header.rindex(constant2, self.position) + len(constant2)
        game_settings_pos = self.header[0:trigger_info_pos].rindex(separator) + len(separator)
        scenario_separator = scenario_constant
        if version.is_aok:
            scenario_separator = aok_separator

        if version.is_aoe2_record:
            scenario_separator = aoe2record_scenario_separator

        scenario_header_pos = self.header.rfind(scenario_separator)
        if scenario_header_pos:
            scenario_header_pos -= 4

        if version.is_aoe2_record:
            aoe2record_header = self.read(Aoe2RecordHeaderAnalyzer)

        include_ai = self.read_header('<L', 4)
        if include_ai:
            self.skip_ai()

        self.position += 4
        if version.is_aoe2_record:
            self.position += 4
            game_speed = aoe2record_header['game_speed']
        else:
            game_speed = self.read_header('<l', 4)


        # These bytes contain the game speed again several times over, as ints
        # and as floats (On normal speed: 150, 1.5 and 0.15). Why?!
        self.position += 37
        pov = self.read_header('<H', 2)
        if version.is_aoe2_record:
            num_players = aoe2record_header['num_players']
            game_mode = aoe2record_header['is_multi_player']
            self.position += 4
        else:
            num_players = int(self.header[self.position])
            self.position += 1
            num_players -= 1
            # - 1, because player #0 is GAIA.
            if version.is_mgx:
                self.position += 1  # Is instant building enabled? (cheat "aegis")
                self.position += 1  # Are cheats enabled?

            game_mode = self.read_header('<H', 2)


        analysis.num_players = num_players

        self.position += 58
        old_pos = self.position

#        if version.is_aoe2_record:
#            self.position += 1

        for i in range(1, 2):
            try:
                self.position = old_pos + i
                map_data = self.read(MapDataAnalyzer)
                analysis.map_size = map_data["map_size"]

                if analysis.map_size[0] > 5 and analysis.map_size[0] == analysis.map_size[1]:
                    print(i)
                    print(analysis.map_size)
            except:
                pass

        # int. Value is 10060 in AoK recorded games, 40600 in AoC and on.
        self.position += 4

        player_info_pos = self.position

        self.analysis.scenario_filename = None

        if scenario_header_pos > 0:
            self.position = scenario_header_pos
            self.read_scenario_header()
            # Set game type here, it will be overwritten by data from the
            # recorded game settings later. In MGL files there is no game
            # type field in the recorded game, so self one will be used.
            game_type = GameSettings.TYPE_SCENARIO

        analysis.messages = self.read_messages()

        # Skip two separators to find the victory condition block.
        self.position = self.header.index(separator, self.position)
        self.position = self.header.index(separator, self.position + 4)

        analysis.victory = self.read(VictorySettingsAnalyzer)

        self.position = game_settings_pos + 8

        # TODO Is 12.3 the correct cutoff point?
        if version.sub_version >= 12.3:
            # TODO what are theeeese?
            self.position += 16

        if version.is_aoe2_record:
            # Always 0? Map ID is now in the aoe2record front matter and gets
            # parsed below.
            self.position += 4
            map_id = aoe2record_header['map_id']
        elif not version.is_aok:
            map_id = self.read_header('<l', 4)

        difficulty = self.read_header('<l', 4)
        lock_teams = self.read_header('<L', 4)

        players = self.read(PlayerMetaAnalyzer)

        for player in players:
            players_by_index[player.index] = player
            if player.index == pov:
                player.owner = True

        # Merge in player from the aoe2record header if it exists.
        # In some cases (eg. civ_id) the places where the data was originally stored is now empty,
        # with the data instead only being stored in the aoe2record header.
        # Other player analyzers will fall back to self data in those cases.
        if version.is_aoe2_record and 'players' in aoe2record_header:
            for i, player in enumerate(players):
                for key, value in aoe2record_header['players'].items():
                    setattr(player, key, value)

        analysis.players = players

        self.position = trigger_info_pos + 1
        self.skip_trigger_info()

        team_indices = {}
        for i in range(0, 8):
            team_indices[i] = self.header[self.position + i]

        for i, player in enumerate(analysis.players):
            player.team_index = team_indices[i] - 1

        self.position += 8

        restore = self.position

        self.position = player_info_pos
        player_info = self.read(PlayerInfoBlockAnalyzer, analysis)

        self.position = restore

        if version.sub_version < 12.3:
            self.position += 1

        reveal_map = self.read_header('<l', 4)

        self.position += 4
        map_size = self.read_header('<l', 4)
        pop_limit = self.read_header('<l', 4)

        if version.is_mgx:
            game_type = self.header[self.position]
            lock_diplomacy = self.header[self.position + 1]
            self.position += 2

        if version.sub_version >= 11.96:
            self.position += 1

        if version.is_hd_edition:
            self.position += 4

        pregame_chat = []
        if version.is_mgx:
            pregame_chat = self.read_chat(players)

        analysis.teams = self.build_teams(players)

        if version.is_user_patch:
            pop_lim = pop_limit * 25
        else:
            pop_lim = pop_limit

        game_settings = {'game_type': game_type,
                         'game_speed': game_speed,
                         'map_size': map_size,
                         'difficulty_level': difficulty,
                         # User_patch stores the actual population limit divided by 25.
                         'pop_limit': pop_lim}

        if not version.is_aok:
            game_settings.update({'map_id': map_id,
                                  'lock_diplomacy': lock_diplomacy})

        game_info = GameInfo(self.rec)

        analysis.map_data = map_data["terrain"]
        analysis.pregame_chat = pregame_chat
        analysis.game_settings = GameSettings(self.rec, game_settings)
        analysis.game_info = game_info
        analysis.player_info = player_info

        return analysis

    def read_chat(self, players):
        """
        Read a block containing chat messages.

        Chat block structure:
            int32 count
            Chat_message messages[count]
        Chat message structure:
            int32 length
            char contents[length]
        Not much data is encoded in the chat message structure, so we derive
        a lot of it from the `contents` string instead.
        """
        players_by_number = {}
        for player in players:
            players_by_number[player.number] = player

        messages = []
        message_count = self.read_header('<l', 4)
        for i in range(0, message_count):
            length = self.read_header('<l', 4)
            if length <= 0:
                continue

            chat = self.read_header_raw(length).decode('utf-8')

            # pre-game chat messages are stored as "@#%d_player_name: Message",
            # where %d is a digit from 1 to 8 indicating player's index (or
            # colour)
            if chat[0] == '@' and chat[1] == '#' and chat[2] >= '1' and chat[2] <= '8':
                chat = chat.rstrip(' \x00')  # throw None-termination character
                if int(chat[2]) in players_by_number:
                    player = players_by_number[int(chat[2])]
                else:
                    # self player left before the game started
                    player = None

                messages.append(ChatMessage.create(None, player, chat[3:]))

        return messages

    def skip_ai(self):
        version = self.version

        # String table
        self.position += 2
        num_ai_strings = self.read_header('<H', 2)
        self.position += 4
        for i in range(0, num_ai_strings):
            length = self.read_header('<l', 4)
            self.position += length

        self.position += 6

        # Compiled script
        # Compute size of a single AI rule. A rule can contain conditions and
        # actions, with 4 integer parameters each. A rule can have 16
        action_size = (
            4 +  # int type
            2 +  # id
            2 +  # unknown
            4 * 4  # params
        )
        rule_size = (
            12 +  # unknown
            1 +  # number of facts
            1 +  # number of facts + actions
            2 +  # unknown
            action_size * 16
        )

        # For HD Edition's MGX2 files.
        if version.is_hd_patch4:
            # TODO what's in self? More actions, perhaps?
            rule_size += 0x180

        for i in range(0, 8):
            self.position += (
                4 +  # int unknown
                4 +  # int seq
                2  # max rules, constant
            )
            num_rules = self.read_header('<H', 2)
            self.position += 4
            for j in range(0, num_rules):
                self.position += rule_size

        self.position += 104  # unknown
        self.position += 10 * 4 * 8  # timers: 10 ints * 8 players
        self.position += 256 * 4  # shared goals: 256 ints
        self.position += 4096  # ???
        if version.sub_version >= 11.96:
            self.position += 1280  # ???

        # TODO is self the correct cutoff point?
        if version.sub_version >= 12.3:
            # The 4 bytes here are likely actually somewhere in between one
            # of the skips above.
            self.position += 4

    def skip_trigger_info(self):
        """
        Skip a scenario triggers info block. See Scenario_triggers_analyzer for
        contents of a trigger block.
        """
        # Effects and triggers are of variable size, but conditions are
        # constant.
        condition_size = (
            (11 * 4) +  # 11 ints
            (4 * 4) +  # area (4 ints)
            (3 * 4)  # 3 ints
        )

        if self.version.is_hd_patch4:
            condition_size += 2 * 4  # 2 ints

        num_triggers = self.read_header('<l', 4)
        for i in range(0, num_triggers):
            self.position += 4 + (2 * 1) + (3 * 4)  # int, 2 bools, 3 ints
            description_length = self.read_header('<l', 4)
            # HD edition 4.x saves a length of -1 when the string is absent,
            # whereas older versions would use 0. That used to work fine
            # without self guard, but now we should only skip if the length is
            # positive.
            if description_length > 0:
                self.position += description_length

            name_length = self.read_header('<l', 4)
            if name_length > 0:
                self.position += name_length

            num_effects = self.read_header('<l', 4)
            for j in range(0, num_effects):
                self.position += 6 * 4  # 6 ints
                num_selected_objects = self.read_header('<l', 4)
                if num_selected_objects == -1:
                    num_selected_objects = 0

                self.position += 9 * 4  # 9 ints
                self.position += 2 * 4  # location (2 ints)
                self.position += 4 * 4  # area (2 locations)
                self.position += 3 * 4  # 3 ints
                if self.version.is_hd_patch4:
                    self.position += 4  # int for the new Attack Stance effect

                text_length = self.read_header('<l', 4)
                if text_length > 0:
                    self.position += text_length

                sound_file_name_length = self.read_header('<l', 4)
                if sound_file_name_length > 0:
                    self.position += sound_file_name_length

                self.position += num_selected_objects * 4  # unit IDs (one int each)

            self.position += num_effects * 4  # effect order (list of ints)
            num_conditions = self.read_header('<l', 4)
            self.position += num_conditions * condition_size  # conditions
            self.position += num_conditions * 4  # conditions order (list of ints)

        if num_triggers > 0:
            self.position += num_triggers * 4  # trigger order (list of ints)
            # TODO perhaps also set game type to Scenario here?

    def read_scenario_header(self):
        """
        Read the scenario info header. Contains information about configured
        players and the scenario file.
        """
        next_unit_id = self.read_header('<l', 4)
        self.position += 4
        # Player names
        for i in range(0, 16):
            self.position += 256  # rtrim(read_header_raw(), \0)

        # Player names (string table)
        for i in range(0, 16):
            self.position += 4  # int

        for i in range(0, 16):
            self.position += 4  # bool is_active
            self.position += 4  # bool is_human
            self.position += 4  # int civilization
            self.position += 4  # const 0x00000004

        self.position += 5

        elapsed_time = self.read_header('<f', 4)
        name_len = self.read_header('<H', 2)
        filename = self.read_header_raw(name_len)

        # These should be string IDs for messages?
        if self.version.is_mgl:
            self.position += 20
        else:
            self.position += 24

        self.analysis.scenario_filename = filename

    def read_messages(self):
        """Read messages."""
        length = self.read_header('<H', 2)
        instructions = self.read_header_raw(length).rstrip(b'\x00').decode(errors='ignore') # FIXME
        length = self.read_header('<H', 2)
        hints = self.read_header_raw(length).rstrip(b'\x00').decode()
        length = self.read_header('<H', 2)
        victory = self.read_header_raw(length).rstrip(b'\x00').decode()
        length = self.read_header('<H', 2)
        loss = self.read_header_raw(length).rstrip(b'\x00').decode()
        length = self.read_header('<H', 2)
        history = self.read_header_raw(length).rstrip(b'\x00').decode()
        length = self.read_header('<H', 2)
        scouts = self.read_header_raw(length).rstrip(b'\x00').decode()
        return {'instructions': instructions,
                'hints': hints,
                'victory': victory,
                'loss': loss,
                'history': history,
                'scouts': scouts}

    def build_teams(self, players):
        """Group players into teams."""
        teams = []
        teams_by_index = {}
        for player in players:
            # Team = 0 can mean two things: either self player has no team,
            # i.e. is in a team on their own, or self player is cooping with
            # another player who _is_ part of a team.
            if player.team_index == 0:
                found = False
                for team in teams:
                    if team.index == player.team:
                        for coop_player in team.players:
                            if coop_player.index == player.index:
                                team.add_player(player)
                                found = True
                                break

                # Not a cooping player, so add them to their own team.
                if not found:
                    team = Team()
                    team.add_player(player)
                    teams.append(team)
                    team._index = player.team_index
            else:
                if player.team_index in teams_by_index:
                    teams_by_index[player.team_index].add_player(player)
                else:
                    team = Team()
                    team.add_player(player)
                    team._index = player.team_index
                    teams.append(team)

        return teams
