import os
from ms_cfb.Models.Directories.directory import Directory


class StreamDirectory(Directory):

    def __init__(self, name, path):
        super(StreamDirectory, self).__init__()
        self._type = 2
        self.name = name
        # How many bytes does this item reserve in the file.
        # This includes padding to fill a sector or ministream.
        self.bytesUsed = 0
        self.file_path = path

    def set_created(self, datetime) -> None:
        raise Exception("File Directory must have created date of zero.")

    def set_modified(self, datetime) -> None:
        raise Exception("File Directory must have modified date of zero.")

    def set_clsid(self, uuid) -> None:
        raise Exception("clsid must be zero.")

    def set_bytes_reserved(self, quantity: int) -> None:
        self.bytesUsed = quantity

    def file_size(self) -> int:
        """
        Size in bytes of the file
        """
        return os.stat(self.file_path).st_size

    def minifat_sectors_used(self) -> int:
        return (self.file_size() - 1) // 64 + 1
