class Research():
    """Represents a research action."""
    def __init__(self, rec, id, time):
        # Recorded game
        self._rec = rec

        # Research ID that was researched by this action
        self._id = id

        # Time since the start of the game at which the research action occurred, in milliseconds
        self._time = int(time)

    def name(self):
        """Get the localised research name."""
        return self._rec.trans('researches', self._id)

    def time(self):
        return self._time
