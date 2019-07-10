import struct

from pyrecanalyst.Model.Unit import Unit
from pyrecanalyst.Analyzers.Analyzer import Analyzer
from pyrecanalyst.Analyzers.VersionAnalyzer import VersionAnalyzer


class Analysis:
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
    UT_GENIE_STATIC = 10

    # Unit type ID.
    UT_TRIBE_TREE = 15

    # Unit type ID.
    UT_GENIE_ANIMATED = 20

    # Unit type ID.
    UT_GENIE_DOPPLE = 25

    # Unit type ID.
    UT_GENIE_MOVING = 30

    # Unit type ID.
    UT_GENIE_ACTION = 40

    # Unit type ID.
    UT_GENIE_COMBAT = 50

    # Unit type ID.
    UT_GENIE_MISSILE = 60

    # Unit type ID.
    UT_TRIBE_COMBAT = 70

    # Unit type ID.
    UT_TRIBE_BUILDING = 80

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
        self.object_end_separator = struct.pack('cccccccccccc', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\x00', b'\x00', b'\x80', b'\xBF', b'\x00', b'\x00', b'\x80', b'\xBF') \
                                  + struct.pack('cccccccccccc', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\xFF') \
                                  + struct.pack('cccccc', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00')
        # Magic byte string signifying the end of the data for a creatable or
        # building object data in Age of Kings.
        self.aok_object_end_separator = \
            struct.pack('ccccccccc', b'\xFF', b'\xFF', b'\xFF', b'\xFF', b'\x00', b'\x00', b'\x80', b'\xBF', b'\x00') \
            + struct.pack('cccccccc', b'\x00', b'\x80', b'\xBF', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00')
        # Magic byte string signifying the end of the list of player objects.
        self.player_info_end_separator = \
            struct.pack('cccccccccccc', b'\x00', b'\x0B', b'\x00', b'\x02', b'\x00', b'\x00', b'\x00', b'\x02', b'\x00', b'\x00', b'\x00', b'\x0B')
        # Magic byte string for... something?
        self.objects_mid_separator_gaia = \
            struct.pack('cccccccccc', b'\x00', b'\x0B', b'\x00', b'\x40', b'\x00', b'\x00', b'\x00', b'\x20', b'\x00', b'\x00')


    def run(self):
        self.version = self.get(VersionAnalyzer)
        self.pack = self.rec.get_resource_pack()

        while True:
            try:
                self.object_type = self.read_header('<B', 1)
            except Exception:
                break

            if self.object_type == PlayerObjectsListAnalyzer.UT_GENIE_STATIC:
                self.read_genie_static_obj()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_GENIE_ANIMATED:
                self.read_genie_animated()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_GENIE_DOPPLE:
                self.read_genie_dopple()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_GENIE_MOVING:
                self.read_genie_moving()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_GENIE_ACTION:
                self.read_genie_combat_obj()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_GENIE_MISSILE:
                self.read_genie_missile_obj()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_TRIBE_TREE:
                self.read_tribe_tree()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_TRIBE_COMBAT:
                self.read_tribe_combat()
            elif self.object_type == PlayerObjectsListAnalyzer.UT_TRIBE_BUILDING:
                self.read_tribe_building()
            elif self.object_type == 0:
                self.position -= 1

                buff = self.read_header_raw(len(self.player_info_end_separator))
                if buff == self.player_info_end_separator:
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

    def read_obj(self):
        self.owner_id = self.read_header('<B', 1)
        self.owner = self.players[self.owner_id]
        self.unit_id = self.read_header('<H', 2)


    # AOC sub_4CE690
    def read_genie_static_obj(self):
        self.read_obj()

        self.position += 2  # SpriteId
        self.position += 4  # InsideObjId
        self.position += 4  # HitPoints
        self.position += 1  # State
        self.position += 1  # SleepMode

        if self.version.sub_version >= 7.09:
            self.position += 1  # DoppleMode

        self.position += 1  # GoingToSleepMode
        self.position += 4  # Identity
        self.position += 1  # Facet

        pos_x = self.read_header('<f', 4)  # PositionX
        pos_y = self.read_header('<f', 4)  # PositionY

        unit = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])
        if self.pack.is_gaia_object(self.unit_id):
            # Track GAIA objects for the map image generator.
            self.gaia_objects.append(unit)
        elif self.owner:
            # These units belong to someone!
            unit.owner = self.owner
            self.player_objects.append(unit)

        self.position += 4  # PositionZ
        self.position += 2  # ScreenOffset0X
        self.position += 2  # ScreenOffset0Y
        self.position += 2  # ScreenOffset1X
        self.position += 2  # ScreenOffset1Y

        if self.version.sub_version < 11.58:
            self.position += 1  # SelectedGroup

        self.position += 2  # HeldAttributeId
        self.position += 4  # HeldAttributeAmount

        if self.version.is_hd_edition:  # HD made no version control for this cast! boohh...
            self.position += 4  # WorkerNum (32-bit)
        else:
            self.position += 1  # WorkerNum (8-bit)

        self.position += 1  # DamagePercent

        if self.version.sub_version >= 9.85:
            self.position += 1  # ???

        self.position += 1  # UnderAttack

        if self.version.sub_version < 10.85:
            self.position += 4  # GroupCommander
            self.position += 4  # GroupRange

        if self.version.sub_version == 6.99:
            self.position += 4  # Unused1A (float)
            self.position += 4  # Unused1B (float)
            self.position += 4  # Unused1C (float)
            self.position += 4  # Unused2
            self.position += 4  # Unused3A
            self.position += 4  # Unused3B

        if self.version.sub_version < 10.85:
            group_units_count = self.read_header('<l', 4)  # CommandingGroupUnitsCount
            self.position += group_units_count * 4  # CommandingGroupMembers

        group_units_count = self.read_header('<l', 4)  # GroupUnitsCount
        self.position += group_units_count * 4  # GroupMembers

        if self.version.sub_version >= 9.11 and self.version.sub_version <= 9.62:
            self.position += 4  # ???
        if self.version.sub_version >= 9.66:
            self.position += 4  # ??? (float)
        if self.version.sub_version >= 11.33:
            self.position += 1  # ???

        if self.version.sub_version >= 12.49:  # HD Edition
            self.position += 4  # ???

        act_spr_used = 1  # ActiveSpritesUsed
        if self.version.sub_version >= 11.11:
            act_spr_used = self.read_header('<b', 1)

        if act_spr_used:
            self.read_active_sprites()


    ACTIVE_SPRITE_TYPE_NORMAL = 1
    ACTIVE_SPRITE_TYPE_ANIMATED = 2

    # AOC sub_5ECAC0
    def read_active_sprites(self):
        active_sprite_type = self.read_header('<b', 1)
        while active_sprite_type:
            if active_sprite_type == self.ACTIVE_SPRITE_TYPE_NORMAL:
                self.read_active_sprite()
            elif active_sprite_type == self.ACTIVE_SPRITE_TYPE_ANIMATED:
                self.read_active_sprite_animated()

            if self.version.sub_version >= 9.23:
                self.position += 1  # ActiveSpriteNodeOrder
                self.position += 1  # ActiveSpriteNodeCount
                self.position += 1  # ActiveSpriteNodeUnknown
            active_sprite_type = self.read_header('<b', 1)

    # AOC sub_5EC030
    def read_active_sprite(self):
        self.position += 2  # SpriteId
        self.position += 4  # OffsetX
        self.position += 4  # OffsetY
        self.position += 2  # Facet
        self.position += 1  # Mode

    # AOC sub_5EC460
    def read_active_sprite_animated(self):
        self.read_active_sprite()
        self.position += 4  # Tempo (float)
        self.position += 4  # Unknown1 (float)
        self.position += 2  # Unknown2
        self.position += 1  # FrameEnd
        self.position += 1  # Looped
        self.position += 1  # Animating
        self.position += 4  # Unknown3 (float)

    # AOC sub_5ED420
    def read_genie_animated(self):
        self.read_genie_static_obj()
        self.position += 4  # Speed (float)


    # AOC sub_5A51A0
    def read_genie_dopple(self):
        self.read_genie_static_obj()

        self.position += 4  # DoppledSpawnPtr
        self.position += 1  # MapDrawLevel
        self.position += 4  # MapColor
        self.position += 4  # DoppledMasterPtr
        self.position += 4  # DoppledPlayerId

        if self.version.sub_version >= 7.06:
            self.position += 4  # FogFlag

        if self.version.sub_version >= 9.09:
            self.position += 1  # ???

    def read_genie_moving(self):
        self.read_genie_animated()

        self.position += 4  # TrailRemainder
        self.position += 4  # VelocityX
        self.position += 4  # VelocityY
        self.position += 4  # VelocityZ
        self.position += 4  # Angle
        self.position += 4  # TurnTowardsTime
        self.position += 4
        self.position += 4
        self.position += 4
        self.position += 4
        self.position += 1
        self.position += 1

        if self.version.sub_version >= 9.58:
            self.position += 1

        unk_size = self.read_header('<l', 4)

        for _ in range(0, unk_size):
            self.read_unk_struct()

        if self.version.sub_version >= 10.10:
            unk_flag = self.read_header('<l', 4)
            if unk_flag == 1:
                self.read_unk_struct()

        unk_flag = self.read_header('<l', 4)
        if unk_flag == 1:
            self.read_waypoint()
            self.read_waypoint()

        self.read_waypoint()
        self.read_waypoint()
        self.read_waypoint()

        self.position += 4  # ???
        unk_size = self.read_header('<l', 4)
        for _ in range(0, unk_size):
            self.read_waypoint()  # Waypoints

        if self.version.sub_version >= 10.05:
            self.position += 4  # ???
            self.read_waypoint()
        if self.version.sub_version >= 10.06:
            self.position += 4  # ???
        if self.version.sub_version == 10.64:
            self.position += 4  # ???
        if self.version.sub_version >= 12.10:  # HD Edition
            self.position += 1  # ???

    def read_unk_struct(self):
        if self.version.sub_version >= 9.44:
            self.position += 4
        self.position += 4
        self.position += 4
        self.position += 4
        self.position += 4
        if self.version.sub_version >= 10.20:
            self.position += 4
        if self.version.sub_version >= 10.24:
            self.position += 4
        self.position += 4
        self.position += 4
        self.position += 4
        self.position += 4
        self.position += 4
        if self.version.sub_version >= 10.25:
            self.position += 4
        if self.version.sub_version >= 12.10:  # HD Edition
            self.position += 4

    # AoK way-points are supposed to be 12 bytes in length.
    # AoE way-points were 16 bytes in length as they had "NextFacet" property.
    def read_waypoint(self, read_next_facet=False):
        self.position += 4  # X (float)
        self.position += 4  # Y (float)
        self.position += 4  # Z (float)

        if read_next_facet:
            self.position += 4  # NextFacet

    def read_genie_action_obj(self):
        self.read_genie_moving()

        self.position += 1  # Waiting
        if self.version.sub_version >= 6.50:
            self.position += 1  # CommandMode
        if self.version.sub_version >= 11.58:
            if self.version.sub_version >= 11.90:
                self.position += 4  # ??? (32-bit)
            else:
                self.position += 2  # ??? (16-bit)
        self.read_actions()

    # AOC(00.07.26.0809) sub_5CDA10
    def read_genie_combat_obj(self):
        self.read_genie_action_obj()

        if self.version.sub_version >= 9.05:
            self.position += 1  # ???
            self.position += 1  # ???
            self.position += 1  # ???
        self.position += 4  # AttackTimer (float)
        if self.version.sub_version >= 2.01:
            self.position += 1  # ???
        if self.version.sub_version >= 9.09:
            self.position += 1  # ???
            self.position += 1  # ???
        if self.version.sub_version >= 10.02:
            self.position += 4  # ???

    # AOC sub_57A5A0
    def read_genie_missile_obj(self):
        self.read_genie_combat_obj()

        if self.version.sub_version > 7.09:
            self.position += 4  # RangeMax (float)

        master_parsed = 0
        if self.version.sub_version >= 10.37:
            self.position += 4  # ??? maybe missile_master_id...
            master_parsed = self.read_header('<l', 4)

        if master_parsed:
            master_type = self.read_header('b', 1)
            # TODO: read master object for missile type
            # self.read_master_missile_object()

    def read_tribe_tree(self):
        self.read_genie_static_obj()
        # yep, nothing else is read...


    # TODO: need to fix this function
    def read_tribe_combat(self):
        self.read_obj()

        self.position += 19
        pos_x = self.read_header('<f', 4)
        pos_y = self.read_header('<f', 4)
        unit = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])

        if self.pack.is_gaia_unit(self.unit_id):
            self.gaia_objects.append(unit)
        elif self.owner:
            unit.owner = self.owner
            self.player_objects.append(unit)

        separator = self.aok_object_end_separator
        if self.version.is_mgx:
            separator = self.object_end_separator

        separator_pos = self.header.index(separator, self.position)
        self.position = separator_pos + len(separator)

        if separator_pos == -1:
            raise 'Could not find object end separator'

    # TODO: need to fix this function
    def read_tribe_building(self):
        self.read_obj()

        if self.owner:
            self.position += 19
            pos_x = self.read_header('f', 4)
            pos_y = self.read_header('f', 4)
            unit = Unit(self.rec, self.unit_id, [round(pos_x), round(pos_y)])
            unit.owner = self.owner
            self.player_objects.append(unit)

        separator = self.aok_object_end_separator
        if self.version.is_mgx:
            separator = self.object_end_separator

        separator_pos = self.header.index(separator, self.position)
        self.position = separator_pos + len(separator)


        if separator_pos == -1:
            raise "Could not find object end separator"

        self.position += 126
        if self.version.is_mgx:
            self.position += 1

        if self.version.is_hd_patch4:
            self.position -= 4


    # AOC sub_601510
    def read_actions(self):
        action_type = self.read_header('<h', 2)
        while action_type:
            self.read_actions_for_tribe(action_type)
            action_type = self.read_header('<h', 2)


    ACTION_TYPE_GENIE_MOVE = 1
    ACTION_TYPE_GENIE_ENTER = 3
    ACTION_TYPE_GENIE_EXPLORE = 4
    ACTION_TYPE_GENIE_GATHER = 5
    ACTION_TYPE_GENIE_GRAZE = 6
    ACTION_TYPE_GENIE_MISSILE = 8
    ACTION_TYPE_GENIE_ATTACK = 9
    ACTION_TYPE_GENIE_BIRD = 10
    ACTION_TYPE_GENIE_TRANSPORT = 12
    ACTION_TYPE_GENIE_GUARD = 13
    ACTION_TYPE_GENIE_MAKE = 21

    ACTION_TYPE_TRIBE_BUILD = 101
    ACTION_TYPE_TRIBE_SPAWN = 102
    ACTION_TYPE_TRIBE_RESEARCH = 103
    ACTION_TYPE_TRIBE_CONVERT = 104
    ACTION_TYPE_TRIBE_HEAL = 105
    ACTION_TYPE_TRIBE_REPAIR = 106
    ACTION_TYPE_TRIBE_ARTIFACT = 107
    ACTION_TYPE_TRIBE_DISCOVERY = 108
    ACTION_TYPE_TRIBE_EXPLORE = 109
    ACTION_TYPE_TRIBE_HUNT = 110
    ACTION_TYPE_TRIBE_TRADE = 111

    ACTION_TYPE_TRIBE_WONDER = 120
    ACTION_TYPE_TRIBE_FARM = 121
    ACTION_TYPE_TRIBE_GATHER = 122
    ACTION_TYPE_TRIBE_HOUSING = 123
    ACTION_TYPE_TRIBE_PACK = 124
    ACTION_TYPE_TRIBE_UNPACK = 125

    ACTION_TYPE_TRIBE_MERCHANT = 131
    ACTION_TYPE_TRIBE_PICKUP = 132
    ACTION_TYPE_TRIBE_CHARGE = 133
    ACTION_TYPE_TRIBE_TRANSFORM = 134
    ACTION_TYPE_TRIBE_CAPTURE = 135
    ACTION_TYPE_TRIBE_DELIVER = 136
    ACTION_TYPE_TRIBE_SHEPHERD = 149

    # AOC(00.07.26.0809) sub_601600
    def read_actions_for_genie(self, action_type):
        if action_type == self.ACTION_TYPE_GENIE_GRAZE:
            self.read_action_genie_graze()
        elif action_type == self.ACTION_TYPE_GENIE_ATTACK:
            self.read_action_genie_attack()
        elif action_type == self.ACTION_TYPE_GENIE_BIRD:
            self.read_action_genie_bird()
        elif action_type == self.ACTION_TYPE_GENIE_EXPLORE:
            self.read_action_genie_explore()
        elif action_type == self.ACTION_TYPE_GENIE_GATHER:
            self.read_action_genie_gather()
        elif action_type == self.ACTION_TYPE_GENIE_MISSILE:
            self.read_action_genie_missile()
        elif action_type == self.ACTION_TYPE_GENIE_MOVE:
            self.read_action_genie_move()
        elif action_type == self.ACTION_TYPE_GENIE_MAKE:
            self.read_action_genie_make()
        elif action_type == self.ACTION_TYPE_GENIE_GUARD:
            self.read_action_genie_guard()
        else:
            raise "Error in action type !"

    # AOC sub_4B1A20
    def read_actions_for_tribe(self, action_type):
        if action_type == self.ACTION_TYPE_GENIE_TRANSPORT:
            self.read_action_genie_transport()
        elif action_type == self.ACTION_TYPE_GENIE_ENTER:
            self.read_action_genie_enter()
        # The following Action instances are from Tribe:
        elif action_type == self.ACTION_TYPE_TRIBE_BUILD:
            self.read_action_tribe_build()
        elif action_type == self.ACTION_TYPE_TRIBE_SPAWN:
            self.read_action_tribe_spawn()
        elif action_type == self.ACTION_TYPE_TRIBE_RESEARCH:
            self.read_action_tribe_research()
        elif action_type == self.ACTION_TYPE_TRIBE_CONVERT:
            self.read_action_tribe_convert()
        elif action_type == self.ACTION_TYPE_TRIBE_HEAL:
            self.read_action_tribe_heal()
        elif action_type == self.ACTION_TYPE_TRIBE_REPAIR:
            self.read_action_tribe_repair()
        elif action_type == self.ACTION_TYPE_TRIBE_ARTIFACT:
            self.read_action_tribe_artifact()
        elif action_type == self.ACTION_TYPE_TRIBE_DISCOVERY:
            self.read_action_tribe_discovery()
        elif action_type == self.ACTION_TYPE_TRIBE_EXPLORE:
            self.read_action_tribe_explore()
        elif action_type == self.ACTION_TYPE_TRIBE_HUNT:
            self.read_action_tribe_hunt()
        elif action_type == self.ACTION_TYPE_TRIBE_TRADE:
            self.read_action_tribe_trade()
        elif action_type == self.ACTION_TYPE_TRIBE_WONDER:
            self.read_action_tribe_wonder()
        elif action_type == self.ACTION_TYPE_TRIBE_FARM:
            self.read_action_tribe_farm()
        elif action_type == self.ACTION_TYPE_TRIBE_GATHER:
            self.read_action_tribe_gather()
        elif action_type == self.ACTION_TYPE_TRIBE_HOUSING:
            self.read_action_tribe_housing()
        elif action_type == self.ACTION_TYPE_TRIBE_PACK:
            self.read_action_tribe_pack()
        elif action_type == self.ACTION_TYPE_TRIBE_UNPACK:
            self.read_action_tribe_unpack()
        elif action_type == self.ACTION_TYPE_TRIBE_MERCHANT:
            self.read_action_tribe_merchant()
        elif action_type == self.ACTION_TYPE_TRIBE_PICKUP:
            self.read_action_tribe_pickup()
        elif action_type == self.ACTION_TYPE_TRIBE_CHARGE:
            self.read_action_tribe_charge()
        elif action_type == self.ACTION_TYPE_TRIBE_TRANSFORM:
            self.read_action_tribe_transform()
        elif action_type == self.ACTION_TYPE_TRIBE_CAPTURE:
            self.read_action_tribe_capture()
        elif action_type == self.ACTION_TYPE_TRIBE_DELIVER:
            self.read_action_tribe_deliver()
        elif action_type == self.ACTION_TYPE_TRIBE_SHEPHERD:
            self.read_action_tribe_sheperd()
        else:
            self.read_actions_for_genie(action_type)

     # AOC sub_5FDA30
    def read_action(self):
        self.position += 1  # State
        self.position += 4  # TargetSpawnPtr1
        self.position += 4  # TargetSpawnPtr2
        self.position += 4  # TargetSpawnId1
        self.position += 4  # TargetSpawnId2
        self.position += 4  # TargetSpawnAxisX
        self.position += 4  # TargetSpawnAxisY
        self.position += 4  # TargetSpawnAxisZ
        self.position += 4  # Timer

        if self.version.sub_version >= 9.92:
            self.position += 1  # ???
        self.position += 2  # TaskId
        self.position += 1  # SubActionValue
        self.read_actions()  # SubActions
        self.position += 2  # SpriteId

    def read_action_genie_graze(self):
        self.read_action()

    # AOC sub_605370
    def read_action_genie_attack(self):
        self.read_action()
        self.position += 4  # RangeMax (float)
        self.position += 4  # RangeMin (float)
        self.position += 2  # MissileMasterId
        self.position += 2  # MissileAtFrame
        self.position += 1  # NeedToAttack
        self.position += 1  # WasSameOwner
        self.position += 1  # IndirectFireMode
        self.position += 2  # MoveSpriteId
        self.position += 2  # FightSpriteId
        self.position += 2  # WaitSpriteId
        if self.version.sub_version >= 9.02:
            self.position += 4  # PositionX (float)
            self.position += 4  # PositionY (float)
            self.position += 4  # PositionZ (float)

    def read_action_genie_explore(self):
        self.read_action()

    def read_action_genie_guard(self):
        self.read_action()

    # AOC sub_601280
    def read_action_genie_make(self):
        self.read_action()
        if self.version.sub_version >= 9.41:
            self.position += 4  # ??? (float) (what is this? it's set to 120.0 by default)

    # AOC sub_5FFC10
    def read_action_genie_move(self):
        self.read_action()
        self.position += 4  # Range (float)

    def read_action_genie_bird(self):
        self.read_action()

    # AOC sub_602060
    def read_action_genie_gather(self):
        self.read_action()
        self.position += 4  # Classifier
        if self.version.sub_version >= 9.01:
            self.position += 1  # ???
            self.position += 1  # ???
            self.position += 4  # AttributeFactor (float)
            self.position += 4  # ???
            self.position += 1  # ???
            self.position += 1  # ???
        if self.version.sub_version >= 11.57:
            self.position += 4  # DepositAxisX (float)
            self.position += 4  # DepositAxisY (float)

    # AOC sub_600350
    def read_action_genie_missile(self):
        self.read_action()
        self.position += 4  # VelocityX (float)
        self.position += 4  # VelocityY (float)
        self.position += 4  # VelocityZ (float)
        self.position += 4  # BallisticVelocity (float)
        self.position += 4  # BallisticAcceleration (float)
        if self.version.sub_version >= 10.29:
            self.position += 4  # ???

    def read_action_genie_transport(self):
        self.read_action()

    def read_action_genie_enter(self):
        self.read_action()
        if self.version.sub_version >= 9.92:
            self.position += 4  # ???

    def read_action_tribe_build(self):
        self.read_action()
        if self.version.sub_version >= 10.47:
            self.position += 4  # ???

    # AOC sub_4B0A20
    def read_action_tribe_spawn(self):
        self.read_action()
        self.position += 2  # MasterId
        self.position += 4  # WorkDone
        self.position += 4  # UniqueId

    # AOC sub_4AC920
    def read_action_tribe_research(self):
        self.read_action()
        self.position += 2  # ResearchId
        self.position += 4  # UniqueId

    # AOC sub_4B76D0
    def read_action_tribe_convert(self):
        self.read_action()
        self.position += 1  # WasSameOwner
        self.position += 4  # RequiredRange (float)
        if self.version.sub_version >= 9.53:
            self.position += 4  # ??? (float)
        if self.version.sub_version >= 9.54:
            self.position += 1  # ???
            self.position += 1  # ???
            self.position += 4  # ???
        if self.version.sub_version >= 10.33:
            self.position += 4  # ???
            self.position += 4  # ???
            self.position += 4  # ??? (some offset to structure)

    def read_action_tribe_heal(self):
        self.read_action()

    # AOC sub_4AEAA0
    def read_action_tribe_repair(self):
        self.read_action()
        if self.version.sub_version >= 6.50:
            self.position += 1  # SaveTargetCommand
        if self.version.sub_version >= 10.47:
            self.position += 4  # ???

    def read_action_tribe_artifact(self):
        self.read_action()

    def read_action_tribe_discovery(self):
        self.read_action()
        num_players = 9
        self.position += 1 * num_players  # DiscoverOwners

    def read_action_tribe_explore(self):
        self.read_action()

    # AOC sub_4B2EE0
    def read_action_tribe_hunt(self):
        self.read_action()
        self.position += 4  # TargetMasterClass
        if self.version.sub_version >= 10.31:
            self.position += 4  # ???
            if self.version.sub_version >= 10.53:
                self.position += 1  # ???
            if self.version.sub_version >= 10.56:
                self.position += 4  # ??? (float)
            if self.version.sub_version >= 10.53:
                self.position += 2  # ???
                self.position += 4  # ??? (float)
                self.position += 4  # ??? (float)
                self.position += 4  # ??? (some offset to structure)

    # AOC sub_4AB8C0
    def read_action_tribe_trade(self):
        self.read_action()
        if self.version.sub_version >= 10.04:
            self.position += 1  # ???
            self.position += 4  # ???
            self.position += 4  # ???
        if self.version.sub_version >= 10.07:
            self.position += 4  # ??? (float)
            self.position += 4  # ??? (float)

    # AOC sub_4AA260
    def read_action_tribe_wonder(self):
        self.read_action()
        if self.version.sub_version >= 9.33:
            self.position += 4  # ??? (float) (internally set to 2000.0, possibly time)

        if self.version.sub_version >= 11.73:
            self.position += 1  # ???

    def read_action_tribe_farm(self):
        self.read_action()

    # AOC sub_4B53D0
    def read_action_tribe_gather(self):
        self.read_action()
        self.position += 4  # GatherMasterId

    # AOC sub_4B2B80
    def read_action_tribe_housing(self):
        self.read_action()
        self.position += 4  # ???

    # AOC sub_4AF610
    def read_action_tribe_pack(self):
        self.read_action()
        self.position += 4  # ???
        self.position += 1  # ???
        if self.version.sub_version >= 10.27:
            self.position += 4  # ???

    # AOC sub_4AB130
    def read_action_tribe_unpack(self):
        self.read_action()
        self.position += 4  # ???
        self.position += 1  # ???
        if self.version.sub_version >= 9.40:
            self.position += 4  # ???:
        if self.version.sub_version >= 10.27:
            self.position += 4  # ???

    # AOC sub_4AFA80
    def read_action_tribe_merchant(self):
        self.read_action()
        self.position += 4  # ???
        self.position += 4  # ???

    # AOC sub_4B0380
    def read_action_tribe_pickup(self):
        self.read_action()

    # AOC sub_4AAB70
    def read_action_tribe_transform(self):
        self.read_action()
        self.position += 4  # Unknown

    # AOC sub_4B7220
    def read_action_tribe_charge(self):
        self.read_action()

    # AOC sub_4B8B70
    def read_action_tribe_capture(self):
        self.read_action()

    # AOC sub_4B1440
    def read_action_tribe_deliver(self):
        self.read_action()
        self.position += 1  # Unknown

    def read_action_tribe_sheperd(self):
        self.read_action()
