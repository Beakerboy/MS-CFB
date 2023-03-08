import os
from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase


class FatFilesystem(FilesystemBase):

    def __init__(self, size):
        super().__init__(size)
        self._nextFreeSector = 1

    def get_chain(self):
        """
        Need to add support for DIFAT
        """
        chain = super().get_chain()
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
        streams_length = os.stat(path).st_size
        self.write_chain("fat_chain.bin")
        f = open(path, "w+b")
        length = os.stat("fat_chain.bin").st_size
        if streams_length != 1024:
            raise Exception("file is the wrong size")
        c = open("fat_chain.bin", "ab")
        fill = self._sector_size - length % self._sector_size
        c.write(b'\xff' * fill)
        c.close()
        c = open("fat_chain.bin", "rb")
        f.write(c.read(512))
        f.close()
        c.close()
