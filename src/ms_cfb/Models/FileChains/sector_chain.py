class SectorChain:

    def __init__(self):

        # The next available sector on the chain
        self._next_free_sector = 0

    def __len__(self):
        return self._next_free_sector

    def get_chain(self):
        chain = []
        for stream in self._streams:
            sectors = stream.get_sectors()
            max = sectors[-1]
            if max >= len(chain):
                number = max - len(chain) + 1
                chain.extend([0] * number)
            for i in range(len(sectors)):
                sectornum = sectors[i]
                if sectors[i] == max:
                    chain[sectornum] = 0xFFFFFFFE
                else:
                    chain[sectornum] = sectors[i + 1]

        return chain

    def reserve_next_free_sector(self) -> int:
        sector = self._next_free_sector
        self._next_free_sector += 1
        return sector

    def extend_chain(self, stream, number) -> None:
        """
        """
        sector_list = []
        for i in range(number):
            sector_list.append(self._reserve_next_free_sector())
        stream.set_additional_sectors(sector_list)

    def request_new_sectors(self, stream):
        """
        the size of the stream has changed, based on the new size, are
        additional sectors needed?
        """
        size = stream.stream_size()
        have = len(stream.get_sectors())
        if (have * self._sectorSize) < size:
            needed = (size - 1) // self._sectorSize + 1
            self.extend_chain(stream, needed - have)
        pass

    def add_stream(self, stream) -> None:
        sector = self._start_new_chain()
        stream.set_start_sector(sector)
        sectors_needed = max((stream.stream_size() - 1) // self._sectorSize, 0)
        if sectors_needed > 0:
            self.extend_chain(stream, sectors_needed)
        self._streams.append(stream)

    def _start_new_chain(self) -> int:
        # Increase the necessary chain resources by one address
        new_sector = self._reserve_next_free_sector()
        return new_sector

    def write_chain(self, path: str, endian="little") -> None:
        """
        write the chain list to a file.
        """
        chain = self.getChain()
        f = open(path, "wb")
        # Each address is 4 bytes
        for address in chain:
            f.write(address.to_bytes(4, endian))

    def write_streams(self, path: str, endian="little") -> None:
        sectors = len(self)
        f = open(path, "wb")
        f.write(b'\x00' * sectors * self._sector_size)
        for stream in self._streams:
            sectors = stream.get_sectors()
            s = open(stream.file, "rb")
            for sector in sectors:
                sector_data = s.read(self._sector_size)
                f.seek(sector * self._sector_size)
                f.write(sector_data)
