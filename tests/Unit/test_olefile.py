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
    ole_file.extract_stream('PROJECTwm')
    f = open('PROJECTwm.bin', 'rb')
    actual = f.read()
    expected = (''
                + '5468 6973 57 6F 72 6B 62 6F 6F 6B 00 54 00 68'
                + '0069 0073 00 57 00 6F 00 72 00 6B 00 62 00 6F  .i.s.W.o.r.k.b.o
                + '006F 006B 00 00 00 53 68 65 65 74 31 00 53 00  .o.k...Sheet1.S.
                + '6800 6500 65 00 74 00 31 00 00 00 4D 6F 64 75  h.e.e.t.1...Modu
                + '6C65 3100 4D 00 6F 00 64 00 75 00 6C 00 65 00  le1.M.o.d.u.l.e.
                + '3100')
    assert actual == b''
