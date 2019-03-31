import json
import os
from ResourcePacks.AgeofEmpires.Unit import Unit

class Colors(object):
    """Utilities for colors of things in Age of Empires."""

    # Default colors of GAIA-owned objects, indexed by unit ID.
    GAIA_COLORS = {
        Unit.GOLDMINE: '#ffc700',
        Unit.STONEMINE: '#919191',
        Unit.CLIFF1: '#714b33',
        Unit.CLIFF2: '#714b33',
        Unit.CLIFF3: '#714b33',
        Unit.CLIFF4: '#714b33',
        Unit.CLIFF5: '#714b33',
        Unit.CLIFF6: '#714b33',
        Unit.CLIFF7: '#714b33',
        Unit.CLIFF8: '#714b33',
        Unit.CLIFF9: '#714b33',
        Unit.CLIFF10: '#714b33',
        Unit.RELIC: '#ffffff',
        Unit.TURKEY: '#a5c46c',
        Unit.SHEEP: '#a5c46c',
        Unit.DEER: '#a5c46c',
        Unit.BOAR: '#a5c46c',
        Unit.JAVELINA: '#a5c46c',
        Unit.FORAGEBUSH: '#a5c46c',
    }

    colors = None

    @staticmethod
    def get_colors(category):
        """Get colors from the resources file."""
        if not Colors.colors:
            with open(os.path.join(os.path.dirname(__file__), '../../../resources/data/ageofempires/colors.json'),'r') as fh:
                Colors.colors = json.load(fh)

        return Colors.colors[category]

    @staticmethod
    def get_terrain_color(id, variation="1"):
        """Get the color for a terrain type."""
        terrain_colors = Colors.get_colors('terrain')
        return terrain_colors[str(id)][str(variation)]

    @staticmethod
    def get_unit_color(id):
        """
        Get the color for a unit or object type, such as sheep or boar or
        cliffs(!).
        """
        return Colors.GAIA_COLORS[id]

    @staticmethod
    def get_player_color(id):
        """Get the color for a player."""
        player_colors = Colors.get_colors('players')
        return player_colors[str(id)]
