import os
from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase
from ms_cfb.Models.DataStreams.file_array import FileArray
from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import TypeVar


T = TypeVar('T', bound='MinifatFilesystem')


class MinifatFilesystem(FilesystemBase, StreamBase):

    def __init__(self: T) -> None:
        minifat_sector_size = 64
        FilesystemBase.__init__(self, minifat_sector_size)
        StreamBase.__init__(self)
        self._streams: FileArray = FileArray(minifat_sector_size)

    def set_storage_sector_size(self: T, size: int) -> None:
        """
        From StreamBase
        """
        self._storage_sector_size = size
        self._streams.set_storage_sector_size(size)

    def get_streams(self: T) -> FileArray:
        return self._streams

    def get_first_stream_sector(self: T) -> int:
        return self._streams.get_start_sector()

    def extend_chain(self: T, stream: 'StreamBase', number: int) -> None:
        """
        """
        sector_list = []
        for i in range(number):
            sector_list.append(self._reserve_next_free_sector())
        stream.set_additional_sectors(sector_list)

    def _start_new_chain(self: T) -> int:
        # Increase the necessary chain resources by one address
        new_sector = self._reserve_next_free_sector()
        return new_sector

    def stream_size(self: T) -> int:
        """
        implementation of StreamBase.stream_size()
        """
        return 4 * len(self)

    def _extend_data(self: T, number: bytes) -> None:
        """
        implementation of StreamBase._extend_data()
        """
        pass

    def to_file(self: T, path: str) -> None:
        """
        Write the chain data to a file.
        The stream data is written by calling
        MinifatFilesytem._streams.to_file()
        """
        self.write_chain(path)
        length = os.stat(path).st_size
        fill = (self._storage_sector_size - length % self._storage_sector_size)
        if fill < self._storage_sector_size:
            c = open(path, "ab")
            c.write(b'\xff' * fill)
            c.close()
