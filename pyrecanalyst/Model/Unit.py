class Unit:
    """Represents a unit object in the game."""

    def __init__(self, rec, id, position=(0, 0)):
        """Create a new Unit."""
        self.rec = rec
        self.id = id
        self.position = position

        # The player that owns this unit. None if GAIA.
        self.owner = None

    def name(self):
        return self.rec.trans('units', self.id)
