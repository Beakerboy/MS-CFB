from ms_cfb.Models.Filesystems.minifat_filesystem import MinifatFilesystem


def test_initial_properties() -> None:
    chain = MinifatFilesystem()
    assert chain.get_sector_size() == 64
    assert len(chain) == 0
