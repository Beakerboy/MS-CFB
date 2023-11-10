from ms_cfb.Models.Directories.directory_factory import DirectoryFactory
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory


def test_root_from_binary() -> None:
    da = (b''
          + b'R\x00o\x00o\x00t\x00 \x00E\x00n\x00t\x00'
          + b'r\x00y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x16\x00\x05\x00\xff\xff\xff\xff\xff\xff\xff\xff\x01\x00\x00\x00'
          + b'\x00gaVT\xc1\xce\x11\x85S\x00\xaa\x00\xa1\xf9['
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x23\xb8\xc2'
          + b'\x33\x24\xd9\x01\x03\x00\x00\x00@\x02\x00\x00\x00\x00\x00\x00')
    root = DirectoryFactory.from_binary(da)
    assert isinstance(root, RootDirectory)
    expected = ("Root Entry\n\tCreated: 1601-01-01 00:00:00\n\tModified: " +
                "2023-01-09 14:07:51.292000\n\tStart Sector: 3\n\tSize: 576")
    assert str(root) == expected


def test_storage_from_binary() -> None:
    da = (""
          + "5600 4200 4100 0000 0000 0000 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0800 0100 FFFF FFFF FFFF FFFF 0400 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 C023 B8C2 3324 D901 C023 B8C2"
          + "3324 D901 0000 0000 0000 0000 0000 0000")
    storage = DirectoryFactory.from_binary(bytes.fromhex(da))
    assert isinstance(storage, StorageDirectory)
    expected = ("VBA\n\tCreated: 2023-01-09 14:07:51.292000\n\tModified: "
                + "2023-01-09 14:07:51.292000\n\tStart Sector: 0\n\tSize: 0")
    assert str(storage) == expected


def test_stream_from_binary() -> None:
    da = (""
          + "5300 6800 6500 6500 7400 3100 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0E00 0201 0600 0000 FFFF FFFF FFFF FFFF"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 0000 0000 0000 0000 0000 0000"
          + "0000 0000 1000 0000 DF03 0000 0000 0000")
    stream = DirectoryFactory.from_binary(bytes.fromhex(da))
    assert isinstance(stream, StreamDirectory)
    expected = ("Sheet1\n\tCreated: 1601-01-01 00:00:00\n\tModified: "
                + "1601-01-01 00:00:00\n\tStart Sector: 16\n\tSize: 991")
    assert str(stream) == expected
