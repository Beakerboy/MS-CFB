from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.Directories.directory import Directory


class DirectoryStream(ArrayStream):

    def __init__(self) -> None:
        ArrayStream.__init__(self)
        self._padding = (b'\x00' * (16 * 4 + 4) + b'\xff' * 12
                         + b'\x00' * 16 * 3)

    def _render_element(self, dir: 'Directory') -> bytes:
        return dir.to_bytes()

    def stream_size(self) -> int:
        return len(self._data) * 16 * 8
