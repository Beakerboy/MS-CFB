from ms_cfb.Models.Filesystems.fat_filesystem import FatFilesystem
from ms_cfb.Models.DataStreams.stream_base import StreamBase


def test_initialProperties():
    chain = FatFilesystem(512)
    assert chain.getSectorSize() == 512
    assert len(chain) == 1
    assert chain.get_chain() == [0xfffffffd]


def test_addingChain():
    chain = FatFilesystem(512)
    stream = StreamStub()
    chain.add_stream(stream)
    assert len(chain) == 2
    assert chain.get_chain() == [0xfffffffd, 0xfffffffe]

    stream2 = StreamStub()
    chain.add_stream(stream2)
    assert len(chain) == 3
    assert chain.get_chain() == [0xfffffffd, 0xfffffffe, 0xfffffffe]


def test_extendChain():
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    stream2 = StreamStub()
    chain.add_stream(stream2)
    chain.extendChain(stream1, 2)
    assert len(chain) == 5
    assert chain.get_chain() == [0xfffffffd, 3, 0xfffffffe, 4, 0xfffffffe]


def test_newFatTableSector():
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extendChain(stream1, 126)
    stream2 = StreamStub()
    chain.add_stream(stream2)
    assert chain.get_chain()[126:] == [127, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_extendThroughFatSector():
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extendChain(stream1, 126)
    assert len(chain) == 128

    chain.extendChain(stream1, 1)
    assert chain.get_chain()[126:] == [127, 129, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_lastSectorOnFatSector():
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extendChain(stream1, 125)
    assert len(chain) == 127
    chain.extendChain(stream1, 2)
    assert chain.get_chain()[126:] == [127, 129, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_extendThroughFatSector2():
    chain = FatFilesystem(512)
    stream1 = StreamStub()
    chain.add_stream(stream1)
    chain.extendChain(stream1, 125)
    chain.extendChain(stream1, 3)
    assert len(chain) == 131
    assert chain.get_chain()[126:] == [127, 129, 0xFFFFFFFD, 130, 0xFFFFFFFE]


def test_write_chain():
    fs = FatFilesystem(512)
    fs.write_chain("chain.bin")
    f = open("chain.bin", "rb")
    assert f.read() == bytes.fromhex("FDFF FFFF")
    

class StreamStub(StreamBase):
    def streamSize(self):
        return 1
