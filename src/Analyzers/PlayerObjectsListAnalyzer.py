import struct

from Analyzers.Analyzer import Analyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer
from Model.Unit import Unit

class Analysis(object):
    def __init__(self):
        self.gaia_objects = []
        self.player_objects = []


class PlayerObjectsListAnalyzer(Analyzer):
    """
    Reads a player objects list.

    TODO The different object types stack, so the data for a flag can be read by
    first calling the readEyeCandy() method, and then reading some extra data.
    Currently self class duplicates some reading logic in multiple methods, but
    they could reuse each other instead.
    """

    # Unit type ID.
    UT_EYECANDY = 10

    # Unit type ID.
    UT_FLAG = 20

    # Unit type ID.
    UT_DEAD_FISH = 30

    # Unit type ID.
    UT_BIRD = 40

    # Unit type ID.
    UT_UNKNOWN = 50

    # Unit type ID.
    UT_PROJECTILE = 60

    # Unit type ID.
    UT_CREATABLE = 70

    # Unit type ID.
    UT_BUILDING = 80

    def __init__(self, options):
        # Game version.
        self.version = None

        # Resource Pack.
        self.pack = None

        # Current unit object type. Always one of the UT_ constants above.
        self.object_type = -1

        # Player ID of the owner of the current object.
        self.owner_id = -1

        # Player model of the owner of the current object.
        self.owner = None

        # The current object's unit ID.
        self.unit_id = -1

        # GAIA objects that have been found. self currently only tracks objects
        # that will be drawn by the MapImage processor.
        self.gaia_objects = []

        # Player's units.
        self.player_objects = []

        # Players in self game, by index. Should be passed in as an argument to
        # self analyzer.
        self.players = options['players']

        # Magic byte string signifying the end of the data for a creatable or
        # building object data.
        self.object_end_separator = struct.pack('cccccccccccc', '\xFF', '\xFF', '\xFF', '\xFF', '\x00', '\x00', '\x80', '\xBF', '\x00', '\x00', '\x80', '\xBF') \
                                  + struct.pack('cccccccccccc', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF', '\xFF') \
                                  + struct.pack('cccccc', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00')
        # Magic byte string signifying the end of the data for a creatable or
        # building object data in Age of Kings.
        self.aok_object_end_separator = \
            struct.pack('ccccccccc', '\xFF', '\xFF', '\xFF', '\xFF', '\x00', '\x00', '\x80', '\xBF', '\x00') \
            + struct.pack('cccccccc', '\x00', '\x80', '\xBF', '\x00', '\x00', '\x00', '\x00', '\x00')
        # Magic byte string signifying the end of the list of player objects.
        self.player_info_end_separator = \
            struct.pack('cccccccccccc', '\x00', '\x0B', '\x00', '\x02', '\x00', '\x00', '\x00', '\x02', '\x00', '\x00', '\x00', '\x0B')
        # Magic byte string for... something?
        self.objects_mid_separator_gaia = \
            struct.pack('cccccccccc', '\x00', '\x0B', '\x00', '\x40', '\x00', '\x00', '\x00', '\x20', '\x00', '\x00')


    def run(self):
        self.version = self.get(VersionAnalyzer)
        self.pack = self.rec.get_resource_pack()
        done = False
        while not done:
            self.object_type = self.read_header('B', 1)

            self.owner = None
            self.ownerId = None
            if self.object_type:
                self.owner_id = self.read_header('B', 1)

                try:
                    self.owner = self.players[self.owner_id]
                except:
                    pass
            else:
                self.position += 1

            self.unit_id = self.read_header('<H', 2)

            if self.object_type == PlayerObjectsListAnalyzer.UT_EYECANDY:
                self.read_eye_candy()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_FLAG:
                # Flags, Map Revealers, ???, only tends to appear in
                # scenario games.
                self.read_flag()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_DEAD_FISH:
                self.read_dead_or_fish()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_PROJECTILE:
                # Should there be an objectType = 40 and objectType = 50 here?
                self.read_projectile()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_CREATABLE:
                self.read_creatable_unit()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_BUILDING:
                self.read_building()
            elif self.object_type == 0:
                self.position -= 4

                buff = self.read_header_raw(len(self.player_info_end_separator))
                if buff == self.player_info_end_separator:
                    done = True
                    break

                self.position -= len(self.player_info_end_separator)

                if buff[0] == self.objects_mid_separator_gaia[0] and buff[1] == self.objects_mid_separator_gaia[1]:
                    self.position += len(self.objects_mid_separator_gaia)
                else:
                    raise Exception('Could not find GAIA object separator')
            else:
                raise Exception('Unknown object type ' + str(self.object_type))

        analysis = Analysis()
        # TODO these probably don't need to be separate.
        analysis.gaia_objects = self.gaia_objects
        analysis.player_objects = self.player_objects
        return analysis


    def read_eye_candy(self):
        # Track GAIA objects for the map image generator.
        if self.pack.is_gaia_object(self.unit_id):
            restore = self.position
            self.position += 19
            pos_x = self.read_header('f', 4)
            pos_y = self.read_header('f', 4)
            self.position = restore
            go = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])
            self.gaia_objects.append(go)

        self.position += 63 - 4

        # TODO what's self?
        if self.version.is_hd_edition:
            self.position += 3

        if self.version.sub_version >= 12.49:
            self.position += 4

        if self.version.is_mgl:
            self.position += 1


    def read_flag(self):
        if self.version.is_hd_edition:
            self.position += 3

        if self.version.is_mgx:
            self.position += 59
            is_extended = ord(self.header[self.position])
            self.position += 1  # isExtended
            self.position += 4
            if is_extended == 2:
                self.position += 34
        else:
            self.position += 103 - 4

    def read_dead_or_fish(self):
        # TODO what's self?
        if self.version.is_hd_edition:
            self.position += 3

        if self.version.sub_version >= 12.49:
            self.position += 4

        if not self.version.is_mgx:
            self.position += 1

        is_extended = ord(self.header[self.position + 59])
        if is_extended == 2:
            self.position += 17

        self.position += 204 - 4

        if self.version.is_hd_patch4:
            self.position += 1

    def read_bird(self):
        b = ord(self.header[self.position + 204])
        self.position += 233 - 4

        if b:
            self.position += 67

    def read_creatable_unit(self):
        if self.pack.is_gaia_unit(self.unit_id):
            self.position += 19
            pos_x = self.read_header('f', 4)
            pos_y = self.read_header('f', 4)
            go = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])
            self.gaia_objects.append(go)
        elif self.owner:
            # These units belong to someone!
            self.position += 19
            pos_x = self.read_header('f', 4)
            pos_y = self.read_header('f', 4)
            uo = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])
            uo.owner = self.owner
            self.player_objects.append(uo)

        if self.version.is_mgx:
            separator_pos = self.header.index(self.object_end_separator, self.position)
            self.position = separator_pos + len(self.object_end_separator)
        else:
            separator_pos = self.header.index(self.aok_object_end_separator, self.position)
            self.position = separator_pos + len(self.aok_object_end_separator)

        if separator_pos == -1:
            raise Exception('Could not find object end separator')

    def read_building(self):
        if self.owner:
            self.position += 19
            pos_x = self.read_header('f', 4)
            pos_y = self.read_header('f', 4)
            uo = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])
            uo.owner = self.owner
            self.player_objects.append(uo)

        if self.version.is_mgx:
            separator_pos = self.header.index(self.object_end_separator, self.position)
            self.position = separator_pos + len(self.object_end_separator)
        else:
            separator_pos = self.header.index(self.aok_object_end_separator, self.position)
            self.position = separator_pos + len(self.aok_object_end_separator)

        if separator_pos == -1:
            raise Exception('Could not find object end separator')

        self.position += 126
        if self.version.is_mgx:
            self.position += 1

        if self.version.is_hd_patch4:
            self.position -= 4
