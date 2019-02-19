# RecAnalyst Examples

## [Simple](./simple.py)

A very small example that saves a minimap and displays players and their
civilizations on the command line.

## [Chat](./chat.py)

A small example that reads all chat messages from a recorded game and displays
them on the command line.

## [Localized](./simple-localized.py)

A small example that displays some information about the game settings of a
recorded game, in a language of user choice.

```bash
python3 examples/simple-localized.py --input game.aoe2record # Default language (French in this script).
python3 examples/simple-localized.py --input game.aoe2record --lang br # Use Brazilian Portuguese
```
## [Analyze](./analyze.py)

Advanced analysis of a game; can be used to populate a database (JSON ouput).

```bash
python3 examples/analyze.py --input game.aoe2record --lang fr --minimap minimap.out.png --researches researches.out.png
```
