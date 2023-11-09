from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_dtyp.filetime import Filetime
from typing import TypeVar


T = TypeVar('T', bound='RootDirectory')


class RootDirectory(StorageDirectory):

    def __init__(self: T) -> None:
        super(RootDirectory, self).__init__("Root Entry")
        self._type = 5
        self._start_sector = 0xFFFFFFFE

    def set_created(self: T, created: Filetime) -> None:
        if not created == Filetime(1601, 1, 1)
            raise Exception("Root Directory must have created date of zero.")

    def file_size(self: T) -> int:
        """
        The number of bytes allocated in the minifat storage.
        """
        minifat_sector_size = 64
        size = 0
        for dir in self.directories:
            size += dir.minifat_sectors_used()
        return size * minifat_sector_size
