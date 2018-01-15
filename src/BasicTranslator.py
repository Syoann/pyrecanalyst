import os


class BasicTranslator(object):
    """
    Super tiny default translator for when RecAnalyst is used outside of Laravel.
    Uses translations provided with RecAnalyst, with no possibility of
    customisation.
    """

    def __init__(self, locale='en'):
        # Current locale.
        self.locale = locale
        self.translations = {}

    def trans(self, file, keys):
        if not file in self.translations:
            current = self.get_file_path(self.locale, file)
            # Default to English
            if not os.path.isfile(current):
                current = self.get_file_path('en', file)
            translation_table = eval(open(current).read())
            self.translations[file] = translation_table
        return self.get(self.translations[file], keys)

    def get_file_path(self, locale, file):
        """Get the path to a translation file."""
        return os.path.dirname(os.path.abspath(__file__)) + '/../resources/lang/' + locale + '/' + file + '.py'

    def get(self, arr, lst):
        """Get a value from a property list."""
        if not arr:
            return None

        prop, val = lst
        if prop in arr and val in arr[prop]:
            arr = arr[prop][val]
        else:
            return ""
        return arr
