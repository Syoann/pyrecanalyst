#! /usr/bin/env python

"""
Outputs a bunch of information about the recorded game, in a specified
locale. By default, this script uses French, but a command-line parameter
can be passed to use a different language.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame
from BasicTranslator import BasicTranslator

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', dest='filename', help='Input file', required=True)
parser.add_argument('-l', '--lang', dest='language', help='Language')
args = parser.parse_args()

# Deafult language
if args.locale is None:
    args.locale = 'fr'


# Read a recorded game from a file path.
rec = RecordedGame(args.filename, {
    'translator': BasicTranslator(args.language)
})

# Display some metadata.
print('Game Type: ' + rec.game_settings().game_type_name())
print('Starting Age: ' + rec.pov().starting_age())
print('Map Name: ' + rec.game_settings().map_name())

# Display players and their civilizations.
print('Players:')

for player in rec.players():
    print(' * ' + player.name + ' (' + player.civ_name() + ')')
