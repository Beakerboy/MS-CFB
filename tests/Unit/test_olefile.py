import pytest
from ms_cfb.ole_file import OleFile


def test_set_version_exception() -> None:
    ole_file = OleFile()
    with pytest.raises(Exception):
        ole_file.set_version(1)


def test_get_version() -> None:
    ole_file = OleFile()
    assert ole_file.get_version() == 3
    ole_file.set_version(4)
    assert ole_file.get_version() == 4
    ole_file.set_version(3)
    assert ole_file.get_version() == 3

def test_extract() -> None:
    ole_file = OleFile.create_from_file('')
    ole_file.extract_stream('PROJECTwm')
    
