from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import Iterator


class ArrayStream(StreamBase):

    def __init__(self) -> None:
        super(ArrayStream, self).__init__()
        self._data = []

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def to_file(self, path: str) -> None:
        f = open(path, "wb")
        for element in self._data:
            f.write(self._render_element(element))
        sector_size = self._storage_chain.get_sector_size()
        length = f.tell()
        if length % sector_size == 0:
            mod = sector_size
        else:
            mod = length % sector_size
        fill = (sector_size - mod) // len(self._padding)
        f.write(self._padding * fill)
        f.close()

    def stream_size(self) -> int:
        sum = 0
        sector_size = self._storage_chain.get_sector_size()
        for stream in self._data:
            sectors = (stream.stream_size() - 1) // sector_size + 1
            sum += sectors * sector_size
        return sum

    def _render_element(self, element) -> bytes:
        return element.to_bytes()

    def _extend_data(self, data) -> None:
        """
        Add new data to the array
        """
        self._data.append(data)
