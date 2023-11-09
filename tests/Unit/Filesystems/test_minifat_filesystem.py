from ms_cfb.Models.Filesystems.minifat_filesystem import MinifatFilesystem
from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import TypeVar


def test_initial_properties() -> None:
    chain = MinifatFilesystem()
    assert chain.get_sector_size() == 64
    assert len(chain) == 0


def test_adding_chain() -> None:
    """
    Add description. why is chain storage sector 16?
    """
    chain = MinifatFilesystem()
    chain.set_storage_sector_size(16)
    stream = StreamStub()
    stream.set_stream_size(1)
    stream.set_storage_sector_size(64)
    chain.add_stream(stream)
    assert len(chain) == 1
    assert chain.get_chain() == [0xfffffffe]
    assert stream.get_sectors() == [0]

    stream2 = StreamStub()
    stream2.set_stream_size(1)
    stream2.set_storage_sector_size(64)
    chain.add_stream(stream2)
    assert len(chain) == 2
    assert chain.get_chain() == [0xfffffffe, 0xfffffffe]

    chain.extend_chain(stream, 2)
    assert len(chain) == 4
    assert chain.get_chain() == [2, 0xfffffffe, 3, 0xfffffffe]
    assert stream.get_sectors() == [0, 2, 3]

    chain.to_file("test.bin")
    f = open("test.bin", "rb")
    expected = "02000000 FEFFFFFF 03000000 FEFFFFFF"
    assert f.read() == bytes.fromhex(expected)


def test_adding_chain_longer_storage() -> None:
    """
    Add description. Why is chain storage sector 24?
    """
    chain = MinifatFilesystem()
    chain.set_storage_sector_size(24)
    stream = StreamStub()
    stream.set_stream_size(1)
    stream.set_storage_sector_size(64)
    chain.add_stream(stream)
    stream2 = StreamStub()
    stream2.set_stream_size(1)
    stream2.set_storage_sector_size(64)
    chain.add_stream(stream2)
    chain.extend_chain(stream, 2)
    chain.to_file("test.bin")
    f = open("test.bin", "rb")
    expected = ["02000000 FEFFFFFF 03000000 FEFFFFFF",
                "FFFFFFFF FFFFFFFF"]
    assert f.read() == bytes.fromhex(" ".join(expected))


def test_start_sector() -> None:
    pass


T = TypeVar('T', bound='StreamStub')


class StreamStub(StreamBase):
    def set_stream_size(self: T, size: int) -> None:
        self._size = size

    def stream_size(self: T) -> int:
        return self._size
