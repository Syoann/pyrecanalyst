class Team:
    """Represents a Team of Players in the game."""

    def __init__(self):
        # Players in this team.
        self.players = []

        # Team's index
        self.index = None

    def add_player(self, player):
        """Adds a player to the team."""
        self.players.append(player)

        if not self.index:
            self.index = player.team

    def get_player(self, index):
        """Returns a player at the specified offset."""
        return self.players[index]
