from typing import TypeVar
from ms_cfb.Models.Filesystems.filesystem_base import FilesystemBase


T = TypeVar('T', bound='StreamBase')


class StreamBase:
    """
    Base class for any object which will appear as a stream within a sector
    chain.
    """

    def __init__(self: T) -> None:

        # The stuff that will be used to squeeze data into the chain.
        # It can just be the data itself.
        self._data = b''

        # An array of sectors this stream will reside
        self._sectors = []

        # An object of type SectorChain which will be storing this stream
        self._storage_chain = 0

        # bytes to pad data to fill a sector
        self._padding = b'\x00'

    def set_padding(self: T, padding: bytes) -> None:
        self._padding = padding

    def set_storage_chain(self: T, chain: FilesystemBase) -> None:
        self._storage_chain = chain

    def set_start_sector(self: T, sector: int) -> None:
        """
        Set the location of the first sector of the file
        Must be run first
        """
        self._sectors = [sector]

    def get_start_sector(self: T) -> int:
        return self._sectors[0]

    def set_additional_sectors(self: T, sectors: list) -> None:
        self._sectors.extend(sectors)

    def get_sectors(self: T) -> list:
        return self._sectors

    def append(self: T, data: bytes) -> None:
        """
        Extend the data in this stream.
        Request additional chain storage if needed
        """
        self._extend_data(data)
        self._storage_chain.request_new_sectors(self)

    def stream_size(self: T) -> int:
        """
        The size the stream will be when rendered
        """
        return len(self._data)

    def _extend_data(self: T, data: bytes) -> None:
        """
        Add new data to the bytearray
        """
        self._data += data
