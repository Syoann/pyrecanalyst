import os


class BasicTranslator:
    """
    Super tiny default translator for when RecAnalyst is used outside of Laravel.
    Uses translations provided with RecAnalyst, with no possibility of
    customisation.
    """

    def __init__(self, locale='en'):
        # Current locale.
        self.locale = locale
        self.translations = {}

    def __del__(self):
        ( f.close() for f in self.translations.values() )

    def trans(self, filename, keys):
        if not filename in self.translations:
            current = self.get_file_path(self.locale, filename)
            # Default to English
            if not os.path.isfile(current):
                current = self.get_file_path('en', filename)

            with open(current) as fh:
                translation_table = eval(fh.read())
                self.translations[filename] = translation_table

        return self.get(self.translations[filename], keys)

    def get_file_path(self, locale, filename):
        """Get the path to a translation file."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            os.pardir, 'resources', 'lang', locale, filename + '.py')
        return os.path.normpath(path)


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
