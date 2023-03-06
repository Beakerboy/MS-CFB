import os
from ms_cfb.ole_file import OleFile


def test_min_file():
    """
    The smallest file has three sectors, one each:
    header, fat, directory
    """
    ole_file = OleFile()
    ole_file.create_file(".")
    assert os.path.exists("vbaProject.bin")
    assert os.stat("vbaProject.bin").st_size == 512 * 3
