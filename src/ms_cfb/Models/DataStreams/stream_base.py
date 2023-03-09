class StreamBase:
    """
    Base class for any object which will appear as a stream within a sector
    chain.
    """

    def __init__(self):

        # The stuff that will be used to squeeze data into the chain.
        # It can just be the data itself.
        self._data = b''

        # An array of sectors this stream will reside
        self._sectors = []

        # An object of type SectorChain which will be storing this stream
        self._storage_chain = 0

        # bytes to pad data to fill a sector
        self._padding = b'\x00'

    def set_padding(self, padding: bytes) -> None:
        self._padding = padding

    def set_storage_chain(self, chain) -> None:
        self._storage_chain = chain

    def set_start_sector(self, sector: int) -> None:
        """
        Set the location of the first sector of the file
        Must be run first
        """
        self._sectors = [sector]

    def get_start_sector(self):
        return self._sectors[0]

    def set_additional_sectors(self, sectors) -> None:
        self._sectors.extend(sectors)

    def get_sectors(self):
        return self._sectors

    def append(self, data) -> None:
        """
        Extend the data in this stream.
        Request additional chain storage if needed
        """
        self._extend_data(data)
        self._storage_chain.request_new_sectors(self)

    def stream_size(self) -> int:
        """
        The size the stream will be when rendered
        """
        return len(self._data)

    def to_bytes():
        """
        Return the object in bytes form
        """
        pass

    def _extend_data(self, data) -> None:
        """
        Add new data to the bytearray
        """
        self._data += data
