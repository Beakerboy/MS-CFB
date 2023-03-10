from ms_cfb.Models.DataStreams.stream_base import StreamBase


class ArrayStream(StreamBase):

    def __init__(self):
        super(ArrayStream, self).__init__()
        self._data = []

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def to_file(self, path):
        f = open(path, "wb")
        for element in self._data:
            f.write(self._render_element(element))
        f.close()

    def stream_size(self) -> int:
        sum = 0
        for stream in self._data:
            sum += stream.stream_size()

    def _render_element(self, element) -> bytes:
        return element.to_bytes()

    def _extend_data(self, data) -> None:
        """
        Add new data to the array
        """
        self._data.append(data)
