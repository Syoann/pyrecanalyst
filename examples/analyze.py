#! /usr/bin/env python

"""
Outputs game information in JSON format.
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
parser.add_option("-l", "--lang", dest="lang", help="Language code (en, fr, es, it, ...)")
parser.add_option("-r", "--researches", dest="researches", help="Output file for the researches image")
parser.add_option("-m", "--minimap", dest="minimap", help="Output file for the minimap")

(options, args) = parser.parse_args()

if not options.filename:
    parser.print_help()
    sys.exit()

if not options.lang:
    options.lang = "en"

# Read a recorded game from a file path.
rec = RecordedGame(options.filename, {'translator': BasicTranslator(options.lang)})

game = {}

# Game settings
version = rec.version()
game["version"] = version.version_string + " " + str(version.sub_version)
game["map"] = rec.game_settings().map_name()
game["type"] = rec.game_settings().game_type_name()
game["population_limit"] = rec.game_settings().get_pop_limit()
game["map_size"] = rec.game_settings().map_size_name()
game["difficulty"] = rec.game_settings().difficulty_name()
game["speed"] = rec.game_settings().game_speed_name()
game["players"] = {}

post_game_data = rec.achievements()

n_players = len(rec.players())

for player in rec.players():
    game["players"][player.name] = {}
    game["players"][player.name]["team"] = player.team_index
    game["players"][player.name]["human"] = player.human
    game["players"][player.name]["civilization"] = player.civ_name()
    game["players"][player.name]["color"] = str(player.color())
    game["players"][player.name]["resign_time"] = player.resign_time

    if options.researches:
        game["players"][player.name]["researches"] = {}
        for research in player.researches():
            game["players"][player.name]["researches"][str(research.time)] = research.name()

# Export in JSON format
print(json.dumps(game, ensure_ascii=False, indent=4))

# Create researches image
if options.researches:
    image = rec.research_image()

    try:
        image.resize((image.size[0], image.size[1])).save(options.researches)
    except AttributeError as error:
        sys.stderr.write("Could not generate the research chronology...\n")
        raise(error)

# Create output map
if options.minimap:
    image = rec.map_image()

    try:
        image.resize((350, 200)).save(options.minimap)
    except AttributeError as error:
        sys.stderr.write("Could not generate the minimap...\n")
