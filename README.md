# pyrecanalyst

Python implementation of Recanalyst. Parse Age of Empires 2 game replays in python.
At the moment, this is just a portage from php to python, code is not optimized at all.

## Installation

`git clone https://github.com/PietroDR/pyrecanalyst.git`

## Run

```
cd pyrecanalyst/examples
python3 analyze.py -i <path_to_replay.aoe2record> -l <lang> -m <out_minimap.png> -r <out_researches.png>
```

## Problems

- Map can't be drawn for Age of Empires II  HD from version 5.7 (current 5.8)
