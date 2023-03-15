import os
import pytest
import shutil
from ms_cfb.ole_file import main
from ms_dtyp.filetime import Filetime


@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:
    os.mkdir("./files")
    os.mkdir("./files/Storage 1")

    stream1_data = bytes("Data for stream 1", "utf8") * 32
    f = open("./files/Storage 1/Stream 1.bin", "wb")
    f.write(stream1_data)
    f.close()
    ft = Filetime.from_msfiletime(0x01BAB44B13921E80)
    ts = ft.timestamp()
    os.utime("./files/Storage 1", (ts, ts))
    os.utime("./files", (ts, ts))
    # A test function will be run at this point
    yield
    # Code that will run after your test
    names = ["example_test.bin"]
    for name in names:
        if os.path.isfile(name):
            os.remove(name)
    shutil.rmtree("./files")


def test_example_file(mocker):
    """
    The example file as described in MS-CFB.
    The fixture generated the file and directories, the test method
    will create the output as if run from the command line as:
    python ole_file.py -o example_test.bin -x tests/example.yml ./files
    """
    filename = "example_test.bin"
    mocker.patch(
        "sys.argv",
        [
            "ole_file.py",
            "-o",
            filename,
            "-x",
            "tests/example.yml",
            "./files",
        ],
    )
    main()
    assert os.stat(filename).st_size == 512 * 6

    mod_time = os.stat("./files").st_mtime
    ft = Filetime.fromtimestamp(mod_time)
    assert ft.to_msfiletime() == 0x01BAB44B13921E80

    f = open(filename, "rb")
    sector1 = ("D0CF 11E0 A1B1 1AE1 0000 0000 0000 0000",
               "0000 0000 0000 0000 3E00 0300 FEFF 0900",
               "0600 0000 0000 0000 0000 0000 0100 0000",
               "0100 0000 0000 0000 0010 0000 0200 0000",
               "0100 0000 FEFF FFFF 0000 0000 0000 0000")
    expected = bytes.fromhex(" ".join(sector1)) + b'\xff' * 16 * 27
    assert f.read(512) == expected

    sector2 = (bytes.fromhex("FDFF FFFF FEFF FFFF FEFF FFFF 0400 0000 FE")
               + b'\xff' * (16 * 31 - 1))
    assert f.read(512) == sector2

    root = ("5200 6F00 6F00 7400 2000 4500 6E00 7400",
            "7200 7900 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "1600 0501 FFFF FFFF FFFF FFFF 0100 0000",
            "0067 6156 54C1 CE11 8553 00AA 00A1 F95B",
            "0000 0000 0000 0000 0000 0000 801E 9213",
            "4BB4 BA01 0300 0000 4002 0000 0000 0000")

    store = ("5300 7400 6F00 7200 6100 6700 6500 2000",
             "3100 0000 0000 0000 0000 0000 0000 0000",
             "0000 0000 0000 0000 0000 0000 0000 0000",
             "0000 0000 0000 0000 0000 0000 0000 0000",
             "1400 0101 FFFF FFFF FFFF FFFF 0200 0000",
             "0061 6156 54C1 CE11 8553 00AA 00A1 F95B",
             "0000 0000 0088 F912 4BB4 BA01 801E 9213",
             "4BB4 BA01 0000 0000 0000 0000 0000 0000")

    file = ("5300 7400 7200 6500 6100 6D00 2000 3100",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "1200 0201 FFFF FFFF FFFF FFFF FFFF FFFF",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 0000 0000 0000 0000",
            "0000 0000 0000 0000 2002 0000 0000 0000")
    unused = b'\x00' * (16 * 4 + 4) + b'\xff' * 12 + b'\x00' * 16 * 3
    sector3 = (bytes.fromhex(" ".join(root))
               + bytes.fromhex(" ".join(store))
               + bytes.fromhex(" ".join(file))
               + unused)
    assert f.read(512) == sector3

    mini = ("0100 0000 0200 0000 0300 0000 0400 0000",
            "0500 0000 0600 0000 0700 0000 0800 0000",
            "FEFF FFFF")
    sector4 = (bytes.fromhex(" ".join(mini))
               + b'\xFF' * (16 * 29 + 12))
    assert f.read(512) == sector4

    string = "4461 7461 2066 6F72 2073 7472 6561 6D20 31"
    sector5 = (bytes.fromhex(string) * 30
               + b'\x44\x61')
    assert f.read(512) == sector5

    string = ("7461 2066 6F72 2073 7472 6561 6D20 31"
              + "4461 7461 2066 6F72 2073 7472 6561 6D20 31")
    sector6 = (bytes.fromhex(string)
               + b'\x00' * 480)
    assert f.read(512) == sector6
