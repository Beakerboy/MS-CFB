from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.Directories.directory import Directory
from typing import TypeVar


T = TypeVar('T', bound='DirectoryStream')


class DirectoryStream(ArrayStream):

    # Constructor
    def __init__(self: T) -> None:
        ArrayStream.__init__(self, 128)
        self._padding = (b'\x00' * (16 * 4 + 4) + b'\xff' * 12
                         + b'\x00' * 16 * 3)

    # Public Methods

    def stream_size(self: T) -> int:
    """
    Overrides ArrayStream.stream_size()
    """
        return len(self._data) * 16 * 8

    # Private Methods
    def _render_element(self: T, dir: 'Directory') -> bytes:
        return dir.to_bytes()
