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
    ole_file = OleFile.create_from_file('tests/vbaProject.bin')
    sectors = ole_file.get_minifat_chain().get_streams().get_sectors()
    assert sectors == [3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17]
    ole_file.extract_stream('PROJECTwm')
    f = open('PROJECTwm.bin', 'rb')
    actual = f.read(82)
    expected = (''
                + '5468 6973 576F 726B 626F 6F6B 0054 0068'
                + '0069 0073 0057 006F 0072 006B 0062 006F'
                + '006F 006B 0000 0053 6865 6574 3100 5300'
                + '6800 6500 6500 7400 3100 0000 4D6F 6475'
                + '6C65 3100 4D00 6F00 6400 7500 6C00 6500'
                + '3100 0000 0000')
    assert actual == bytes.fromhex(expected)
