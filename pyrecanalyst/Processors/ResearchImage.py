import os
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont


class ResearchImage:
    ASSET_SIZE = (36, 36)
    TIME_LINE_HEIGHT = 20
    WHITESPACE = 4

    PATH_RESOURCES = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "resources")
    PATH_IMAGES = os.path.join(PATH_RESOURCES, "images")
    PATH_FONTS = os.path.join(PATH_RESOURCES, "fonts")

    AGE_COLORS = {0: "#FFCDD2",
                  101: "#FFECB3",
                  102: "#C5CAE9",
                  103: "#C8E6C9",
                  104: "#C8E6C9"}

    def __init__(self, rec, options=None):
        self.rec = rec
        self.players = rec.players()
        self.researches = self.get_researches_by_time()
        self.image = None
        self.draw = None
        self.font = ImageFont.truetype(os.path.join(self.PATH_FONTS, "Arimo-Regular.ttf"), 16)
        self.options = None

        if options is not None:
            self.options.update(options)

        # Width of the longest player name
        self.PLAYER_NAME_SIZE = max([self.font.getsize(player.name)[0] for player in self.players]) + self.WHITESPACE * 2

    def run(self):
        self.draw_background()
        self.draw_headers()
        self.draw_researches()
        return self.image

    def draw_background(self):
        """Draw the background with the correct size"""
        width = self.ASSET_SIZE[0] + self.PLAYER_NAME_SIZE + self.ASSET_SIZE[0] * self.get_max_researches() + self.WHITESPACE * (len(self.researches.keys()) - 1)
        height = self.TIME_LINE_HEIGHT + len(self.players) * self.ASSET_SIZE[0]
        self.image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

    def draw_headers(self):
        """Draw the civilization avatar and the name of every player"""
        y_offset = 0
        for player in self.players:
            # Civilization
            img_civ = Image.open(os.path.join(self.PATH_IMAGES, "civs",
                                              str(player.color_id), str(player.civ_id) + ".png"))
            self.image.paste(img_civ, (0, y_offset))

            #  Player's name
            w, h = self.draw.textsize(player.name, font=self.font)
            text_offset = self.font.getoffset(player.name)
            self.draw.text([self.ASSET_SIZE[0] + self.WHITESPACE, y_offset + (self.ASSET_SIZE[1] - h) / 2 - text_offset[1]], player.name, font=self.font, fill=player.color())
            y_offset += self.ASSET_SIZE[1]

        # Time
        w, h = self.draw.textsize("Time (min)", font=self.font)
        self.draw.text([(self.ASSET_SIZE[0] + self.PLAYER_NAME_SIZE - w) / 2, y_offset + 3], "Time (min)", font=self.font, fill="black")

    def draw_researches(self):
        """Draw researche vignettes for each player"""
        pos_x = self.PLAYER_NAME_SIZE + self.ASSET_SIZE[0]
        timeline_color = {}

        for time, d in self.researches.items():
            pos_y = 0
            max_items = max([len(researches) for researches in d.values()])

            for player in self.players:
                if player not in timeline_color:
                    timeline_color[player] = self.AGE_COLORS[0]

                for i in range(0, max_items):
                    try:
                        research = d[player.name][i]
                        img = Image.open(os.path.join(self.PATH_IMAGES, "researches", str(research.id) + ".png"))
                        self.image.paste(img, (pos_x + i * self.ASSET_SIZE[0], pos_y))

                        if research.id in self.AGE_COLORS.keys():
                            timeline_color[player] = self.AGE_COLORS[research.id]

                    except (KeyError, IndexError):
                        self.draw.rectangle([pos_x + self.ASSET_SIZE[0] * i,
                                             pos_y,
                                             pos_x + self.ASSET_SIZE[0] * (i + 1) - 1,
                                             pos_y + self.ASSET_SIZE[1] - 1], fill=timeline_color[player])
                pos_y += self.ASSET_SIZE[1]

            # Minute
            w, h = self.draw.textsize(str(time), font=self.font)
            self.draw.text([pos_x + (max_items * self.ASSET_SIZE[1] - w) / 2, pos_y + 3], str(time), font=self.font, fill="black")

            pos_x += max_items * self.ASSET_SIZE[1] + self.WHITESPACE

    def get_researches_by_player(self):
        """Get the list of researches, by player"""
        researches_by_player = defaultdict(dict)

        for player in self.players:
            researches_by_player[player.name] = {}
            for research in player.researches():
                researches_by_player[player.name][research.time] = research

        return researches_by_player

    def get_researches_by_time(self):
        """Get the list of researches, by time (min)"""
        researches_by_time = defaultdict(dict)

        for name, researches in self.get_researches_by_player().items():
            for time, research in researches.items():
                d = researches_by_time[round(time / 60000)]
                if name in d:
                    d[name].append(research)
                else:
                    d[name] = [research]

        return dict(sorted(researches_by_time.items()))

    def get_max_researches(self):
        """Get the maximum number of researches to depict"""
        sum = 0
        for d in self.researches.values():
            sum += max([len(dic) for dic in d.values()])

        return sum
