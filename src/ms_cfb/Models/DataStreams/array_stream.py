from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import Iterator
from typing import TypeVar
from typing import Any


T = TypeVar('T', bound='ArrayStream')


class ArrayStream(StreamBase):
    """
    An ArrayStream is a stream that is a list of renderable elements.
    """
    def __init__(self: T) -> None:
        super(ArrayStream, self).__init__()
        self._data = []

    def __iter__(self: T) -> Iterator:
        return iter(self._data)

    def __len__(self: T) -> int:
        return len(self._data)

    def to_file(self: T, path: str) -> None:
        f = open(path, "wb")
        for element in self._data:
            f.write(self._render_element(element))
        length = f.tell()
        if length % self._storage_sector_size == 0:
            mod = self._storage_sector_size
        else:
            mod = length % self._storage_sector_size
        fill = (self._storage_sector_size - mod) // len(self._padding)
        f.write(self._padding * fill)
        f.close()

    def stream_size(self: T) -> int:
        """
        From StreamBase
        """
        sum = 0
        for stream in self._data:
            sectors = ((stream.stream_size() - 1)
                       // 64
                       + 1)
            sum += sectors * 64
        return sum

    def _extend_data(self: T, data: Any) -> None:
        """
        Add new data to the array
        """
        self._data.append(data)
