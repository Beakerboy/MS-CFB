from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import Iterator
from typing import TypeVar
from typing import Any


T = TypeVar('T', bound='ArrayStream')


class ArrayStream(StreamBase):
    """
    An array stream is a stream in which renderable data is
    saved in an array.
    This class is a base class. Child classes must implement
    the _render_element() method.
    """
    # Constructor
    def __init__(self: T, child_sector_size: int) -> None:
        super(ArrayStream, self).__init__()
        self._data = []
        self._child_sector_size = child_sector_size

    # Dunder Methods
    def __iter__(self: T) -> Iterator:
        return iter(self._data)

    def __len__(self: T) -> int:
        return len(self._data)

    # Public Methods
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
        sum = 0
        for stream in self._data:
            sectors = ((stream.stream_size() - 1)
                       // self._child_sector_size
                       + 1)
            sum += sectors * self._child_sector_size
        return sum

    # Private Methods
    def _extend_data(self: T, data: Any) -> None:
        """
        Add new data to the array
        """
        self._data.append(data)

    def _render_element(self: T, index: int) -> bytes:
        """
        Create the binary form of the object.
        This method must be implemented by each child
        if the object contained in the array does not
        have a to_bytes() method.
        """
        return self._data[index].to_bytes()
