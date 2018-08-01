import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame
from Model.GameSettings import GameSettings
from Model.VictorySettings import VictorySettings
from Analyzers.HeaderAnalyzer import HeaderAnalyzer


class HeaderAnalyzerTest(unittest.TestCase):
    def load(self, path):
        return RecordedGame(os.path.join(os.path.dirname(__file__), path))

    def test_players(self):
        data = self.players_provider()

        for entry in data:
            f = entry[0]
            expected = entry[1]
            expected_count = entry[2]

            rec = self.load(f)
            analysis = rec.run_analyzer(HeaderAnalyzer())
            self.assertEqual(expected_count, analysis.num_players)

            for index, dic in enumerate(expected):
                for key, value in dic.iteritems():
                    if key == "is_cooping":
                        self.assertEqual(value, getattr(analysis.players[index], key)())
                    else:
                        self.assertEqual(value, getattr(analysis.players[index], key))

    def test_scenario_messages(self):
        rec = self.load('recs/scenario/scenario-with-messages.mgz')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        message_types = {
            # Identifiers embedded in the test game.
            'instructions': 'RECANALYST:INSTRUCTIONS\r\n\r\nDEMO SCENARIO INSTRUCTIONS',
            'hints': 'RECANALYST:HINTS\r\n\r\nSCENARIO HINTS',
            'loss': 'RECANALYST:LOSS\r\n\r\nDEMO LOSS',
            'victory': 'RECANALYST:VICTORY\r\n\r\nDEMO VICTORY',
            'scouts': 'RECANALYST:SCOUT\r\n\r\nDEMO SCOUTING INFORMATION',
            'history': 'RECANALYST:HISTORY\r\n\r\nDEMO HISTORY',
        }

        for type, expected in message_types.iteritems():
            self.assertEqual(expected, analysis.messages[type])

    def test_skipping_ai_info(self):
        """Test a game with multiple AI players."""
        rec = self.load('recs/ai/20141214_blutze(mong)+ffraid(pers) vs bots(goth+chin).mgx2')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        # Just check that we didn't crash.
        self.assertIsNotNone(analysis)

    def test_skipping_complex_trigger_info(self):
        """"
        Test a scenario with complex trigger info. self Age of Heroes beta
        version contains something like 700+ triggers.
        """
        rec = self.load('recs/scenario/age-of-heroes.mgz')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        # Just check that we didn't crash.
        self.assertIsNotNone(analysis)

    def test_aoe2_record_with_trigger_info(self):
        """Test a single-player campaign game in HD Edition Patch 4+."""
        rec = self.load('recs/versions/SP Replay v4.6 @2015.12.29 001221.aoe2record')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        # Just check that we didn't crash.
        self.assertIsNotNone(analysis)

    def test_aoe2_record(self):
        rec = self.load('recs/versions/HD Tourney r1 robo_boro vs Dutch Class g1.aoe2record')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        self.assertEqual(1, getattr(analysis.game_settings, 'lock_diplomacy'))
        self.assertEqual(GameSettings.LEVEL_EASIEST, getattr(analysis.game_settings, 'difficulty_level'))
        self.assertEqual(28, getattr(analysis.game_settings, 'map_id'))
        self.assertTrue('Conquest Game' in analysis.messages["instructions"])

    def test_aoe2_record_victory_settings(self):
        rec = self.load('recs/versions/HD Tourney r1 robo_boro vs Dutch Class g1.aoe2record')
        analysis = rec.run_analyzer(HeaderAnalyzer())

        self.assertEqual(VictorySettings.STANDARD, getattr(analysis.victory, 'mode'))
        self.assertEqual(900, getattr(analysis.victory, 'score_limit'))
        self.assertEqual(9000, getattr(analysis.victory, 'time_limit'))

    def test_aoe2_record_with_ai(self):
        """Skipping AI in HD edition 5.0."""
        rec = self.load('recs/versions/SP Replay v5.0 @2016.12.21 111710.aoe2record')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        # Just check that we didn't crash.
        self.assertIsNotNone(analysis)

    def test_chat(self):
        data = self.chat_counts_provider()

        for row in data:
            file = row[0]
            expected_count = row[1]

            rec = self.load(file)
            analysis = rec.run_analyzer(HeaderAnalyzer())
            self.assertEqual(expected_count, len(analysis.pregame_chat))

    def test_coop_chats(self):
        rec = self.load('recs/chat/TCC R5 Team Picon vs Combat Wombats G3.mgx2')
        analysis = rec.run_analyzer(HeaderAnalyzer())
        l = len(analysis.pregame_chat) - 1

        # Three performance warning notifications from different players:
        for i in range(2, 5):
            self.assertTrue(re.match("Performance warning: There is moderate latency between .* and .*\. This will hinder the speed of the match.", analysis.pregame_chat[l - i].msg))

        self.assertEqual('hf gl', analysis.pregame_chat[l - 1].msg)
        self.assertEqual('gl hf', analysis.pregame_chat[l].msg)

    def test_coops(self):
        rec = self.load('recs/coop/coop.mgx')
        players = rec.run_analyzer(HeaderAnalyzer()).players

        self.assertEqual(1, players[0].index)
        self.assertEqual(2, players[1].index)
        self.assertEqual(2, players[2].index)
        self.assertEqual(1, players[3].index)

        self.assertTrue(players[0].is_cooping())
        self.assertTrue(players[1].is_cooping())
        self.assertTrue(players[2].is_cooping())
        self.assertTrue(players[3].is_cooping())

        # Check that coop main/partner are defined correctly.
        self.assertTrue(players[0].is_coop_main())
        self.assertFalse(players[0].is_coop_partner())
        self.assertTrue(players[1].is_coop_main())
        self.assertFalse(players[1].is_coop_partner())
        self.assertTrue(players[2].is_coop_partner())
        self.assertFalse(players[2].is_coop_main())
        self.assertTrue(players[3].is_coop_partner())
        self.assertFalse(players[3].is_coop_main())

        rec = self.load('recs/FluffyFur+yousifr+TheBlackWinds+Mobius_One[Chinese]=VS=MOD3000+Chrazini+ClosedLoop+ [AGM]Wineup[Britons]_1v1_8PlayerCo-op_01222015.mgx2')
        players = rec.run_analyzer(HeaderAnalyzer()).players

        # Check that coop partners are collected correctly.
        partners = players[0].get_coop_partners()
        self.assertEqual(3, len(partners))
        partners = players[7].get_coop_partners()
        self.assertEqual(3, len(partners))

        # Check that coop mains are returned correctly.
        self.assertEqual(players[6].get_coop_main(), players[0])
        self.assertTrue(players[6] in players[0].get_coop_partners())

    def players_provider(self):
        return [
            ['./recs/versions/HD_test.mgx', [
                {'team_index': 3, 'name': 'ZeroEmpires'},
                {'team_index': 2, 'name': 'Befbeer'},
                {'team_index': 2, 'name': 'dark_knight1907'},
                {'team_index': 3, 'name': 'Idle Beaver'},
                {'team_index': 3, 'name': 'Hand Banana'},
                {'team_index': 3, 'name': 'Iso'},
                {'team_index': 2, 'name': 'JJEL'},
                {'team_index': 2, 'name': 'SudsNDeath'},
            ], 8],
            ['./recs/versions/aok.mgl', [
                {'team_index': 1, 'name': 'AoE2_K_Master'},
                {'team_index': 2, 'name': 'Elsakar'},
                {'team_index': 1, 'name': 'AOKH_Washizu'},
                {'team_index': 2, 'name': 'Baked_potato_'},
            ], 4],
            ['./recs/versions/up1.4.mgz', [
                {'name': 'Zuppi'},
                {'name': 'JorDan_23'},
            ], 2],
            ['./recs/versions/up1.5.mgz', [
                {'name': 'Myth'},
                {'name': 'Louis IX'},
                {'name': 'Athelred the Unready'},
            ], 3],
            ['./recs/ai/Lobsth_15-pop-scouts_ai.mgx', [
                {'name': 'Eternal Lobster'},
                {'name': 'Ernak the Hun'},
            ], 2],
            ['./recs/ai/20141214_blutze(mong)+ffraid(pers) vs bots(goth+chin).mgx2', [
                {'name': 'Purpleblutzicle'},
                {'name': 'Ffraid'},
                {'name': 'Li Shi-min'},
                {'name': 'Theodoric the Goth'},
            ], 4],
            ['./recs/FluffyFur+yousifr+TheBlackWinds+Mobius_One[Chinese]=VS=MOD3000+Chrazini+ClosedLoop+ [AGM]Wineup[Britons]_1v1_8PlayerCo-op_01222015.mgx2', [
                {'team_index': 1, 'is_cooping': True, 'name': 'Mobius One'},
                {'team_index': 2, 'is_cooping': True, 'name': 'MOD3000'},
                {'team_index': 1, 'is_cooping': True, 'name': 'TheBlackWinds'},
                {'team_index': 1, 'is_cooping': True, 'name': 'yousifr'},
                {'team_index': 2, 'is_cooping': True, 'name': 'Chrazini'},
                {'team_index': 2, 'is_cooping': True, 'name': 'ClosedLoop'},
                {'team_index': 1, 'is_cooping': True, 'name': 'FluffyFur'},
                {'team_index': 2, 'is_cooping': True, 'name': '[AGM]Wineup'},
            ], 2],
            ['./recs/versions/HD Tourney r1 robo_boro vs Dutch Class g1.aoe2record', [
                {'name': 'Dutch Class', 'color_id': 0},
                {'name': 'robo_boro', 'color_id': 4},
            ], 2],
            ['./recs/versions/Kingdoms Britons v Britons - SP Replay v4.6 @2016.05.05 130519.aoe2record', [
                {'civ_id': 1, 'name': 'Idle Beaver'},
                {'civ_id': 1, 'name': 'Duke of Normandy (AI)'},
            ], 2],
            ['./recs/versions/MP_Replay_v4.8_2016.11.03_221821_2.aoe2record', [
                {'civ_id': 6, 'name': 'Nobody'},
                {'civ_id': 25, 'name': 'TWest'},
            ], 2],
            ['./recs/versions/HD Tourney Winner Final robo vs Klavskis g1.aoe2record', [
                {'civ_id': 11, 'name': 'robo_boro'},
                {'civ_id': 11, 'name': 'Klavskis'},
            ], 2],
            ['./recs/versions/HD Tourney Winner Final robo vs Klavskis g2.aoe2record', [
                {'civ_id': 21, 'name': 'robo_boro'},
                {'civ_id': 21, 'name': 'Klavskis'},
            ], 2],
            ['./recs/versions/HD Tourney Winner Final robo vs Klavskis g3.aoe2record', [
                {'civ_id': 7, 'name': 'robo_boro'},
                {'civ_id': 7, 'name': 'Klavskis'},
            ], 2],
            ['./recs/versions/HD Tourney Winner Final robo vs Klavskis g4.aoe2record', [
                {'civ_id': 15, 'name': 'robo_boro'},
                {'civ_id': 15, 'name': 'Klavskis'},
            ], 2],
        ]

    def chat_counts_provider(self):
        return [
            ['recs/versions/HD Tourney r1 robo_boro vs Dutch Class g1.aoe2record', 13],
            ['recs/versions/HD_test.mgx', 50],
        ]
