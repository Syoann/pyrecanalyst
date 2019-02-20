import math
import re
import struct

from Analyzers.Analyzer import Analyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer
from Analyzers.PlayerMetaAnalyzer import PlayerMetaAnalyzer
from Analyzers.PostgameDataAnalyzer import PostgameDataAnalyzer
from Model.Resource import Resource
from Model.Tribute import Tribute
from Model.ChatMessage import ChatMessage
from ResourcePacks.AgeofEmpires.Civilization import Civilization


class Analysis(object):
    def __init__(self):
        self.duration = None
        self.tributes = None
        self.chat_messages = None
        self.units = None
        self.buildings = None
        self.post_game_data = None


class BodyAnalyzer(Analyzer):
    """Analyzer for most things in a recorded game file body."""
    # Operation ID of in-game commands.
    OP_COMMAND = int('0x01', 16)

    # Operation ID of sync packets.
    OP_SYNC = int('0x02', 16)

    # Operation ID of "meta" operations like the start of the game or chat
    # messages.
    OP_META = int('0x03', 16)

    # Same as OP_META, but not quite?
    OP_META2 = int('0x04', 16)

    # Game start identifier.
    META_GAME_START = int('0x01F4', 16)

    # Chat message identifier.
    META_CHAT = -1

    # Resignation command ID.
    COMMAND_RESIGN = int('0x0b', 16)

    # Research command ID.
    COMMAND_RESEARCH = int('0x65', 16)

    # Unit training command ID.
    COMMAND_TRAIN = int('0x77', 16)

    # Unit training command ID (used by AIs).
    COMMAND_TRAIN_SINGLE = int('0x64', 16)

    # Building command ID.
    COMMAND_BUILD = int('0x66', 16)

    # Tribute command ID.
    COMMAND_TRIBUTE = int('0x6C', 16)

    # UserPatch post-game lobby data command ID.
    COMMAND_POSTGAME = int('0xFF', 16)

    # Feudal age research ID.
    RESEARCH_FEUDAL = 101

    # Castle age research ID.
    RESEARCH_CASTLE = 102

    # Imperial age research ID.
    RESEARCH_IMPERIAL = 103

    def __init__(self):
        # Game version information.
        self.version = None

        # Current game time in ms.
        self.current_time = 0

        # Tributes sent during the game.
        self.tributes = []

        # Chat messages sent during the game.
        self.chat_messages = []

        # Amount of units of each type built during the game.
        self.units = {}

        # Amount of buildings of each type built during the game.
        self.buildings = {}

        # Post-game data, such as achievements.
        self.post_game_data = None

    # Run the analysis.
    def run(self):
        pack = self.rec.get_resource_pack()
        self.version = self.get(VersionAnalyzer)
        version = self.version

        players = self.get(PlayerMetaAnalyzer)

        # The player number is used for chat messages.
        players_by_number = {}
        # The player index is used for game actions.
        players_by_index = {}
        for player in players:
            players_by_number[player.number] = player
            players_by_index[player.index] = player

        self.players_by_number = players_by_number

        size = len(self.body)

        self.position = 0
        while self.position < size - 3:
            operation_type = 0
            if version.is_mgl and self.position == 0:
                operation_type = self.OP_META2
            else:
                operation_type = self.read_body('<L', 4)

            if operation_type == self.OP_META or operation_type == self.OP_META2:
                command = self.read_body('<l', 4)
                if command == self.META_GAME_START:
                    self.process_game_start()
                elif command == self.META_CHAT:
                    self.process_chat_message()
            elif operation_type == self.OP_SYNC:
                # There are a lot of sync packets, so we get a significant
                # speedup just from doing this inline (and not in a separate
                # method), and by using `unpack` and manual position increments
                # instead of `read_body`.
                data = struct.unpack('<ll', self.body[self.position:self.position + 8])
                self.current_time += data[0]  # self.read_body('<l', 4)
                unknown = data[1]  # self.read_body('<l', 4)
                if unknown == 0:
                    self.position += 28

                self.position += 20
            elif operation_type == self.OP_COMMAND:
                length = self.read_body('<l', 4)
                next_position = self.position + length
                command = self.body[self.position]
                self.position += 1

                # player resign
                if command == self.COMMAND_RESIGN:
                    player_number = int(self.body[self.position + 1])
                    disconnected = int(self.body[self.position + 2])
                    self.position += 3

                    player = players_by_index[player_number]

                    if player and player.resign_time == 0:
                        player.resign_time = self.current_time
                        message = player.name + ' resigned'
                        self.chat_messages.append(ChatMessage(self.current_time, None, message))
                # research
                elif command == self.COMMAND_RESEARCH:
                    self.position += 3
                    building_id = self.read_body('<l', 4)
                    player_id = self.read_body('<H', 2)
                    research_id = self.read_body('<H', 2)
                    player = players_by_index[player_id]

                    if not player:
                        break

                    if research_id == self.RESEARCH_FEUDAL:
                        research_duration = 130000
                        player.feudal_time = self.current_time + research_duration
                    elif research_id == self.RESEARCH_CASTLE:
                        # persians have faster research time
                        research_duration = 160000
                        if player.civ_id == Civilization.PERSIANS:
                            research_duration /= 1.10
                        player.castle_time = self.current_time + round(research_duration)
                    elif research_id == self.RESEARCH_IMPERIAL:
                        research_duration = 190000
                        if player.civ_id == Civilization.PERSIANS:
                            research_duration /= 1.15
                        player.imperial_time = self.current_time + round(research_duration)
                    player.add_research(research_id, self.current_time)
                # training unit
                elif command == self.COMMAND_TRAIN:
                    self.position += 3
                    building_id = self.read_body('<l', 4)
                    unit_type = self.read_body('<H', 2)
                    amount = self.read_body('<H', 2)

                    if unit_type not in self.units:
                        self.units[unit_type] = amount
                    else:
                        self.units[unit_type] += amount
                # AI trains unit
                elif command == self.COMMAND_TRAIN_SINGLE:
                    self.position += 9
                    unit_type = self.read_body('<H', 2)
                    if unit_type not in self.units:
                        self.units[unit_type] = 1
                    else:
                        self.units[unit_type] += 1
                # building
                elif command == self.COMMAND_BUILD:
                    self.position += 1
                    player_id = self.read_body('<H', 2)
                    self.position += 8
                    building_type = self.read_body('<H', 2)

                    building_type = pack.normalize_unit(building_type)

                    if player_id not in self.buildings:
                        self.buildings[player_id] = {}

                    if building_type not in self.buildings[player_id]:
                        self.buildings[player_id][building_type] = 1
                    else:
                        self.buildings[player_id][building_type] += 1
                # tributing
                elif command == self.COMMAND_TRIBUTE:
                    player_id_from = int(self.body[self.position])
                    self.position += 1
                    player_id_to = int(self.body[self.position])
                    self.position += 1
                    resource_id = int(self.body[self.position])
                    self.position += 1

                    player_from = players_by_index[player_id_from]
                    player_to = players_by_index[player_id_to]

                    if player_from and player_to:
                        amount = self.read_body('f', 4)
                        market_fee = self.read_body('f', 4)

                        tribute = Tribute()
                        tribute.time = self.current_time
                        tribute.player_from = player_from
                        tribute.player_to = player_to
                        tribute.resource = Resource(resource_id)
                        tribute.amount = math.floor(amount)
                        tribute.fee = market_fee
                        self.tributes.append(tribute)
                    else:
                        self.position += 8
                # multiplayer postgame data in UP1.4 RC2+
                elif command == self.COMMAND_POSTGAME:
                    self.post_game_data = self.read(PostgameDataAnalyzer)

                self.position = next_position

        ordered_chat_messages = []
        if self.chat_messages:
            ordered_chat_messages = sorted(self.chat_messages, key=lambda x: x.time)

        ordered_buildings = []
        if self.buildings:
            ordered_buildings = [(k, self.buildings[k]) for k in sorted(self.buildings.keys())]

        analysis = Analysis()
        analysis.duration = self.current_time
        analysis.tributes = self.tributes
        analysis.chat_messages = ordered_chat_messages
        analysis.units = self.units
        analysis.buildings = ordered_buildings
        analysis.post_game_data = self.post_game_data

        return analysis

    # Process the game start data. Not much here right now.
    def process_game_start(self):
        self.position += 20

        if self.version.is_mgl:
            self.position += 8
            ver = int(self.body[self.position])
            self.position += 4

    # Read a chat message.
    def process_chat_message(self):
        length = self.read_body('<l', 4)

        if length <= 0:
            return

        chat = self.read_body_raw(length).rstrip(b'\x00').decode('utf-8')

        # Chat messages are stored as "@#%dPlayerName: Message", where %d is a
        # digit from 1 to 8 indicating player's index (or colour).
        if re.match(r'@#[1-8]', chat):
            chat = chat.rstrip()
            player_number = int(chat[2])
            message = chat[3:]

            if message.startswith('--') and message.endswith('--'):
                # Skip messages like "--Warning: You are under attack... --"
                return
            elif player_number in self.players_by_number:
                player = self.players_by_number[player_number]
            else:
                # Shouldn't happen, but we'll let the ChatMessage factory
                # create a fake player for this message.
                # TODO that auto-create behaviour is probably not desirable...
                player = None

            self.chat_messages.append(ChatMessage.create(self.current_time, player, message))
