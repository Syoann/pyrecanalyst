import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame

class MapNameTest(unittest.TestCase):
    def test_custom_map_name_extract(self):
        rec = RecordedGame(os.path.join(os.path.dirname(__file__), 'recs/game-settings/[AoFE-FF DE R1] RoOk_FaLCoN - [Pervert]Moneimon (pov) G1.mgz'))
        self.assertEqual(rec.game_settings().map_name(), 'Acropolis')
        self.assertEqual(rec.game_settings().map_name({
            'extract_rms_name': False
        }), 'Custom')

    def test_non_english_map_name_extract(self):
        rec = RecordedGame(os.path.join(os.path.dirname(__file__), 'recs/game-settings/rec.20140311-034826.mgz'))
        self.assertEqual(rec.game_settings().map_name(), 'Golden Pit')
        self.assertEqual(rec.game_settings().map_name({
            'extract_rms_name': False
        }), 'Custom')
