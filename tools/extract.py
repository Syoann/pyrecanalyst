"""
Extract the header and body streams from a file.
"""

import os
import sys

file = sys.argv[1]
output_dir = sys.argv[2].rstrip('/')

os.mkdir(directory)

# @mkdir($outputDir, 0777, true);

rec = RecordedGame(file)


file_put_contents($outputDir . '/header.dat', $rec->getHeaderContents());
file_put_contents($outputDir . '/body.dat', $rec->getBodyContents());
