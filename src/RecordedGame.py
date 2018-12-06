from BasicTranslator import BasicTranslator
from StreamExtractor import StreamExtractor
from Analyzers.BodyAnalyzer import BodyAnalyzer
from Analyzers.VersionAnalyzer import VersionAnalyzer
from Analyzers.HeaderAnalyzer import HeaderAnalyzer
from ResourcePacks.AgeOfEmpires import AgeOfEmpires
from Processors.MapImage import MapImage
from Processors.ResearchImage import ResearchImage
from Processors.Achievements import Achievements


class Result:
    def __init__(self):
        self.analysis= None
        self.position = None


class RecordedGame:
    """Create a recorded game analyser."""
    def __init__(self, filename=None, options=None):
        # Completed analyses.
        self.analyses = {}

        # File handle to the recorded game file.
        self.fp = None

        # Current resource pack.
        self.resource_pack = None

        # RecAnalyst options.
        self.options = {'translator': BasicTranslator()}

        if options is not None:
            self.options.update(options)

        # Set the file name and file pointer/handle/resource.
        self.filename = filename

        if not self.fp:
            self.open()

        # Set default resource pack. The VersionAnalyzer could be used in the
        # future to detect which resource pack to use, should support for SWGB
        # or other games be added.
        self.resource_pack = AgeOfEmpires()

        # Initialize the header/body extractor.
        self.streams = StreamExtractor(self.fp, options)

    def __del__(self):
        if self.fp:
            self.fp.close()

    def open(self):
        """Create a file handle for the recorded game file."""
        self.fp = open(self.filename, 'rb')

    def get_resource_pack(self):
        """Get the current resource pack."""
        return self.resource_pack

    def run_analyzer(self, analyzer):
        """Run an analysis on the current game."""
        return analyzer.analyze(self)

    def get_analysis(self, analyzer_name, arg=[], start_at=0):
        """Get an analysis result for a specific analyzer, running it if necessary."""
        key = str(analyzer_name) + ':' + str(start_at)
        if key not in self.analyses.keys():
            analyzer = None

            if arg:
                analyzer = analyzer_name(arg)
            else:
                analyzer = analyzer_name()

            analyzer.position = start_at
            result = Result()
            result.analysis = self.run_analyzer(analyzer)
            result.position = analyzer.position
            self.analyses[key] = result
        return self.analyses[key]

    def get_header_contents(self):
        """Return the raw decompressed header contents."""
        return self.streams.get_header()

    def get_body_contents(self):
        """Return the raw body contents."""
        return self.streams.get_body()

    def version(self):
        """Get the game version."""
        return self.get_analysis(VersionAnalyzer).analysis

    def header(self):
        """Get the result of analysis of the recorded game header."""
        return self.get_analysis(HeaderAnalyzer).analysis

    def game_settings(self):
        """Get the game settings used to play this recorded game."""
        return self.header().game_settings

    def victory_settings(self):
        """Get the victory settings for this game."""
        return self.header().victory

    def body(self):
        """Get the result of analysis of the recorded game body."""
        return self.get_analysis(BodyAnalyzer).analysis

    def map_image(self, options=None):
        """Render a map image."""
        return MapImage(self, options).run()

    def research_image(self, options=None):
        """Render a research chronology for all players"""
        return ResearchImage(self, options).run()

    def teams(self):
        """Get the teams that played in this recorded game."""
        return self.header().teams

    def players(self):
        """
        Get the players that played in this recorded game.
        Excludes spectating players in HD Edition games.
        """
        return [player for player in self.header().players if not player.is_spectator()]

    def spectators(self):
        """
        Get the players that spectated this recorded game. Spectating players are
        only saved in the recorded games played in HD Edition.
        """
        return [player for player in self.header().players if player.is_spectator]

    def pov(self):
        """
        Get the POV player. This is the player that recorded this recorded game
        file.
        """
        for player in self.header().players:
            if player.owner:
                return player
        return None

    def get_player(self, id):
        """Get a player by their index."""
        for player in self.header().players:
            if player.index == id:
                return player

    def achievements(self, options=None):
        """Get the player achievements."""
        proc = Achievements(self, options)
        return proc.run()

    def get_translate_key(self, args):
        """Get a translate key."""
        # Game version names are in their own file, not in with resource packs.
        if args[0] == 'game_versions':
            packname = 'game_versions'
            keys = args
        else:
            packname = type(self.resource_pack).__name__.lower()
            keys = args
        return [packname, keys]

    def get_translator(self):
        return self.options['translator']

    def trans(self, *args):
        packname, keys = self.get_translate_key(args)
        return self.get_translator().trans(packname, keys)
