from Model.VictorySettings import VictorySettings
from Analyzers.Analyzer import Analyzer


class VictorySettingsAnalyzer(Analyzer):
    """Analyze an aoe2record game info header."""
    def run(self):
        victory = VictorySettings(self.rec)
        self.position += 4  # separator 9D FF FF FF
        self.custom_conquest = self.read_header('<l', 4) != 0
        self.position += 4  # zero
        self.custom_relics = self.read_header('<l', 4)
        self.position += 4  # zero
        self.custom_percent_explored = self.read_header('<l', 4)
        self.position += 4  # zero
        self.custom_all = self.read_header('<l', 4) != 0
        self.mode = self.read_header('<l', 4)
        self.score = self.read_header('<l', 4)
        self.time_limit = self.read_header('<l', 4)

        victory.mode = self.mode
        victory.time_limit = self.time_limit
        victory.score_limit = self.score

        # TODO add custom victory information somewhere:
        # victory._customRelics = customRelics
        # victory._customPercentExplored = customPercentExplored
        # victory._customAll = customAll

        return victory
