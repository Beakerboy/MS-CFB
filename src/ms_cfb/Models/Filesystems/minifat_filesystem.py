from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase
from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.DataStreams.stream_base import StreamBase


class MinifatFilesystem(FilesystemBase, StreamBase):

    def __init__(self, size):
        FilesystemBase.__init__(self, size)
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
            self._streams.setStorageChain(self._storageChain)
            self._storageChain.addStream(self._streams)
        FilesystemBase.addStream(self, stream)

    def extendChain(self, stream, number):
        """
        """
        sectorList = []
        for i in range(number):
            sectorList.append(self._reserveNextFreeSector())
        stream.setAdditionalSectors(sectorList)

    def _startNewChain(self):
        # Increase the necessary chain resources by one address
        newSector = self._reserveNextFreeSector()
        self.append(1)
        return newSector

    def streamSize(self):
        """
        implementation of StreamBase.streamSize()
        """
        return 4 * len(self)

    def _extendData(self, number):
        """
        implementation of StreamBase._extendData()
        """
        pass
