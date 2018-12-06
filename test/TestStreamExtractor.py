import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from StreamExtractor import StreamExtractor



class TestStreamExtractor(unittest.TestCase):
    def setUp(self):
        self.fp = open("recs/forgotten/HD-FE.mgx2", 'rb')
        self.fp.readlines()
        self.stream = StreamExtractor(self.fp)

    def test_get_file_size(self):
        self.assertEqual(self.stream.get_file_size(), 224538)

    def test_determine_header_length(self):
        self.stream.determine_header_length()
        self.assertEqual(self.stream.header_len, 126742)

    def test_manually_determine_header_length(self):
        self.stream.manually_determine_header_length()
        self.assertEqual(self.stream.header_len, 126750)

    def test_get_header(self):
        self.stream.get_header()
        self.assertIsNotNone(self.stream.header_contents)

    def test_get_body(self):
        body = self.stream.get_body()
        self.assertIsNotNone(self.stream.body_contents)

    def tearDown(self):
        self.fp.close()
