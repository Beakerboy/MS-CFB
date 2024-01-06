from typing import Any, TypeVar


T = TypeVar('T', bound='StreamBase')


class StreamBase:
    """
    Base class for any object which will appear as a stream within a sector
    chain.
    """

    def __init__(self: T) -> None:

        # The stuff that will be used to squeeze data into the chain.
        # It can just be the data itself.
        self._data: Any = b''

        # An array of sectors this stream will reside
        self._sectors: list = []

        # bytes to pad data to fill a sector
        self._padding = b'\x00'

        # the size in bytes of a sector in the storage chain
        self._storage_sector_size = 64

    def set_start_sector(self: T, sector: int) -> None:
        """
        Set the location of the first sector of the file
        Must be run first
        """
        self._sectors = [sector]

    def get_start_sector(self: T) -> int:
        """
        Get the sector in which the first block of this stream resides.
        """
        return self._sectors[0]

    def set_storage_sector_size(self: T, size: int) -> None:
        """
        The size in bytes of each sector that will hold this
        object
        """
        self._storage_sector_size = size

    def set_additional_sectors(self: T, sectors: list) -> None:
        self._sectors.extend(sectors)

    def get_sectors(self: T) -> list:
        return self._sectors

    def append(self: T, data: Any) -> None:
        """
        Extend the data in this stream.
        Request additional chain storage if needed
        """
        self._extend_data(data)

    def stream_size(self: T) -> int:
        """
        The size the stream will be when rendered
        """
        return len(self._data)

    def _extend_data(self: T, data: bytes) -> None:
        """
        Add new data to the stream.
        In this basic implementation, the byte array is lengthed.
        """
        self._data += data
