from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.Directories.directory import Directory
from typing import TypeVar


T = TypeVar('T', bound='DirectoryStream')


class DirectoryStream(ArrayStream):

    def __init__(self: T) -> None:
        ArrayStream.__init__(self)
        self._padding = (b'\x00' * (16 * 4 + 4) + b'\xff' * 12
                         + b'\x00' * 16 * 3)

    def _render_element(self: T, dir: 'Directory') -> bytes:
        return dir.to_bytes()

    def stream_size(self: T) -> int:
        return len(self._data) * 16 * 8
