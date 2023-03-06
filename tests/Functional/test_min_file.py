import os
from ms_cfb.Models.ole_file import OleFile


def test_min_file():
    """
    The smallest file has three sectors, one each:
    header, fat, directory
    """
    ole_file = OleFile()
    ole_file.write_file()
    assert os.path.exists("vbaProject.bin")
   
