#! /usr/bin/env python3

"""
Outputs a bunch of information about the recorded game, in a specified
locale. By default, this script uses French, but a command-line parameter
can be passed to use a different language.
"""

import argparse
import locale

from pyrecanalyst.RecordedGame import RecordedGame
from pyrecanalyst.BasicTranslator import BasicTranslator

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', dest='filename', help='Input file', required=True)
parser.add_argument('-l', '--lang', dest='language', help='Language')
args = parser.parse_args()

# Deafult language is system locale
if args.language is None:
    args.language = locale.getdefaultlocale()[0].split('_')[0]


# Read a recorded game from a file path.
rec = RecordedGame(args.filename, {
    'translator': BasicTranslator(args.language)
})

# Display some metadata.
print(f"Game Type: {rec.game_settings().game_type_name()}")
print(f"Starting Age: {rec.pov().starting_age()}")
print(f"Map Name: {rec.game_settings().map_name()}")

# Display players and their civilizations.
print("Players:")

for player in rec.players():
    print(f" * {player.name} ({player.civ_name()})")
