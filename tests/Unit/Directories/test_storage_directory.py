from ms_cfb.Models.Directories.storage_directory import StorageDirectory


def test_constructor():
    dir = StorageDirectory("name")
    assert dir.get_type() == 1
    assert isinstance(dir, StorageDirectory)
