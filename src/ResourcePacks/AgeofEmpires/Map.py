class Map:
    """Some map constants."""
    ARABIA = 9
    ARCHIPELAGO = 10
    BALTIC = 11
    BLACKFOREST = 12
    COASTAL = 13
    CONTINENTAL = 14
    CRATERLAKE = 15
    FORTRESS = 16
    GOLDRUSH = 17
    HIGHLAND = 18
    ISLANDS = 19
    MEDITERRANEAN = 20
    MIGRATION = 21
    RIVERS = 22
    TEAMISLANDS = 23
    RANDOM = 24
    SCANDINAVIA = 25
    MONGOLIA = 26
    YUCATAN = 27
    SALTMARSH = 28
    ARENA = 29
    KINGOFTHEHILL = 30
    OASIS = 31
    GHOSTLAKE = 32
    NOMAD = 33
    IBERIA = 34
    BRITAIN = 35
    MIDEAST = 36
    TEXAS = 37
    ITALY = 38
    CENTRALAMERICA = 39
    FRANCE = 40
    NORSELANDS = 41
    SEAOFJAPAN = 42
    BYZANTINUM = 43
    CUSTOM = 44
    BLINDRANDOM = 48
    ACROPOLIS = 49
    BUDAPEST = 50
    CENOTES = 51
    CITYOFLAKES = 52
    GOLDENPIT = 53
    HIDEOUT = 54
    HILLFORT = 55
    LOMBARDIA = 56
    STEPPE = 57
    VALLEY = 58
    MEGARANDOM = 59
    HAMBURGER = 60
    CTR_RANDOM = 61
    CTR_MONSOON = 62
    CTR_PYRAMIDDESCENT = 63
    CTR_SPIRAL = 64

    @staticmethod
    def is_real_world_map(id):
        """
        Check whether a builtin map is a "Real World" map, such as Byzantinum or
        Texas.
        """
        return id in (Map.IBERIA, Map.BRITAIN, Map.MIDEAST, Map.TEXAS,
                      Map.ITALY, Map.CENTRALAMERICA, Map.FRANCE, Map.NORSELANDS,
                      Map.SEAOFJAPAN, Map.BYZANTINUM)

    @staticmethod
    def is_custom_map(id):
        """Check whether a map ID denotes a custom map (i.e., not a builtin one)."""
        return id == Map.CUSTOM

    @staticmethod
    def is_standard_map(id):
        """Check whether a map ID denotes a builtin map."""
        return id in (Map.ARABIA, Map.ARCHIPELAGO, Map.BALTIC, Map.BLACKFOREST,
                      Map.COASTAL, Map.CONTINENTAL, Map.CRATERLAKE,
                      Map.FORTRESS, Map.GOLDRUSH, Map.HIGHLAND, Map.ISLANDS,
                      Map.MEDITERRANEAN, Map.MIGRATION, Map.RIVERS,
                      Map.TEAMISLANDS, Map.SCANDINAVIA, Map.MONGOLIA,
                      Map.YUCATAN, Map.SALTMARSH, Map.ARENA, Map.KINGOFTHEHILL,
                      Map.OASIS, Map.GHOSTLAKE, Map.NOMAD,
                      Map.RANDOM)
