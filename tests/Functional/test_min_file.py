import os
from ms_cfb.ole_file import OleFile


def test_min_file():
    """
    The smallest file has three sectors, one each:
    header, fat, directory
    """
    ole_file = OleFile()
    ole_file.create_file(".")
    assert os.stat("vbaProject.bin").st_size == 512 * 3

    f = open("vbaProject.bin", "rb")
    sector1 = ("D0CF 11E0 A1B1 1AE1 0000 0000 0000 0000",
               "0000 0000 0000 0000 3E00 0300 FEFF 0900",
               "0600 0000 0000 0000 0000 0000 0100 0000",
               "0100 0000 0000 0000 0010 0000 0000 0000",
               "0100 0000 FEFF FFFF 0000 0000 0000 0000")
    expected = bytes.fromhex(" ".join(sector1)) + b'\xff' * 16 * 27
    assert f.read(512) == expected

    sector2 = (bytes.fromhex("FDFF FFFF FEFF FFFF FFFF FFFF FFFF FFFF")
              + b'\xff' * 16 * 27)
    assert f.read(512) == expected
