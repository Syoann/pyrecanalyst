import re


class MapName:
    """
    Extracts the map name from the Objectives tab of a recorded game. That's the
    only place where the name of a custom random map is stored.
    """
    def __init__(self, rec):
        # Recorded game file to use.
        self.rec = rec

        # Possible formats for map type lines in the Objectives tab.
        # The Map Type strings used in the Objectives message tab are stored in
        # string id 9654. This array was generated using:
        # grep "9654" "SteamApps/common/Age2HD/resources/*/strings/key-value/key-value-strings-utf8.txt"
        #
        # HD Edition uses UTF-8, but older versions used localization-specific code pages.
        # Code page information for zh, jp and ko was taken from:
        # https:#msdn.microsoft.com/en-us/library/cc194886.aspx
        self.map_type_regexes = {
            'br': {'content': 'Tipo de Mapa: (.*)', 'encoding': 'utf-8'},
            'de': {'content': 'Kartentyp: (.*)', 'encoding': 'utf-8'},
            'en': {'content': 'Map Type: (.*)', 'encoding': 'utf-8'},
            'es': {'content': 'Tipo de mapa: (.*)', 'encoding': 'utf-8'},
            'fr': {'content': 'Type de carte : (.*)', 'encoding': 'utf-8'},
            'it': {'content': 'Tipo di mappa: (.*)', 'encoding': 'utf-8'},
            'jp': {'content': 'マップの種類: (.*)', 'encoding': 'cp932'},
            'ko': {'content': '지도 종류: (.*)', 'encoding': 'cp949'},
            'nl': {'content': 'Kaarttype: (.*)', 'encoding': 'utf-8'},
            'ru': {'content': 'Тип карты: (.*)', 'encoding': 'windows-1251'},
            'zh': {'content': '地图类型: (.*)', 'encoding': 'cp936'},
            'jp_utf-8': {'content': 'マップの種類: (.*)', 'encoding': 'utf-8'},
            'ko_utf-8': {'content': '지도 종류: (.*)', 'encoding': 'utf-8'},
            'zh_utf8': {'content': '地图类型: (.*)', 'encoding': 'utf-8'},
        }

    def run(self):
        """Run the processor."""
        header = self.rec.header()
        messages = header.messages
        instructions = messages["instructions"]

        for line in instructions.split(b'\n'):
            # We don't know what language the game was played in, so we try
            # every language we know.
            for lang, attr in self.map_type_regexes.items():
                try:
                    matches = re.match(attr['content'], line.decode(attr['encoding']))
                    if matches:
                        return matches.group(1)
                except UnicodeDecodeError:
                    pass
