import os
from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase
from ms_cfb.Models.DataStreams.file_array import FileArray
from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import TypeVar


T = TypeVar('T', bound='MinifatFilesystem')


class MinifatFilesystem(FilesystemBase, StreamBase):

    def __init__(self: T) -> None:
        FilesystemBase.__init__(self, 64)
        StreamBase.__init__(self)

    def get_first_stream_sector(self: T) -> int:
        return self._streams.get_start_sector()

    def add_stream(self: T, stream: 'StreamBase') -> None:
        """
        Add a new stream to the minifat chain and arrange the storage resources
        We need to manage changes to the minifat chain, minifat stream, and the
        FAT resources for them.
        """

        # If we have not started a minifat data stream in the FAT chain
        # start one now.
        if len(self._streams) == 0:
            self._streams = FileArray()
            self._storage_chain.add_stream(self._streams)
        FilesystemBase.add_stream(self, stream)
        self._storage_chain.request_new_sectors(self._streams)

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
        self.append(1)
        return new_sector

    def stream_size(self: T) -> int:
        """
        implementation of StreamBase.stream_size()
        """
        return 4 * len(self)

    def _extend_data(self: T, number: int) -> None:
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
        sector_size = self._storage_chain._sector_size
        fill = (sector_size - length % sector_size)
        if fill < sector_size:
            c = open(path, "ab")
            c.write(b'\xff' * fill)
            c.close()
