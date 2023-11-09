from ms_cfb.Models.DataStreams.file_array import FileArray
from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import TypeVar


T = TypeVar('T', bound='FakeStream')


class FakeStream(StreamBase):

    def __init__(self: T, stream_size: int) -> None:
        super(FakeStream, self).__init__()
        self._stream_size = stream_size

    def stream_size(self: T) -> int:
        """
        From StreamBase
        """
        return self._stream_size


def test_constructor() -> None:
    stream = FileArray()
    assert isinstance(stream, FileArray)


def test_stream_size() -> None:
    stream = FileArray()
    stream.set_storage_sector_size(512)
    mock = FakeStream(5)
    stream.append(mock)
    assert stream.stream_size() == 512
