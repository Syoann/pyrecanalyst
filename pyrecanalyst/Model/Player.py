from pyrecanalyst.Model.Research import Research
from pyrecanalyst.Model.InitialState import InitialState


class Player:
    """
    The Player class represents a player in the game. This includes co-op players.
    It does not include players who joined the lobby but didn't launch into
    the actual game.
    """

    def __init__(self, rec=None):
        # Recorded game that contains this player.
        self.rec = rec

        # The player's name.
        self.name = ''

        # The player's index.
        self.index = -1

        # The player number. This is different from the index. The player number
        # is always a sequential unique ID. The player index is the same for
        # multiple players in the case of a co-op game.
        self.number = -1

        # Defines if the player is a human.
        self.human = None

        # Defines if the player is a spectator.
        self.spectator = None

        # Defines player's team index (0 = no team).
        self.team_index = -1

        # Defines if player is an owner of the game.
        self.owner = False

        # ID of the player's civilization.
        self.civ_id = None

        # Player color ID.
        self.color_id = None

        # Player's feudal time (in ms, 0 if hasn't been reached).
        self.feudal_time = 0

        # Player's castle time (in ms).
        self.castle_time = 0

        # Player's imperial time (in ms).
        self.imperial_time = 0

        # Player's resign time (in ms) or 0 if player hasn't resigned.
        self.resign_time = 0

        # An array of player's researches containing
        # "research id => \RecAnalyst\Model\Research instance" pairs.
        self.researches_by_id = {}

        # Co-op partners.
        self.coop_partners = []

        # Contains the player's initial state, such as starting resources
        # and population.
        self.initial_state = InitialState()

    def __str__(self):
        return self.name

    def is_human(self):
        """Returns whether the player is a human player."""
        return self.human

    def team(self):
        """Get the player's team."""
        for team in self.rec.teams():
            if team.index() == self.team_index:
                return team
        return None

    def set_coop_partners(self, partners):
        """Set the player's co-op partner group."""
        self.coop_partners = partners

    def is_coop_main(self):
        """Check whether the player is the main player in a co-op group."""
        return self.coop_partners[0] == self

    def get_coop_main(self):
        """Get the main player of this player's co-op group."""
        return self.coop_partners[0]

    def is_coop_partner(self):
        """
        Check whether the player is a partner, and thus not the main player, in a
        co-op group.
        """
        return len(self.coop_partners) > 1 and not self.is_coop_main()

    def get_coop_partners(self):
        """Get co-op partners of this player."""
        return [partner for partner in self.coop_partners if partner != self]

    def is_cooping(self):
        """Returns whether the player is co-oping."""
        return len(self.coop_partners) > 1

    def is_spectator(self):
        """Returns wether the player is spectator of the game"""
        return self.spectator

    def color(self):
        """Get the hex color of this player."""
        if self.rec:
            resource_pack = self.rec.get_resource_pack()
            return resource_pack.get_player_color(self.color_id)
        return None

    def achievements(self):
        if self.rec:
            achievements = self.rec.achievements()
            if achievements:
                return achievements[self.index - 1]
        return None

    def add_research(self, id, time):
        """Add a research action."""
        self.researches_by_id[id] = Research(self.rec, id, time)

    def researches(self):
        return sorted(self.researches_by_id.values(), key=lambda x: x.time)

    def civ_name(self):
        """Get the name of this player's civilization."""
        if self.rec:
            return self.rec.trans('civilizations', self.civ_id)
        return 'Civ #' + self.civ_id

    def starting_age(self):
        """Get the player's starting age."""
        if self.rec:
            return self.rec.trans('ages', self.initial_state.starting_age)
        return None

    def position(self):
        """Get the player's starting position."""
        return self.initial_state.position
