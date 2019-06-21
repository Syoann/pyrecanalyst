#! /usr/bin/env python3

"""
A very barebones example. It outputs a map image to a PNG file and
outputs the players in the game to the command line.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="filename", help="Input file", required=True)
parser.add_argument("-o", "--output", dest="output", default=None, help="Output file")
args = parser.parse_args()

if not args.output:
    args.output = os.path.basename(args.filename) + ".png"


# Read a recorded game from a file path.
rec = RecordedGame(args.filename)

version = rec.version()

print(f"Version: {version.version_string} ({version.sub_version})")

# Display map name
print(f"Map Name: {rec.game_settings().map_name()}")

# Display players and their civilizations.
print('Players: ')

for player in rec.players():
    symbol = '*'
    if player.owner:
        symbol = '>'
    print(f" {symbol} {player.name} ({player.civ_name()})")

rec.map_image().resize((1024, 1024)).save(args.output)
print(f"Minimap saved under '{args.output}'")
