from ms_cfb.Models.DataStreams.array_stream import ArrayStream


class DirectoryStream(ArrayStream):

    def __init__(self):
        ArrayStream.__init__(self)
        self._padding = (b'\x00' * (16 * 4 + 4) + b'\xff' * 12
                         + b'\x00' * 16 * 3)

    def _render_element(self, dir) -> bytes:
        return dir.to_bytes()

    def stream_size(self) -> int:
        return len(self._data) * 16 * 8
