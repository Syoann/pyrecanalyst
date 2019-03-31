import json
import os


class BasicTranslator:
    """
    Super tiny default translator. Uses translations provided with RecAnalyst,
    with no possibility of customisation.
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
                self.translations[filename] = json.load(fh)

        return self.get(self.translations[filename], keys)

    def get_file_path(self, locale, filename):
        """Get the path to a translation file."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            os.pardir, 'resources', 'lang', locale, filename + '.py')
        return os.path.normpath(path)


    def get(self, arr, keys):
        """Get a value from a property list."""
        if not arr:
            return None

        prop, val = [str(k) for k in keys]
        if prop in arr and val in arr[prop]:
            arr = arr[prop][val]
        else:
            return ""
        return arr
