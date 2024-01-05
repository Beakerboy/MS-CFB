from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import Any, Sequence, TypeVar, overload


T = TypeVar('T', bound='ArrayStream')


class ArrayStream(StreamBase, Sequence[T]):
    """
    An array stream is a stream in which renderable data is
    saved in an array.
    This class is a base class. Child classes must implement
    the _render_element() method.
    """
    # Constructor
    def __init__(self: T, child_sector_size: int) -> None:
        super(ArrayStream, self).__init__()
        self._data: list = []
        self._child_sector_size = child_sector_size

    # Dunder Methods

    @overload
    def __getitem__(self, idx: int) -> T: ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[T]: ...

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise Exception("Subclass disallows slicing")

        return self._data[item]

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

    def _render_element(self: T, data: Any) -> bytes:
        raise Exception("must be implemented bu child")
