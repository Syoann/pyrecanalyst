class Civilization:
    """Utilities for dealing with Age of Empires civilizations."""
    NONE = 0
    BRITONS = 1
    FRANKS = 2
    GOTHS = 3
    TEUTONS = 4
    JAPANESE = 5
    CHINESE = 6
    BYZANTINES = 7
    PERSIANS = 8
    SARACENS = 9
    TURKS = 10
    VIKINGS = 11
    MONGOLS = 12
    CELTS = 13
    SPANISH = 14
    AZTECS = 15
    MAYANS = 16
    HUNS = 17
    KOREANS = 18
    ITALIANS = 19
    INDIANS = 20
    INCAS = 21
    MAGYARS = 22
    SLAVS = 23

    MALIANS = 24
    ETHIOPIANS = 25
    BERBERS = 26
    PORTUGUESE = 27
    BURMESE = 28
    KHMER = 29
    MALAY = 30
    VIETNAMESE = 31


    CIV_NAMES = {
        NONE: '',
        BRITONS: 'Britons',
        FRANKS: 'Franks',
        GOTHS: 'Goths',
        TEUTONS: 'Teutons',
        JAPANESE: 'Japanese',
        CHINESE: 'Chinese',
        BYZANTINES: 'Byzantines',
        PERSIANS: 'Persians',
        SARACENS: 'Saracens',
        TURKS: 'Turks',
        VIKINGS: 'Vikings',
        MONGOLS: 'Mongols',
        CELTS: 'Celts',
        SPANISH: 'Spanish',
        AZTECS: 'Aztecs',
        MAYANS: 'Mayans',
        HUNS: 'Huns',
        KOREANS: 'Koreans',
        ITALIANS: 'Italians',
        INDIANS: 'Indians',
        INCAS: 'Incas',
        MAGYARS: 'Magyars',
        SLAVS: 'Slavs',
        MALIANS: 'Malians',
        ETHIOPIANS: 'Ethiopians',
        BERBERS: 'Berbers',
        PORTUGUESE: 'Portuguese',
        BURMESE: 'Burmese',
        KHMER: 'Khmer',
        MALAY: 'Malay',
        VIETNAMESE: 'Vietnamese'
    }

    @staticmethod
    def get_civ_name(id):
        """Get the in-game name of a civilization."""
        if id in Civilization.CIV_NAMES:
            return Civilization.CIV_NAMES[id]

    @staticmethod
    def is_aok_civ(id):
        """Checks if a civilization is included in the Age of Kings base game."""
        return id in (Civilization.BRITONS,
                      Civilization.FRANKS,
                      Civilization.GOTHS,
                      Civilization.TEUTONS,
                      Civilization.JAPANESE,
                      Civilization.CHINESE,
                      Civilization.BYZANTINES,
                      Civilization.PERSIANS,
                      Civilization.SARACENS,
                      Civilization.TURKS,
                      Civilization.VIKINGS,
                      Civilization.MONGOLS,
                      Civilization.CELTS)

    @staticmethod
    def is_aoc_civ(id):
        """Checks if a civilization was added in the Age of Conquerors expansion."""
        return id in (Civilization.SPANISH,
                      Civilization.AZTECS,
                      Civilization.MAYANS,
                      Civilization.HUNS,
                      Civilization.KOREANS)

    @staticmethod
    def is_forgotten_civ(id):
        """
        Checks if a civilization was added in the Forgotten Empires expansion.
        false otherwise.
        """
        return id in (Civilization.ITALIANS,
                      Civilization.INDIANS,
                      Civilization.INCAS,
                      Civilization.MAGYARS,
                      Civilization.SLAVS)

    @staticmethod
    def is_african_kingdoms_civ(id):
        """
        Checks if a civilization was added in the African Kingdoms expansion.
        """
        return id in (Civilization.MALIANS,
                      Civilization.ETHIOPIANS,
                      Civilization.BERBERS,
                      Civilization.PORTUGUESE)

    @staticmethod
    def is_rajas_civ(id):
        """
        Checks if a civilization was added in the Rise of the Rajas expansion.
        """
        return id in (Civilization.BURMESE,
                      Civilization.KHMER,
                      Civilization.MALAY,
                      Civilization.VIETNAMESE)
