import pytest
from ms_cfb.ole_file import OleFile


def test_set_version_exception():
    ole_file = OleFile()
    with pytest.raises(Exception):
        ole_file.set_version(1)


def test_get_version():
    ole_file = OleFile()
    assert ole_file.get_version() == 3
