# coding: utf-8

from ResourcePacks.ResourcePack import ResourcePack
from ResourcePacks.AgeofEmpires.Map import Map
from ResourcePacks.AgeofEmpires.Unit import Unit
from ResourcePacks.AgeofEmpires.Colors import Colors
from ResourcePacks.AgeofEmpires.Civilization import Civilization


class AgeOfEmpires(ResourcePack):
    """
    Resource pack for Age of Empires 2 recorded games of all stripes (base game,
    expansions, HD Edition, Userpatch, ...).
    """
    NAME = 'ageofempires'

    def get_civ_name(self, id):
        """Get the English name for a civilization."""
        return Civilization.get_civ_name(id)

    def is_aok_civ(self, id):
        """Checks if a civilization is included in the Age of Kings base game."""
        return Civilization.is_aok_civ(id)

    def is_aoc_civ(self, id):
        """Checks if a civilization was added in the Age of Conquerors expansion."""
        return Civilization.is_aoc_civ(id)

    def is_forgotten_civ(self, id):
        """Checks if a civilization was added in the Forgotten Empires expansion."""
        return Civilization.is_forgotten_civ(id)

    def is_real_world_map(self, id):
        """
        Check whether a builtin map is a "Real World" map, such as Byzantinum or
        Texas.
        """
        return Map.is_real_world_map(id)

    def is_custom_map(self, id):
        """Check whether a map ID denotes a custom map (i.e., not a builtin one)."""
        return Map.is_custom_map(id)

    def is_standard_map(self, id):
        """Check whether a map ID denotes a builtin map."""
        return Map.is_standard_map(id)

    def is_gate_unit(self, id):
        """Checks whether a unit type ID is a Gate unit."""
        return id in (Unit.GATE, Unit.GATE2, Unit.GATE3, Unit.GATE4)

    def is_palisade_gate_unit(self, id):
        """Checks whether a unit type ID is a Palisade Gate unit."""
        return id in (Unit.PALISADE_GATE, Unit.PALISADE_GATE2, Unit.PALISADE_GATE3, Unit.PALISADE_GATE4)

    def is_cliff_unit(self, id):
        """Checks whether a unit type ID is a cliff. (Yes! Cliffs are units!)"""
        return id >= Unit.CLIFF1 and id <= Unit.CLIFF10

    def is_gaia_object(self, id):
        """
        Checks whether a unit type ID is a GAIA object type. Used to determine
        which objects to draw on a map.
        """
        return self.is_cliff_unit(id) or id in (Unit.GOLDMINE,
                                                Unit.STONEMINE,
                                                Unit.FORAGEBUSH)

    def is_gaia_unit(self, id):
        """
        Checks whether a unit type ID is a GAIA unit. Used to determine which
        units to draw on a map as not belonging to any player.
        """
        return id in (Unit.RELIC, Unit.DEER, Unit.BOAR, Unit.JAVELINA, Unit.TURKEY, Unit.SHEEP)

    def normalize_unit(self, id):
        """
        Normalize a unit type ID. Turns some groups of unit IDs (such as gates in
        four directions) into a single unit ID, so it's easier to work with.
        """
        if self.is_gate_unit(id):
            return Unit.GATE

        if self.is_palisade_gate_unit(id):
            return Unit.PALISADE_GATE

        return id

    def get_terrain_color(self, id, variation=1):
        """Get the color for a terrain type."""
        return Colors.get_terrain_color(id, variation)

    def get_unit_color(self, id):
        """
        Get the color for a unit or object type, such as sheep or boar or
        cliffs(!).
        """
        return Colors.get_unit_color(id)

    def get_player_color(self, id):
        """Get the color for a player."""
        return Colors.get_player_color(id)
