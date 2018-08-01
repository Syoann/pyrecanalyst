from Analyzers.Analyzer import Analyzer

class Data(object):
    """Game data"""
    def __init__(self):
        self.scenario_filename = None
        self.num_players = None
        self.duration = None
        self.allow_cheats = None
        self.complete = None
        self.u0 = None
        self.map_size = None
        self.map_id = None
        self.population = None
        self.victory = None
        self.starting_age = None
        self.resources = None
        self.all_techs = None
        self.team_together = None
        self.reveal_map = None
        self.is_deatch_match = None
        self.is_regicide = None
        self.u1 = None
        self.lock_teams = None
        self.lock_speed = None
        self.u2 = None



class PlayerStats(object):
    """Player statistics"""
    def __init__(self):
        self.name = None
        self.total_score = None
        self.victory = None
        self.civ_id = None
        self.color_id = None
        self.team = None
        self.allies_count = None
        self.mvp = None
        self.result = None

        self.military_stats = None
        self.economy_stats = None
        self.tech_stats = None
        self.society_stats = None



class MilitaryStats(object):
    """Military statistics"""
    def __init__(self):
        self.score = None
        self.units_killed = None
        self.hit_points_killed = None
        self.units_lost = None
        self.buildings_razed = None
        self.hit_points_razed = None
        self.buildings_lost = None
        self.units_converted = None

        # Amount of units killed and buildings razed against each player.
        self.player_units_killed = {}
        self.player_buildings_razed = {}



class EconomyStats(object):
    """Economic statistics"""
    def __init__(self):
        self.score = None
        self.u0 = None
        self.food_collected = None
        self.wood_collected = None
        self.stone_collected = None
        self.gold_collected = None
        self.tribute_sent = None
        self.tribute_received = None
        self.trade_profit = None
        self.relic_gold = None
        self.player_tribute_sent = {}



class TechStats(object):
    """Technology statistics"""
    def __init__(self):
        self.score = None
        self.u0 = None
        self.feudal_time = None
        self.castle_time = None
        self.imperial_time = None
        self.map_exploration = None
        self.research_count = None
        self.research_percent = None



class SocietyStats(object):
    """Society statistics"""
    def __init__(self):
        self.score = None
        self.total_wonders = None
        self.total_castles = None
        self.relics_captured = None
        self.u0 = None
        self.villager_high = None



class PostgameDataAnalyzer(Analyzer):
    """Analyze a UserPatch post-game data block, containing achievements."""
    def run(self):
        # Prize for ugliest, most boring method of the project goes to...
        data = Data()

        self.position += 3 # Skip body command metadata.
        data.scenario_filename = self.read_body_raw(32).rstrip()
        data.num_players = self.read_body('l', 4)
        data.duration = self.read_body('l', 4)
        self.position += 1
        data.allow_cheats = ord(self.body[self.position])
        self.position += 1
        data.complete = ord(self.body[self.position])
        self.position += 10 # Always zeros?
        data.u0 = self.read_body('f', 4) # Always 2.0?
        self.position += 1
        data.map_size = ord(self.body[self.position])
        self.position += 1
        data.map_id = ord(self.body[self.position])
        self.position += 1
        data.population = ord(self.body[self.position])
        self.position += 1
        self.position += 1
        data.victory = ord(self.body[self.position])
        self.position += 1
        data.starting_age = ord(self.body[self.position])
        self.position += 1
        data.resources = ord(self.body[self.position])
        self.position += 1
        data.all_techs = ord(self.body[self.position])
        self.position += 1
        data.team_together = ord(self.body[self.position])
        self.position += 1
        data.reveal_map = ord(self.body[self.position])
        self.position += 1
        data.is_deatch_match = ord(self.body[self.position])
        self.position += 1
        data.is_regicide = ord(self.body[self.position])
        self.position += 1
        data.u1 = ord(self.body[self.position])
        self.position += 1
        data.lock_teams = ord(self.body[self.position])
        self.position += 1
        data.lock_speed = ord(self.body[self.position])
        self.position += 1
        data.u2 = ord(self.body[self.position])

        players = {}
        for i in range(0, 8):
            player_stats = PlayerStats()
            player_stats.name = self.read_body_raw(16).rstrip()
            player_stats.total_score = self.read_body('H', 2)
            total_scores = [None] * 9
            for j in range(0, 8):
                total_scores[j] = self.read_body('H', 2)

            player_stats.total_scores = total_scores
            self.position += 1
            player_stats.victory = ord(self.body[self.position])
            self.position += 1
            player_stats.civ_id = ord(self.body[self.position])
            self.position += 1
            player_stats.color_id = ord(self.body[self.position])
            self.position += 1
            player_stats.team = ord(self.body[self.position])
            self.position += 1
            player_stats.allies_count = ord(self.body[self.position])
            self.position += 1  # Always -1?
            self.position += 1
            player_stats.mvp = ord(self.body[self.position])
            self.position += 3  # Padding?
            self.position += 1
            player_stats.result = ord(self.body[self.position])
            self.position += 3  # Padding?

            military_stats = MilitaryStats()
            military_stats.score = self.read_body('H', 2)
            military_stats.units_killed = self.read_body('H', 2)
            military_stats.hit_points_killed = self.read_body('H', 2)
            military_stats.units_lost = self.read_body('H', 2)
            military_stats.buildings_razed = self.read_body('H', 2)
            military_stats.hit_points_razed = self.read_body('H', 2)
            military_stats.buildings_lost = self.read_body('H', 2)
            military_stats.units_converted = self.read_body('H', 2)

            # Amount of units killed and buildings razed against each player.
            military_stats.player_units_killed = {}
            for other in range(1, 9):
                military_stats.player_units_killed[other] = self.read_body('H', 2)

            military_stats.player_buildings_razed = {}
            for other in range(1, 9):
                military_stats.player_buildings_razed[other] = self.read_body('H', 2)

            player_stats.military_stats = military_stats

            economy_stats = EconomyStats()
            economy_stats.score = self.read_body('H', 2)
            economy_stats.u0 = self.read_body('H', 2) # Probably padding?
            economy_stats.food_collected = self.read_body('l', 4)
            economy_stats.wood_collected = self.read_body('l', 4)
            economy_stats.stone_collected = self.read_body('l', 4)
            economy_stats.gold_collected = self.read_body('l', 4)
            economy_stats.tribute_sent = self.read_body('H', 2)
            economy_stats.tribute_received = self.read_body('H', 2)
            economy_stats.trade_profit = self.read_body('H', 2)
            economy_stats.relic_gold = self.read_body('H', 2)
            # Tribute sent to each player.
            economy_stats.playerTributeSent = []
            for other in range(1, 9):
                economy_stats.player_tribute_sent[other] = self.read_body('H', 2)

            player_stats.economy_stats = economy_stats

            tech_stats = TechStats()
            tech_stats.score = self.read_body('H', 2)
            tech_stats.u0 = self.read_body('H', 2)  # Probably padding?
            tech_stats.feudal_time = self.read_body('l', 4)
            tech_stats.castle_time = self.read_body('l', 4)
            tech_stats.imperial_time = self.read_body('l', 4)
            self.position += 1
            tech_stats.map_exploration = ord(self.body[self.position])
            self.position += 1
            tech_stats.research_count = ord(self.body[self.position])
            self.position += 1
            tech_stats.research_percent = ord(self.body[self.position])
            player_stats.tech_stats = tech_stats

            self.position += 1  # Padding

            society_stats = SocietyStats()
            society_stats.score = self.read_body('H', 2)
            self.position += 1
            society_stats.total_wonders = ord(self.body[self.position])
            self.position += 1
            society_stats.total_castles = ord(self.body[self.position])
            self.position += 1
            society_stats.relics_captured = ord(self.body[self.position])
            self.position += 1
            society_stats.u0 = ord(self.body[self.position])
            society_stats.villager_high = self.read_body('H', 2)
            player_stats.society_stats = society_stats

            # Padding.
            self.position += 84

            players[i] = player_stats

        data.players = players

        self.position += 4

        return data
