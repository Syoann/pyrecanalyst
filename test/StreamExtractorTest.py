import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from StreamExtractor import StreamExtractor


class StreamExtractorTest(unittest.TestCase):
    def load(self, path):
        fp = open(os.path.join(os.path.dirname(__file__), path), 'r')
        return StreamExtractor(fp)

    def test_stream_extractor(self):
        for f in self.files_provider():
            extractor = self.load(f)
            self.assertIsNotNone(extractor.get_header())
            self.assertIsNotNone(extractor.get_body())

    def files_provider(self):
        return [
            'recs/versions/aok.mgl',
            'recs/versions/up1.4.mgz',
            'recs/versions/mgx2_simple.mgx2',
            'recs/versions/MP Replay v4.3 @2015.09.11 221142 (2).msx',
            'recs/versions/MP_Replay_v4.msx2',
            'recs/versions/HD Tourney r1 robo_boro vs Dutch Class g1.aoe2record',
            # A multiplayer autosave with front matter.
            # ['recs/auto save -  28-jan-2014 16`00`07.msx'],
        ]
