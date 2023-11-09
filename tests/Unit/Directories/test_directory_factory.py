from ms_cfb.Models.Directories.directory_factory import DirectoryFactory
from ms_cfb.Models.Directories.root_directory import RootDirectory


def test_from_binary() -> None:
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
