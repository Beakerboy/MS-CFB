import pytest
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
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0\x23\xB8\xC2'
          + b'\x33\x24\xD9\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']

    assert dir.to_bytes() == ex


def test_add_created():
    dir = RootDirectory()
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_created(date)
