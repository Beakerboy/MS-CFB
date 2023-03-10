import os
from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase
from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.DataStreams.stream_base import StreamBase


class MinifatFilesystem(FilesystemBase, StreamBase):

    def __init__(self):
        FilesystemBase.__init__(self, 64)
        StreamBase.__init__(self)

    def add_stream(self, stream):
        """
        Add a new stream to the minifat chain and arrange the storage resources
        We need to manage changes to the minifat chain, minifat stream, and the
        FAT resources for them.
        """

        # If we have not started a minifat data stream in the FAT chain
        # start one now.
        if len(self._streams) == 0:
            self._streams = ArrayStream()
            self._streams.set_storage_chain(self._storage_chain)
            self._storage_chain.add_stream(self._streams)
        FilesystemBase.add_stream(self, stream)
        stream.set_storage_chain(self)

    def extend_chain(self, stream, number):
        """
        """
        sector_list = []
        for i in range(number):
            sector_list.append(self._reserve_next_free_sector())
        stream.set_additional_sectors(sector_list)

    def _start_new_chain(self):
        # Increase the necessary chain resources by one address
        new_sector = self._reserve_next_free_sector()
        self.append(1)
        return new_sector

    def stream_size(self):
        """
        implementation of StreamBase.stream_size()
        """
        return 4 * len(self)

    def _extend_data(self, number):
        """
        implementation of StreamBase._extend_data()
        """
        pass

    def to_file(self, path):
        filename = "minifat_chain.bin"
        self.write_streams(path)
        self.write_chain(filename)
        f = open(path, "r+b")
        length = os.stat(filename).st_size
        c = open(filename, "ab")
        fill = self._sector_size - length % self._sector_size
        c.write(b'\xff' * fill)
        c.close()
        c = open(filename, "rb")
        f.write(c.read(512))
        f.close()
        c.close()
