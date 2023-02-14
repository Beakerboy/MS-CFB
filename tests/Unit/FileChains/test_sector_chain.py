from ms_cfb.Models.FileChains.sector_chain import SectorChain


def test_next_free():
    chain = SectorChain()
    assert chain.reserve_next_free_sector() == 0
