from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_dtyp.filetime import Filetime
from typing import Literal, TypeVar


T = TypeVar('T', bound='RootDirectory')


class RootDirectory(StorageDirectory):

    def __init__(self: T) -> None:
        super(RootDirectory, self).__init__("Root Entry")
        self._type = 5
        self._start_sector = 0xFFFFFFFE
        # The value from the factory method.
        self.bytes_used = 0

    def __str__(self: T) -> str:
        return (self.get_name() +
                "\n\tModified: " + str(self._modified) +
                "\n\tGUID: " + str(self._class_id) +
                "\n\tStart Sector: " + str(self.get_start_sector()) +
                "\n\tSize: " + str(self.file_size()))

    @property
    def color(self: T) -> Literal['red', 'black']:
        color: Literal["red", "black"] = "black"
        if (len(self.directories) > 2 and
                self.left.is_black() and
                self.right.is_black()):
            color = "red"
        return color

    @color.setter
    def color(self: T, new_color: Literal['red', 'black']) -> None:
        super(RootDirectory, self).color = new_color

    def set_created(self: T, created: Filetime) -> None:
        if not created.to_msfiletime() == 0:
            raise Exception("Root Directory must have created date of zero.")

    def file_size(self: T) -> int:
        """
        The number of bytes allocated in the minifat storage.
        """
        if len(self.directories) == 0 and self.bytes_used > 0:
            return self.bytes_used
        minifat_sector_size = 64
        size = 0
        for dir in self.directories:
            size += dir.minifat_sectors_used()
        return size * minifat_sector_size
