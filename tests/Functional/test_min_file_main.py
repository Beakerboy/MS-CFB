import os
from ms_cfb.ole_file import main


def test_min_file():
    """
    The smallest file has three sectors, one each:
    header, fat, directory
    """
    mocker.patch(
        "sys.argv",
        [
            "ole_file.py",
            "-o",
            "Test123.bin",
            "-/files",
        ],
    )
    main()
    assert os.stat("vbaProject.bin").st_size == 512 * 3

    f = open("vbaProject.bin", "rb")
    sector1 = ("D0CF 11E0 A1B1 1AE1 0000 0000 0000 0000",
               "0000 0000 0000 0000 3E00 0300 FEFF 0900",
               "0600 0000 0000 0000 0000 0000 0100 0000",
               "0100 0000 0000 0000 0010 0000 FEFF FFFF",
               "0100 0000 FEFF FFFF 0000 0000 0000 0000")
    expected = bytes.fromhex(" ".join(sector1)) + b'\xff' * 16 * 27
    assert f.read(512) == expected

    sector2 = (bytes.fromhex("FDFF FFFF FEFF FFFF FFFF FFFF FFFF FFFF")
               + b'\xff' * 16 * 31)
    assert f.read(512) == sector2

    root = ("5200 6F00 6F00 7400 2000 4500 6E00 7400",
            "7200 7900 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "1600 0501 FFFF FFFF FFFF FFFF FFFF FFFF",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 FEFF FFFF 0000 0000 0000 0000")

    unused = b'\x00' * (16 * 4 + 4) + b'\xff' * 12 + b'\x00' * 16 * 3

    sector3 = bytes.fromhex(" ".join(root)) + unused * 3
    assert f.read(512) == sector3
