import os
from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase
from typing import TypeVar


T = TypeVar('T', bound='FatFilesystem')


class FatFilesystem(FilesystemBase):

    def __init__(self: T, size: int) -> None:
        super().__init__(size)
        self._next_free_sector = 1

    def get_chain(self: T) -> list:
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

    def _reserve_next_free_sector(self: T) -> int:
        if self._next_free_sector % 0x80 == 0:
            self._next_free_sector += 1
        sector = self._next_free_sector
        self._next_free_sector += 1
        return sector

    def count_fat_chain_sectors(self: T) -> int:
        """
        How many fat chain sectors are needed to express the chain?
        """
        return (self._next_free_sector - 1) // self._sector_size + 1

    def to_file(self: T, path: str) -> None:
        self.write_streams(path)
        self.write_chain("fat_chain.bin")
        f = open(path, "r+b")
        length = os.stat("fat_chain.bin").st_size
        c = open("fat_chain.bin", "ab")
        fill = self._sector_size - length % self._sector_size
        c.write(b'\xff' * fill)
        c.close()
        c = open("fat_chain.bin", "rb")
        f.write(c.read(self._sector_size))
        f.close()
        c.close()
        os.remove("fat_chain.bin")
