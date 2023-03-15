from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from typing import TypeVar


T = TypeVar('T', bound='NumberStream')


class NumberStream(ArrayStream):

    def _render_element(self: T, element) -> bytes:
        return element.to_bytes(4, "little")

    def stream_size(self: T) -> int:
        return len(self._data) * 4
