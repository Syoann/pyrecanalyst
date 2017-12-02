#! /usr/bin/env python
# coding: utf-8

"""
Outputs a bunch of information about the recorded game, in a specified
locale. By default, this script uses French, but a command-line parameter
can be passed to use a different language.

Usage:
   php examples/simple-localized.php # Default language (French).
   php examples/simple-localized.php br # Use Brazilian Portuguese
   php examples/simple-localized.php fake # Nonexistent language, falls back
                                          # to RecAnalyst's default (English)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame
from BasicTranslator import BasicTranslator


filename = os.path.dirname(__file__) + '/../test/recs/versions/up1.4.mgz'

# Read a command-line argument specifying the language to use.
locale = 'fr'
if len(sys.argv) > 1:
    locale = sys.argv[1]

# Read a recorded game from a file path.
rec = RecordedGame(filename, {
    'translator': BasicTranslator(locale)
})

# Display some metadata.
print('Game Type: ' + rec.game_settings().game_type_name())
print('Starting Age: ' + rec.pov().starting_age())
print('Map Name: ' + rec.game_settings().map_name())

# Display players and their civilizations.
print('Players:')

for player in rec.players():
    print(' * ' + player.name + ' (' + player.civ_name() + ')')
