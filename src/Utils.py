class Utils(object):
    """Miscellaneous utilities for working with RecAnalyst."""

    @staticmethod
    def format_game_time(time, format='%02d:%02d:%02d'):
        """Format a game time as "HH:MM:SS"."""
        if time == 0:
            return '-'

        hour = int(time / 1000 / 3600)
        minute = int(time / 1000 / 60) % 60
        second = int(time / 1000) % 60

        return format % (hour, minute, second)
