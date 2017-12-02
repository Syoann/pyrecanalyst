class Team():
    """Represents a Team of Players in the game."""

    def __init__(self):
        # Players in this team.
        self._players = []

        # Team's index
        self._index = None

    def add_player(self, player):
        """Adds a player to the team."""
        self._players.append(player)

        if not self.index:
            self._index = player.team

    def get_player(self, index):
        """Returns a player at the specified offset."""
        return self._players[index]

    def index(self):
        """Returns an index of the team."""
        return self._index

    def players(self):
        """Get the players in this team."""
        return self._players
