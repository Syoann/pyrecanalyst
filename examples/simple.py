#! /usr/bin/env python
# coding: utf-8

"""
A very barebones example. It outputs a map image to a PNG file and
outputs the players in the game to the command line.
"""

import os
import sys
from optparse import OptionParser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame


parser = OptionParser()
parser.add_option("-i", "--input", dest="filename", help="Input file")
parser.add_option("-o", "--output", dest="output", default=None, help="Output file")

(options, args) = parser.parse_args()

if not options.output:
    options.output = options.filename + ".png"


# Read a recorded game from a file path.
rec = RecordedGame(options.filename)

version = rec.version()

print('Version: ' + version.version_string + ' (' + str(version.sub_version) + ')')

# Display map name
print('Map Name: ' + str(rec.game_settings().map_name()))

# Display players and their civilizations.
print('Players: ')

for player in rec.players():
    symbol = '*'
    if player.owner:
        symbol = '>'
    print(' ' + symbol + ' ' + str(player.name) + ' (' + str(player.civ_name()) + ')')

rec.map_image().resize((1024, 512)).save(options.output)
