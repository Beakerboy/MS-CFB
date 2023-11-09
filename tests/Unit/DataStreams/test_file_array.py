from ms_cfb.Models.DataStreams.file_array import FileArray
from typing import TypeVar


T = TypeVar('T', bound='FakeStream')


class FakeStream():

    def __init__(self: T, stream_size: int) -> None:
        self._stream_size = stream_size

    def stream_size(self: T) -> int:
        """
        From StreamBase
        """
        return self._stream_size


def test_constructor() -> None:
    stream = FileArray(64)
    assert isinstance(stream, FileArray)


def test_stream_size() -> None:
    stream = FileArray()
    stream.set_storage_sector_size(512)
    # The array will cover an 64 bytes
    # when even a small amount of data is added.
    mock = FakeStream(5)
    stream.append(mock)
    assert stream.stream_size() == 64
    # if another small amount is added, it increases
    # by multiples of 64
    mock2 = FakeStream(65)
    stream.append(mock2)
    assert stream.stream_size() == 192
