import struct
import zlib

class StreamExtractor:
    """
    Extracts header and body parts from recorded game files.
    Position of the first header byte in the file.
    """
    def __init__(self, fp, options=None):
        if options is None:
            options = {}

        self.header_start = 0
        self.header_len = 0
        self.header_contents = None
        self.body_contents = None
        self.fp = fp
        self.options = options
        self.options.update({'memoryLimit': 16777216})

    def manually_determine_header_length(self):
        """
        Determine the header length if the Header Length field was not set in the
        file.
        """
        separator = struct.pack('<cccc', b'\xf4', b'\x01', b'\x00', b'\x00')
        initial_base = self.fp.tell()
        base = initial_base
        buffer = self.fp.read(8192)
        while buffer:
            index = buffer.find(separator)
            if index != -1:
                self.header_len = base + index - 4
            base += len(buffer)
            buffer = self.fp.read(8192)

        self.fp.seek(initial_base)

    def get_file_size(self):
        """Get the total size of the file."""
        self.fp.seek(0, 2)
        return self.fp.tell()

    def determine_header_length(self):
        """Find the header length."""
        raw_read = self.fp.read(4)

        if not raw_read or len(raw_read) < 4:
            raise Exception('Unable to read the header length')

        self.header_len = struct.unpack('<L', raw_read)[0]

        if not self.header_len:
            self.manually_determine_header_length()
            if not self.header_len:
                raise Exception('Header length is zero')
        raw_read = self.fp.read(4)
        next_pos = struct.unpack('<L', raw_read)[0]
        has_next_pos = next_pos == 0 or next_pos < self.get_file_size()
        self.header_start = 4
        if has_next_pos:
            self.header_start = 8
        self.header_len -= self.header_start

    def get_header(self):
        """Read or return the Recorded Game file's header block."""
        if self.header_contents:
            return self.header_contents
        if not self.header_len:
            self.determine_header_length()
        self.fp.seek(self.header_start, 0)
        read = 0
        bindata = b''
        buff = self.fp.read(self.header_len - read)
        while read < self.header_len and buff:
            read += len(buff)
            bindata += buff
            buff = self.fp.read(self.header_len - read)

        del buff
        self.header_contents = zlib.decompress(bindata, -15)
        del bindata
        if not self.header_contents:
            raise Exception('Cannot decompress header section')
        return self.header_contents

    def get_body(self):
        """Read or return the Recorded Game file's body."""
        if self.body_contents:
            return self.body_contents
        if not self.header_len:
            self.determine_header_length()

        self.fp.seek(self.header_start + self.header_len, 0)
        self.body_contents = ''
        self.body_contents = self.fp.read()
        return self.body_contents
