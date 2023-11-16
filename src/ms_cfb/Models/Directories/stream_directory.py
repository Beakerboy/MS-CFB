import os
import uuid
from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.DataStreams.file_stream import FileStream
from ms_dtyp.filetime import Filetime
from typing import TypeVar


T = TypeVar('T', bound='StreamDirectory')


class StreamDirectory(FileStream, Directory):

    def __init__(self: T, name: str, path: str) -> None:
        Directory.__init__(self)
        FileStream.__init__(self, path)
        self._type = 2
        self.name = name
        # How many bytes does this item reserve in the file.
        # This includes padding to fill a sector or ministream.
        self.bytesUsed = 0
        self._file_path = path

    def __str__(self: T) -> str:
        return (self.get_name() +
                "\n\tStart Sector: " + str(self.get_start_sector()) +
                "\n\tSize: " + str(self.file_size()))

    def set_created(self: T, created: Filetime) -> None:
        if not created.to_msfiletime() == 0:
            raise Exception("File Directory must have created date of zero.")

    def set_modified(self: T, modified: Filetime) -> None:
        if not modified.to_msfiletime() == 0:
            raise Exception("File Directory must have modified date of zero.")

    def set_clsid(self: T, clsid: uuid.UUID) -> None:
        if clsid.int != 0x00:
            raise Exception("clsid must be zero.")

    def set_bytes_reserved(self: T, quantity: int) -> None:
        self.bytesUsed = quantity

    def set_start_sector(self: T, sector: int) -> None:
        """
        Copied feom StreamBase since Directory has a
        function with the same name.
        Set the location of the first sector of the file
        Must be run first
        """
        self._sectors = [sector]

    def get_start_sector(self: T) -> int:
        return self._sectors[0]

    def stream_size(self: T) -> int:
        """
        implements StreamBase.stream_size()
        """
        return self.file_size()

    def file_size(self: T) -> int:
        """
        Size in bytes of the file
        """
        if self._file_path == "":
            return self.bytes_used
        return os.stat(self._file_path).st_size

    def minifat_sectors_used(self: T) -> int:
        """
        Implements Directory.minifat_sectors_used()
        How many minifat sectors does this stream use?
        """
        if self.file_size() >= 4096:
            return 0
        return (self.file_size() - 1) // 64 + 1
