import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame
from Model.Version import Version
from Analyzers.VersionAnalyzer import VersionAnalyzer


class VersionAnalyzerTest(unittest.TestCase):
    def test_version(self):
        data = self.versions_provider()

        for case in data:
            file, expected_version, expected = case

            rec = RecordedGame(os.path.join(os.path.dirname(__file__), file))
            version = rec.run_analyzer(VersionAnalyzer())

            for prop, value in expected.items():
                try:
                    self.assertEqual(value, getattr(version, prop))
                except:
                    print("Expected {} of file {} to be {}".format(prop, file, str(value)))

    def versions_provider(self):
        return [
            ['./recs/versions/aok.mgl', Version.VERSION_AOK, {
                'is_mgl': True,
                'is_mgx': False,
                'is_mgz': False,
                'is_msx': False,
                'is_aok': True,
                'is_aoc': False,
                'is_aoe2_record': False,
                'is_hd_edition': False,
            }],
            ['./recs/versions/HD_test.mgx', Version.VERSION_HD, {
                'is_aoc': True,
                'is_hd_edition': True,
                'is_hd_patch4': False,
                'is_msx': False,
                'is_aoe2_record': False,
            }],
            ['./recs/versions/HD-FE.mgx2', Version.VERSION_HD, {
                'is_hd_edition': True,
                'is_hd_patch4': False,
                'is_msx': False,
                'is_aoe2_record': False,
            }],
            ['./recs/versions/mgx2_simple.mgx2', Version.VERSION_HD, {
                'is_hd_edition': True,
                'is_hd_patch4': True,
                'is_msx': False,
                'is_aoe2_record': False,
            }],
            ['./recs/versions/MP Replay v4.3 @2015.09.11 221142 (2).msx', Version.VERSION_HD43, {
                'is_hd_edition': True,
                'is_hd_patch4': True,
                'is_aoe2_record': False,
                'is_msx': True,
            }],
            ['./recs/versions/MP_Replay_v4.msx2', Version.VERSION_HD43, {
                'is_hd_edition': True,
                'is_hd_patch4': True,
                'is_aoe2_record': False,
                'is_msx': True,
            }],
            ['./recs/versions/SP Replay v4.6 @2016.05.05 130050.aoe2record', Version.VERSION_HD46, {
                'is_hd_edition': True,
                'is_hd_patch4': True,
                'is_aoe2_record': True,
            }]
        ]
