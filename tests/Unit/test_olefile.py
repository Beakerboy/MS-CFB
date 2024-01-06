import pytest
import random
import string
from ms_cfb.ole_file import OleFile


def test_set_version_exception() -> None:
    ole_file = OleFile()
    with pytest.raises(Exception):
        ole_file.version = 1


def test_version_property() -> None:
    ole_file = OleFile()
    assert ole_file.version == 3
    ole_file.version = 4
    assert ole_file.version == 4
    ole_file.version = 3
    assert ole_file.version == 3


def test_extract() -> None:
    ole_file = OleFile.create_from_file('tests/vbaProject.bin')
    sectors = ole_file.minifat_chain.get_streams().get_sectors()
    assert sectors == [3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17]
    dir = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=7))
    ole_file.extract_stream('PROJECTwm', dir)
    fa = open(dir + '/PROJECTwm.bin', 'rb')
    actual = fa.read()
    fe = open('tests/vbaProject.bin', 'rb')
    fe.seek(0x2100)
    expected = fe.read(86)
    assert actual == expected
