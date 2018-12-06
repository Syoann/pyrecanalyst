import functools

from PIL import Image, ImageColor, ImageDraw

from ResourcePacks.AgeofEmpires.Unit import Unit


class MapImage(object):
    """Generate a top-down map image that shows the starting state of the game."""
    def __init__(self, rec, options=None):
        # Recorded game file to use.
        self.rec = rec

        self.options = {'manager': None,
                        'show_positions': True,
                        'show_player_units': False,
                        'show_elevation': False}

        if options is not None:
            self.options.update(options)

        self.show_positions = self.options['show_positions']
        self.show_player_units = self.options['show_player_units']
        self.show_elevation = self.options['show_elevation']

    # Generate a map!
    def run(self):
        header = self.rec.header()
        map_data = header.map_data
        map_size = len(map_data)
        image = Image.new('RGBA', (map_size, map_size), (255, 255, 255, 0))

        print(map_size)

        draw = ImageDraw.Draw(image)
        pixels = image.load()

        p = self.rec.get_resource_pack()

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                variation = 1
                if self.show_elevation:
                    if map_data[y + 1][x + 1]:
                        bottom_right = map_data[y + 1][x + 1]
                        if bottom_right.elevation < tile.elevation:
                            variation = 0
                        elif bottom_right.elevation > tile.elevation:
                            variation = 2

                color = p.get_terrain_color(tile.terrain, variation)

                if color:
                    pixels[x, y] = ImageColor.getrgb(color)
                else:
                    raise Exception('Unknown terrain ID ' + str(tile.terrain))

        gaia_objects = self.sort_objects(header.player_info.gaia_objects)

        for obj in gaia_objects:
            color = p.get_unit_color(obj.id)
            (x, y) = obj.position

            draw.rectangle(((x-1, y-1), (x+1, y+1)), fill=ImageColor.getrgb(color))

        if self.show_player_units:
            for obj in header.player_info.player_objects:
                if obj.owner.index < 0:
                    continue

                color = obj.owner.color()
                (x, y) = obj.position

                draw.rectangle(((x-1, y-1), (x+1, y+1)), fill=ImageColor.getrgb(color))

        if self.show_positions:
            for player in header.players:
                if player.is_cooping() or player.is_spectator():
                    continue

                color = player.color()
                (x, y) = player.position()

                draw.ellipse((x-4, y-4, x+4, y+4), fill=ImageColor.getrgb(color))
                draw.ellipse((x-8, y-8, x+8, y+8), outline=ImageColor.getrgb(color))

        image = image.rotate(45, expand=True)
        return image

    def sort_objects(self, objects):
        """
        Sort GAIA objects for a good draw order. Relics are important, and show
        on top of everything else; cliffs are lines (so interruptions are OK) and
        show below everything else.
        """
        p = self.rec.get_resource_pack()

        def sorting_func(item1, item2):
            # relics shown on top of everything else
            if item1.id == Unit.RELIC and item2.id != Unit.RELIC:
                return True
            if item2.id == Unit.RELIC and item1.id != Unit.RELIC:
                return False

            # cliffs show below everything else
            if p.is_cliff_unit(item1.id) and not p.is_cliff_unit(item2.id):
                return False
            if p.is_cliff_unit(item2.id) and not p.is_cliff_unit(item1.id):
                return True
            return 0

        cmp = functools.cmp_to_key(sorting_func)
        return sorted(objects, key=cmp)
