class InitialState:
    """
    InitialState represents the initial state of a player, including resources
    and population.
    """
    DARKAGE = 0
    FEUDALAGE = 1
    CASTLEAGE = 2
    IMPERIALAGE = 3
    POSTIMPERIALAGE = 4

    def __init__(self):
        # Initial food
        self.food = 0

        # Initial wood.
        self.wood = 0

        # Initial stone.
        self.stone = 0

        # Initial gold.
        self.gold = 0

        # Starting age.
        self.starting_age = InitialState.DARKAGE

        # Initial house capacity.
        self.house_capacity = 0

        # Initial population.
        self.population = 0

        # Initial civilian population.
        self.civilian_pop = 0

        # Initial military population.
        self.military_pop = 0

        # Initial extra population.
        self.extra_pop = 0

        # Initial position.
        self.position = [0, 0]
