class Tribute:
    """Represents a resource tribute."""

    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3

    def __init__(self):
        # Time this tribute was sent
        self.time = 0

        # Amount of the resource
        self.amount = 0

        # Player this tribute was sent from
        self.player_from = None

        # Player this tribute was sent to
        self.player_to = None

        # ID of the resource sent in this tribute
        self.resource_id = Tribute.FOOD

        # Market fee
        self.fee = 0.0
