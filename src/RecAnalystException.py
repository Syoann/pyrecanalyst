class RecAnalystException(Exception):
    # The feature or option is planned but has not yet been implemented. It
    # should be available in a future revision of the package.
    NOT_IMPLEMENTED = 0x0001

    # Trigger info block has not been found in the header section.
    TRIGGERINFO_NOTFOUND = 0x0001

    # Game settings block has not been found in the header section.
    GAMESETTINGS_NOTFOUND = 0x0002

    # No input has been specified for analysis.
    FILE_NOT_SPECIFIED = 0x0003

    # File format is not supported for analysis.
    FILEFORMAT_NOT_SUPPORTED = 0x0004

    # Error reading the header length information.
    HEADERLEN_READERROR = 0x0005

    # Empty header length has been found.
    EMPTY_HEADER = 0x0006

    # Error decompressing header section.
    HEADER_DECOMPRESSERROR = 0x0007

    def __init__(self, msg='', code=0):
        super(RecAnalystException, self).__init__(self, msg, int(code))

    # String representation of the exception.
    def __str__(self):
        return super(RecAnalystException, self).__str__(self)
