import pytest
from ms_cfb.Models.Directories.stream_directory import StreamDirectory


def test_constructor():
    dir = StreamDirectory("name", "/path")
    assert isinstance(dir, StreamDirectory)


def test_add_created():
    dir = StreamDirectory("name", "/path")
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_created(date)


def test_add_modified():
    dir = StreamDirectory("name", "/path")
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_modified(date)

def test_file_size():
    dir = StreamDirectory("name", "tests/Test.txt")
    assert dir.file_size() == 5
