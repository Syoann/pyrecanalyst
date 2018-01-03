#! /usr/bin/env python
# coding: utf-8

"""
This example reads chat messages from a recorded game.

Usage:
   python examples/chat.py /path/to/your/own/file.mgx
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from RecordedGame import RecordedGame
from Utils import Utils

# Read a recorded game filename from the command line.
# Default to a test team game.
filename = sys.argv[1]

if len(sys.argv) > 1:
    filename = sys.argv[1]

# Read a recorded game from a file path.
rec = RecordedGame(filename)

# There are two types of chat in a recorded game: pre-game multiplayer lobby
# chat, and in-game chat.

# Read the pre-game chat from the file header. Pre-game messages don't have a
# timestamp.
for chat in rec.header().pregame_chat:
    print('<' + chat.player.name + '> ' + chat.msg)

# Read the in-game chat from the file body.
for chat in rec.body().chat_messages:
    # Format the millisecond time as HH:MM:SS.
    time = Utils.format_game_time(chat.time)

    if chat.player:
        print('[' + time + '] <' + chat.player.name + '> ' + chat.msg)
    else:
        print('[' + time + '] * ' + chat.msg)
