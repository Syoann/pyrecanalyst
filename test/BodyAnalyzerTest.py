#! /usr/bin/env python
# coding: utf-8

import glob
import os
import unittest



from RecordedGame import RecordedGame
from Model.Tribute import Tribute
from Analyzers.BodyAnalyzer import BodyAnalyzer


class BodyAnalyzerTest(unittest.TestCase):
    def test_hd_forgotten(self):
        files = self.hd_forgotten_provider()
        for f in files:
            rec = RecordedGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), f))
            # Just make sure it doesn't crash!
            analysis = rec.run_analyzer(BodyAnalyzer())
            self.assertIsNotNone(analysis)

    def test_parse(self):
        files = self.records_provider()
        for f in files:
            rec = RecordedGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), f))
            analysis = rec.run_analyzer(BodyAnalyzer())
            self.assertTrue(analysis.duration > 0)

    # Check that voobly injected messages are trimmed correctly.
    def test_voobly_injected_messages(self):
        rec = RecordedGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recs/versions/up1.4.mgz'))
        messages = rec.run_analyzer(BodyAnalyzer()).chat_messages
        # Rating messages should belong to a player.
        self.assertEquals(messages[0].group, 'Rating')
        self.assertEquals(messages[0].msg, '2212')
        self.assertEquals(messages[0].player.name, 'Zuppi')

    # Check that tributes have the correct properties and associated players.
    def test_tributes(self):
        rec = RecordedGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recs/versions/MP Replay v4.3 @2015.09.11 221142 (2).msx'))
        tributes = rec.run_analyzer(BodyAnalyzer()).tributes

        self.assertEqual(10000, tributes[0].amount)
        self.assertEqual(Tribute.WOOD, tributes[0].resource_id)
        self.assertEqual('Ruga the Hun (Original AI)', tributes[0].player_from.name)
        self.assertEqual('Mu Gui-ying (Original AI)', tributes[0].player_to.name)

    def test_achievements(self):
        rec = RecordedGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recs/versions/up1.4.mgz'))
        rec.body()  # Populate achievements on player objects.
        self.assertEqual(7411, rec.get_player(1).achievements()["score"])
        self.assertEqual(9484, rec.get_player(2).achievements()["score"])

    def coop_chat(self):
        rec = RecordedGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recs/FluffyFur+yousifr+TheBlackWinds+Mobius_One[Chinese]=VS=MOD3000+Chrazini+ClosedLoop+ [AGM]Wineup[Britons]_1v1_8PlayerCo-op_01222015.mgx2'))
        messages = rec.body().chat_messages

        # All these players are co-oping, so they share a player index.
        # They can all chat separately, though.
        self.assertEqual('yousifr', 'name', messages[0].player)
        self.assertEqual('TheBlackWinds', 'name', messages[3].player)
        self.assertEqual('Mobius One', 'name', messages[4].player)

    def records_provider(self):
        return [
            './recs/versions/aok.mgl',
            './recs/versions/HD_test.mgx',
            './recs/versions/HD-FE.mgx2',
            './recs/versions/up1.4.mgz',
        ]

    def hd_forgotten_provider(self):
        return [
            './recs/forgotten/Darkluna vs Mums92.mgx2',
            './recs/forgotten/Finals Spring vs Hallis G1.mgx2',
            './recs/forgotten/Finals Spring vs Hallis G2.mgx2',
            './recs/forgotten/Finals Spring vs Hallis G3.mgx2',
            './recs/forgotten/Finals Spring vs Hallis G4.mgx2',
            './recs/forgotten/Finals Spring vs Hallis G4restart.mgx2',
            './recs/forgotten/HD-FE.mgx2',
            './recs/forgotten/Resonance22 (Persians), colsalas (Mayans), TWest (Mongols), NIghtmare_light (Huns) =VS= Frozen Finneus (Aztecs), iViktorious (Indians), Mobius One (Magyars), [V]_Natalie (Spanish)..mgx2',
            './recs/forgotten/spec.mgx2',
        ]
