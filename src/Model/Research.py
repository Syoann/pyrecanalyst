class Research():
    """Represents a research action."""
    def __init__(self, rec, id, time):
        # Recorded game
        self.rec = rec

        # Research ID that was researched by this action
        self.id = id

        # Time since the start of the game at which the research action occurred, in milliseconds
        self.time = time

    def name(self):
        """Get the localised research name."""
        return self.rec.trans('researches', self.id)
