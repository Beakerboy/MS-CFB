import pytest
from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.Directories.root_directory import RootDirectory


def test_directory():

    dir = RootDirectory()
    dir.name = "Root Entry"
    assert dir.name_size() == 22
    dir.set_modified(0x01D92433C2B823C0)
    dir.set_start_sector(3)
    dir.color = 0

    ex = ["5200 6F00 6F00 7400 2000 4500 6E00 7400",
          "7200 7900 0000 0000 0000 0000 0000 0000",
          "0000 0000 0000 0000 0000 0000 0000 0000",
          "0000 0000 0000 0000 0000 0000 0000 0000",
          "1600 0500 FFFF FFFF FFFF FFFF ffff ffff",
          "0000 0000 0000 0000 0000 0000 0000 0000",
          "0000 0000 0000 0000 0000 0000 C023 B8C2",
          "3324 D901 0300 0000 0000 0000 0000 0000"]

    assert dir.to_bytes() == bytes.fromhex(" ".join(ex))


def test_add_created():
    dir = RootDirectory()
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_created(date)


def test_from_binary():
    data = (b''
            + b'R\x00o\x00o\x00t\x00 \x00E\x00n\x00t\x00'
            + b'r\x00y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x16\x00\x05\x01\xff\xff\xff\xff\xff\xff\xff\xff\x01\x00\x00\x00
            + b'\x00gaVT\xc1\xce\x11\x85S\x00\xaa\x00\xa1\xf9['
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\xbe\xab0'
            + b'\x00\x00\x00\x00\x03\x00\x00\x00@\x02\x00\x00\x00\x00\x00\x00')
    root = Directory.from_binary(data)
