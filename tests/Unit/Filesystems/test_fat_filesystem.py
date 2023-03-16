from ms_cfb.Models.Filesystems.fat_filesystem import FatFilesystem
from ms_cfb.Models.DataStreams.stream_base import StreamBase


def test_initial_properties() -> None:
    chain = FatFilesystem(512)
    assert chain.get_sector_size() == 512
    assert len(chain) == 1
    assert chain.get_chain() == [0xfffffffd]


def test_adding_chain() -> None:
    chain = FatFilesystem(512)
    stream = StreamStub()
    chain.add_stream(stream)
    assert len(chain) == 2
    assert chain.get_chain() == [0xfffffffd, 0xfffffffe]

    stream2 = StreamStub()
    chain.add_stream(stream2)
    assert len(chain) == 3
    assert chain.get_chain() == [0xfffffffd, 0xfffffffe, 0xfffffffe]


def test_extend_chain() -> None:
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    stream2 = StreamStub()
    chain.add_stream(stream2)
    chain.extend_chain(stream1, 2)
    assert len(chain) == 5
    assert chain.get_chain() == [0xfffffffd, 3, 0xfffffffe, 4, 0xfffffffe]


def test_new_fat_table_sector() -> None:
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extend_chain(stream1, 126)
    stream2 = StreamStub()
    chain.add_stream(stream2)
    assert chain.get_chain()[126:] == [127, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_extend_through_fat_sector() -> None:
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extend_chain(stream1, 126)
    assert len(chain) == 128

    chain.extend_chain(stream1, 1)
    assert chain.get_chain()[126:] == [127, 129, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_last_sector_on_fat_sector() -> None:
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extend_chain(stream1, 125)
    assert len(chain) == 127
    chain.extend_chain(stream1, 2)
    assert chain.get_chain()[126:] == [127, 129, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_extend_through_fat_sector2() -> None:
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extend_chain(stream1, 125)
    chain.extend_chain(stream1, 3)
    assert len(chain) == 131
    assert chain.get_chain()[126:] == [127, 129, 0xFFFFFFFD, 130, 0xFFFFFFFE]


def test_write_chain() -> None:
    fs = FatFilesystem(512)
    fs.write_chain("chain.bin")
    f = open("chain.bin", "rb")
    assert f.read() == bytes.fromhex("FDFF FFFF")

from typing import TypeVar


T = TypeVar('T', bound='ArrayStream')


class StreamStub(StreamBase):
    def stream_size(self: T) -> int:
        return 1
