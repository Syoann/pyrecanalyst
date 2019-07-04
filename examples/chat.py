#! /usr/bin/env python

"""
This example reads chat messages from a recorded game.

Usage:
   python examples/chat.py /path/to/your/own/file.mgx
"""

import argparse
import datetime

from pyrecanalyst.RecordedGame import RecordedGame


# Read a recorded game filename from the command line.
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', dest="filename", help="Input file", required=True)
args = parser.parse_args()

# Read a recorded game from a file path.
rec = RecordedGame(args.filename)

# There are two types of chat in a recorded game: pre-game multiplayer lobby
# chat, and in-game chat.

# Read the pre-game chat from the file header. Pre-game messages don't have a
# timestamp.
for chat in rec.header().pregame_chat:
    print(f"<{chat.player.name}> {chat.msg}")

# Read the in-game chat from the file body.
for chat in rec.body().chat_messages:
    # Format the millisecond time as HH:MM:SS.
    time = datetime.timedelta(milliseconds=chat.time)
    time_str = str(time).split(".")[0]

    if chat.player:
        print(f"[{time_str}] <{chat.player.name}> {chat.msg}")
    else:
        print(f"[{time_str}] {chat.msg}")
