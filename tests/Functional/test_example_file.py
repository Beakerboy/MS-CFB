import os
import pytest
import uuid
from ms_cfb.ole_file import OleFile
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory


@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:

    # A test function will be run at this point
    yield
    # Code that will run after your test
    names = ["vbaProject.bin"]
    map(os.remove, names)


def test_example_file():
    """
    The example file as described in MS-CFB
    """

    root = RootDirectory()
    guid = uuid.UUID("11CEC15456616700AA0053855BF9A100")
    root.set_clsid(guid)
    root.set_modified(0x01BAB44B13921E80)

    storage = StorageDirectory("Storage 1")
    # 11/16/1995 5:43:44 PM
    storage.set_created(0x01BAB44B12F98800)
    # 11/16/1995 5:43:45 PM
    storage.set_modified(0x01BAB44B13921E80)
    guid2 = uuid.UUID("56616100-C154-11CE-5385-5BF9A100AA00")
    storage.set_clsid(guid2)

    stream1_data = bytes("Data for stream 1", "utf8") * 32
    f = open("stream1.bin", "wb")
    f.write(stream1_data)
    f.close()
    stream1 = StreamDirectory("Stream 1", "stream1.bin")
    storage.add_directory(stream1)

    ole_file = OleFile()
    ole_file.set_root_directory(root)
    ole_file.add_directory_entry(storage)
    ole_file.create_file(".")
    assert os.stat("vbaProject.bin").st_size == 512 * 5

    f = open("vbaProject.bin", "rb")
    sector1 = ("D0CF 11E0 A1B1 1AE1 0000 0000 0000 0000",
               "0000 0000 0000 0000 3E00 0300 FEFF 0900",
               "0600 0000 0000 0000 0000 0000 0100 0000",
               "0100 0000 0000 0000 0010 0000 0200 0000",
               "0100 0000 FEFF FFFF 0000 0000 0000 0000")
    expected = bytes.fromhex(" ".join(sector1)) + b'\xff' * 16 * 27
    assert f.read(512) == expected
