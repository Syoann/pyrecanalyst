class Achievements(object):
    def __init__(self, rec, options={}):
        # Recorded game file to use.
        self.rec = rec

    def run(self):
        post_game_data = self.rec.body().post_game_data
        if not post_game_data:
            return None

        achievements = {}

        for i, player in post_game_data.players.iterkeys():
            if not player.name:
                continue
            achievements[i] = {
                'score': player.total_score,
                'victory': bool(player.victory),
                'mvp': bool(player.mvp),
                'military': player.military_stats,
                'economy': player.economy_stats,
                'tech': player.tech_stats,
                'society': player.society_stats
            }
        return achievements
