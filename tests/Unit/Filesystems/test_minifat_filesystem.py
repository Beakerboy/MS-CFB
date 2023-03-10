from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase
from ms_cfb.Models.Filesystems.minifat_filesystem import MinifatFilesystem
from ms_cfb.Models.DataStreams.stream_base import StreamBase


def test_initial_properties() -> None:
    chain = MinifatFilesystem()
    assert chain.get_sector_size() == 64
    assert len(chain) == 0


def test_adding_chain() -> None:
    fs = FilesystemStub(16)
    chain = MinifatFilesystem()
    chain.set_storage_chain(fs)
    stream = StreamStub()
    chain.add_stream(stream)
    assert len(chain) == 1
    assert chain.get_chain() == [0xfffffffe]
    assert stream.get_sectors() == [1]

    stream2 = StreamStub()
    chain.add_stream(stream2)
    assert len(chain) == 3
    assert chain.get_chain() == [0xfffffffe, 0xfffffffe]


class StreamStub(StreamBase):
    def stream_size(self):
        return 1


class FilesystemStub(FilesystemBase):
    pass
