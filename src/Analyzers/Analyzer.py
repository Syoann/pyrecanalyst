# coding: utf-8

import struct


class Analyzer(object):
    """Base class for analyzers."""

    def __init__(self):
        # Recorded game to run the analysis on.
        self.rec = None

        # Current position in the header or body streams.
        self.position = 0

    def analyze(self, game):
        """Run this analysis on a recorded game."""
        self.rec = game
        self.header = game.get_header_contents()
        self.body = game.get_body_contents()
        self.header_size = len(self.header)
        self.body_size = len(self.body)
        return self.run()

    def get(self, analyzer, arg=[]):
        """Get the result of another analyzer."""
        return self.rec.get_analysis(analyzer, arg).analysis

    def read(self, analyzer, arg=[]):
        """
        Compose another analyzer. Starts reading at the current position, and
        uses the composed analyzer's final position as the new position.
        """
        result = self.rec.get_analysis(analyzer, arg, self.position)
        self.position = result.position
        return result.analysis

    def read_header(self, type, size):
        """Read and unpack data from the header of the recorded game file."""
        if self.position + size > self.header_size:
            raise Exception("Can't read " + str(size) + " bytes")
        data = struct.unpack(type, self.header[self.position:self.position + size])
        self.position += size
        return data[0]

    def read_header_raw(self, size):
        """Read raw strings from the header of the recorded game file."""
        if self.position + size > self.header_size:
            raise Exception("Can't read " + str(size) + " bytes")
        data = self.header[self.position:self.position + size]
        self.position += size
        return data

    def read_body(self, type, size):
        """Read and unpack data from the body of the recorded game file."""
        data = struct.unpack(type, self.body[self.position:self.position + size])
        self.position += size
        return data[0]

    def read_body_raw(self, size):
        """Read raw strings from the body of the recorded game file."""
        data = self.body[self.position:self.position + size]
        self.position += size
        return data

    def run(self):
        raise NotImplementedError("Should have implemented this")
