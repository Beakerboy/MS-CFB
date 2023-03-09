import os
import uuid
from ms_cfb.ole_file import OleFile


def test_example_file():
    """
    The example file as described in MS-CFB
    """

    root = RootDirectory()
    root.set_clsid(0x11CEC15456616700 0xAA005385 0x5BF9A100)
    root.set_modified(0x01BAB44B13921E80)

    storage = StorageDirectory("Storage 1")
    # 11/16/1995 5:43:44 PM
    storage.set_created(0x01BAB44B12F98800)
    # 11/16/1995 5:43:45 PM
    storage.set_modified(0x01BAB44B13921E80)
    storage.set_clsid(0x5BF9A100AA00538511CEC15456616100)

    stream1_data = "Data for stream 1" * 32
    f = open("stream1.bin" "wb")
    f.write(stream1_data)
    f.close()
    stream1 = StreamDirectory("Stream 1", "stream1.bin")
    storage.add_stream(stream1)

    ole_file = OleFile()
    ole_file.set_root_directory(root)
    ole_file.add_directory_entry(storage)
    ole_file.create_file(".")
