import pytest
import uuid
from ms_cfb.Models.Directories.stream_directory import StreamDirectory


def test_constructor() -> None:
    dir = StreamDirectory("name", "/path")
    assert isinstance(dir, StreamDirectory)


def test_add_created() -> None:
    dir = StreamDirectory("name", "/path")
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_created(date)


def test_add_modified() -> None:
    dir = StreamDirectory("name", "/path")
    date = 0x12345
    with pytest.raises(Exception):
        dir.set_modified(date)


def test_file_size() -> None:
    dir = StreamDirectory("name", "tests/Test.txt")
    assert dir.file_size() == 5


def test_sectors_used() -> None:
    dir = StreamDirectory("name", "tests/Test.txt")
    assert dir.minifat_sectors_used() == 1


def test_class_id_exception() -> None:
    dir = StreamDirectory("name", "/path")
    guid = uuid.uuid1()
    with pytest.raises(Exception):
        dir.set_clsid(guid)


def test_class_id() -> None:
    dir = StreamDirectory("name", "/path")
    assert dir.get_clsid().int == 0x00
    guid = uuid.UUID(int=0x00)
    dir.set_clsid(guid)
    assert dir.get_clsid().int == 0x00
