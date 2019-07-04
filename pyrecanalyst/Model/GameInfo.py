class GameInfo:
    """GameInfo holds metadata about the analyzed game."""

    def __init__(self, rec):
        # Recorded game instance.
        self.rec = rec

        # Objectives string.
        self.objectives_string = ''

        # Original Scenario filename.
        self.sc_file_name = None

    def get_players_string(self):
        """Returns the players string (1v1, FFA, etc.)"""
        teams = self.rec.teams()

        team_members = [team for team in teams]
        # Count non-cooping players
        count = 0
        for team in teams:
            for player in team.players():
                if not player.is_cooping():
                    count += 1

        # Remove teams without players.
        team_members = [i for i in team_members if i != [0]]

        if len(team_members) == len(teams) and len(teams) > 2:
            return 'FFA'
        else:
            return 'v'.join(team_members)

    def get_POV(self):
        """Returns the point of view."""
        for player in self.owner.players:
            if player.owner:
                return player.name

        return ''

    def get_POV_ex(self):
        """Returns extended point of view (including coop players)."""
        owner = None

        for player in self.owner.players:
            if player.owner:
                owner = player
                break

        if not owner:
            return ''

        names = []

        for player in self.owner.players:
            if player == owner:
                continue

            if player.index == owner.index:
                names.append(player.name)

        if not names:
            return owner.name

        return owner.name + ' (' + ', '.join(names) + ')'

    def ingame_coop(self):
        """Determines if there is a cooping player in the game."""
        for player in self.owner.players:
            if player.is_cooping:
                return True
        return False

    def objectives(self):
        """Returns the objectives string."""
        return self.objectives_string

    def scenario_filename(self):
        """Returns the Scenario file name."""
        return self.sc_file_name
