# coding: utf-8

import unittest
from StreamExtractor import StreamExtractor


class TestStreamExtractor(unittest.TestCase):
    def setUp(self):
        fp = open("recs/forgotten/HD-FE.mgx2")
        self.stream = StreamExtractor(fp)

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
