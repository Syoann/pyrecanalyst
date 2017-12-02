class Version(object):
    # Version ID for unknown game versions.
    VERSION_UNKNOWN = 0

    # Version ID for the Age of Kings version.
    VERSION_AOK = 1

    # Version ID for the Age of Kings Trial version.
    VERSION_AOKTRIAL = 2

    #  Version ID for the Age of Kings base game, patch version 2.0.
    VERSION_AOK20 = 3

    # Version ID for the Age Of Kings base game, patch version 2.0a.
    VERSION_AOK20A = 4

    # Version ID for the Age of Conquerors expansion.
    VERSION_AOC = 5

    # Version ID for the Age of Conquerors expansion (Trial version).
    VERSION_AOCTRIAL = 6

    # Version ID for the Age of Conquerors expansion.
    VERSION_AOC10 = 7

    # Version ID for the Age Of Conquerors expansion, patch version 1.0c.
    VERSION_AOC10C = 8

    # Version ID for UserPatch + Forgotten Empires v2.1.
    VERSION_AOFE21 = 10

    # Version ID for UserPatch v1.1.
    VERSION_USERPATCH11 = 9

    # Version ID for UserPatch v1.2.
    VERSION_USERPATCH12 = 12

    # Version ID for UserPatch v1.3.
    VERSION_USERPATCH13 = 13

    # Version ID for UserPatch v1.4.
    VERSION_USERPATCH14 = 11

    # Version ID for UserPatch v1.5.
    VERSION_USERPATCH15 = 20

    # Version ID for HD Edition.
    VERSION_HD = 14

    # Version ID for HD Edition patch 4.3.
    VERSION_HD43 = 15

    # Version ID for HD Edition patch 4.6.
    VERSION_HD46 = 16

    # Version ID for HD Edition patch 4.7.
    VERSION_HD47 = 17

    # Version ID for HD Edition patch 4.8.
    VERSION_HD48 = 18

    # Version ID for HD Edition patch 5.0.
    VERSION_HD50 = 19

    def __init__(self, rec, version_string, sub_version):
        # Recorded game instance.
        self.rec = rec
        self.version_string = version_string
        self.sub_version = sub_version

    def name(self):
        """Get a localised version name."""
        return self.rec.trans('game_versions', self.version_string)
