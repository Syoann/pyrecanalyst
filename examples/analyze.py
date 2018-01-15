#! /usr/bin/env python
# coding: utf-8

"""
A very barebones example. It outputs a map image to a PNG file and
outputs the players in the game to the command line.
"""

import os
import sys
import json
from optparse import OptionParser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame
from BasicTranslator import BasicTranslator
from Utils import Utils


parser = OptionParser()
parser.add_option("-i", "--input", dest="filename", help="Input file")
parser.add_option("-o", "--output", dest="output", default=None, help="Output file")

(options, args) = parser.parse_args()

if not options.output:
    options.output = "minimap.png"


# Read a recorded game from a file path.
rec = RecordedGame(options.filename, {'translator': BasicTranslator('fr')})

version = rec.version()

game = {}

# Game settings
game["map"] = rec.game_settings().map_name()
game["type"] = rec.game_settings().game_type_name()
game["population_limit"] = rec.game_settings().get_pop_limit()
game["map_size"] = rec.game_settings().map_size_name()
game["difficulty"] = rec.game_settings().difficulty_name()
game["speed"] = rec.game_settings().game_speed_name()
game["players"] = {}

for player in rec.players():
    game["players"][player.name] = {}
    game["players"][player.name]["civilization"] = player.civ_name()
    game["players"][player.name]["color"] = str(player.color())

print(json.dumps(game, ensure_ascii=False))

# Create output map
rec.map_image().resize((1024, 512)).save(options.output)
