from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase


class FatFilesystem(FilesystemBase):

    def __init__(self, size):
        super().__init__(size)
        self._nextFreeSector = 1

    def getChain(self):
        """
        Need to add support for DIFAT
        """
        chain = super().getChain()
        if len(chain) == 0:
            chain = [0xFFFFFFFD]
        else:
            addresses_per_sector = self._sector_size // 4
            num = (len(self) - 1) // addresses_per_sector + 1
            for i in range(num):
                chain[i * 0x80] = 0xFFFFFFFD
        return chain

    def _reserveNextFreeSector(self) -> int:
        if self._nextFreeSector % 0x80 == 0:
            self._nextFreeSector += 1
        sector = self._nextFreeSector
        self._nextFreeSector += 1
        return sector

    def count_fat_chain_sectors(self) -> int:
        """
        How many fat chain sectors are needed to express the chain?
        """
        return (self._nextFreeSector - 1) // self._sector_size + 1

    def to_file(self, path):
        self.write_streams(path)
        self.write_chain("fat_chain.bin")
        f = open(path, "wb")
        c = open("fat_chain.bin", "rb")
        f.write(c.read(512))
        f.close()
        c.close()
