class VictorySettings:
    """Victory implements game's victory settings."""
    STANDARD = 0
    CONQUEST = 1
    TIMELIMIT = 2
    SCORELIMIT = 3
    CUSTOM = 4

    VICTORY_CONDITIONS = {
        STANDARD: "Standard",
        CONQUEST: "Conquest",
        TIMELIMIT: "Time limit",
        SCORELIMIT: "Score limit",
        CUSTOM: "Custom",
    }

    def __init__(self, rec):
        self.rec = rec
        self.time_limit = 0
        self.score_limit = 0
        self.mode = self.STANDARD

    def get_victory_string(self):
        """Returns victory string."""
        if self.mode not in VictorySettings.VICTORY_CONDITIONS:
            return ''

        condition = VictorySettings.VICTORY_CONDITIONS[self.mode]

        if self.mode == VictorySettings.TIMELIMIT:
            if self.time_limit:
                return f"{condition} ({self.time_limit})"
        elif self.mode == VictorySettings.SCORELIMIT:
            if (self.score_limit):
                return f"{condition} ({self.score_limit})"

        return condition
