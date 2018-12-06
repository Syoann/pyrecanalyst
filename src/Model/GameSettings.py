from Processors.MapName import MapName


class GameSettings():
    TYPE_RANDOMMAP = 0
    TYPE_REGICIDE = 1
    TYPE_DEATHMATCH = 2
    TYPE_SCENARIO = 3
    TYPE_CAMPAIGN = 4
    TYPE_KINGOFTHEHILL = 5
    TYPE_WONDERRACE = 6
    TYPE_DEFENDTHEWONDER = 7
    TYPE_TURBORANDOMMAP = 8

    MAPSTYLE_STANDARD = 0
    MAPSTYLE_REALWORLD = 1
    MAPSTYLE_CUSTOM = 2
    MAPSTYLE_SPECIAL = 3

    LEVEL_HARDEST = 0
    LEVEL_HARD = 1
    LEVEL_MODERATE = 2
    LEVEL_STANDARD = 3
    LEVEL_EASIEST = 4

    SPEED_SLOW = 100
    SPEED_NORMAL = 150
    SPEED_FAST = 200

    REVEAL_NORMAL = 0
    REVEAL_EXPLORED = 1
    REVEAL_ALLVISIBLE = 2

    SIZE_TINY = 0
    SIZE_SMALL = 1
    SIZE_MEDIUM = 2
    SIZE_NORMAL = 3
    SIZE_LARGE = 4
    SIZE_GIANT = 5

    MODE_SINGLEPLAYER = 0
    MODE_MULTIPLAYER = 1

    def __init__(self, rec, attrs={}):
        # Recorded game instance.
        self.rec = rec

        # Game type.
        self.game_type = attrs.get('game_type', GameSettings.TYPE_RANDOMMAP)

        # Difficulty level.
        self.difficulty_level = attrs.get('difficulty_level', self.LEVEL_HARDEST)

        # Game speed.
        self.game_speed = attrs.get('game_speed', self.SPEED_NORMAL)

        # Reveal Map settings.
        self.reveal_map = attrs.get('reveal_map', self.REVEAL_NORMAL)

        # Map size.
        self.map_size = attrs.get('map_size', self.SIZE_TINY)

        # Map ID.
        self.map_id = attrs.get('map_id', 0)

        # Population limit.
        self.pop_limit = attrs.get('pop_limit', 0)

        # Diplomacy lock status.
        self.lock_diplomacy = attrs.get('lock_diplomacy', False)

    def game_type_name(self):
        """Returns game type string."""
        return self.rec.trans('game_types', self.game_type)

    def map_style_name(self):
        """Returns map style string."""
        map_style = self.rec.get_resource_pack().get_map_style(self.map_id)
        return self.rec.trans('map_styles', map_style)

    def difficulty_name(self):
        """eturns difficulty level string."""
        return self.rec.trans('difficulties', self.difficulty_level)

    def game_speed_name(self):
        """Returns game speed string."""
        return self.rec.trans('game_speeds', self.game_speed)

    def reveal_map_name(self):
        """Returns reveal map string."""
        return self.rec.trans('reveal_map', self.reveal_map)

    def map_size_name(self):
        """Returns map size string."""
        return self.rec.trans('map_sizes', self.map_size)

    def get_pop_limit(self):
        """Returns population limit."""
        return self.pop_limit

    def get_lock_diplomacy(self):
        """Returns whether diplomacy was locked."""
        return self.lock_diplomacy

    def is_scenario(self):
        """Returns true if game type is scenario, false otherwise."""
        return self.game_type == GameSettings.TYPE_SCENARIO

    def map_name(self, options={}):
        """Get the map name."""
        extract_rms_name = True
        if 'extract_rms_name' in options:
            extract_rms_name = options['extract_rms_name']

        if extract_rms_name and self.is_custom_map():
            name_extractor = MapName(self.rec)
            likely_name = name_extractor.run()

            if likely_name:
                return likely_name
        return self.rec.trans('map_names', self.map_id)

    def map_style(self):
        """
        Get the map style for a map ID. Age of Empires categorises the builtin
        maps into several styles in the Start Game menu, but that information
        is not stored in the recorded game file (after all, only the map itself
        is necessary to replay the game).
        """
        resource_pack = self.rec.get_resource_pack()
        if resource_pack.is_custom_map(self.map_id):
            return GameSettings.MAPSTYLE_CUSTOM
        elif resource_pack.is_real_world_map(self.map_id):
            return GameSettings.MAPSTYLE_REALWORLD
        # TODO add case for the "Special" maps in the HD expansion packs
        return GameSettings.MAPSTYLE_STANDARD

    def is_real_world_map(self):
        """
        Check whether the game was played on a "Real World" map, such as
        Byzantinum or Texas.
        """
        resource_pack = self.rec.get_resource_pack()
        return resource_pack.is_real_world_map(self.map_id)

    def is_custom_map(self):
        """Check whether the game was played on a custom map."""
        resource_pack = self.rec.get_resource_pack()
        return resource_pack.is_custom_map(self.map_id)

    def is_standard_map(self):
        """Check whether the game was played on a builtin map."""
        resource_pack = self.rec.get_resource_pack()
        return resource_pack.is_standard_map(self.map_id)
