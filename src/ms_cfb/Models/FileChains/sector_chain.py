class SectorChain:

    def __init__(self):

        # The next available sector on the chain
        self._nextFreeSector = 0

    def __len__(self):
        return self._nextFreeSector

    def getChain(self):
        chain = []
        for stream in self._streams:
            sectors = stream.getSectors()
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
        sector = self._nextFreeSector
        self._nextFreeSector += 1
        return sector

    def extendChain(self, stream, number) -> None:
        """
        """
        sector_list = []
        for i in range(number):
            sector_list.append(self._reserveNextFreeSector())
        stream.setAdditionalSectors(sector_list)

    def requestNewSectors(self, stream):
        """
        the size of the stream has changed, based on the new size, are
        additional sectors needed?
        """
        size = stream.streamSize()
        have = len(stream.getSectors())
        if (have * self._sectorSize) < size:
            needed = (size - 1) // self._sectorSize + 1
            self.extendChain(stream, needed - have)
        pass

    def addStream(self, stream) -> None:
        sector = self._startNewChain()
        stream.setStartSector(sector)
        sectorsNeeded = max((stream.streamSize() - 1) // self._sectorSize, 0)
        if sectorsNeeded > 0:
            self.extendChain(stream, sectorsNeeded)
        self._streams.append(stream)

    def _startNewChain(self) -> int:
        # Increase the necessary chain resources by one address
        new_sector = self._reserveNextFreeSector()
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
        f.write(b'\x00' * sectors * self._sectorSize)
        for stream in self._streams:
            sectors = stream.getSectors()
            s = open(stream.file, "rb")
            for sector in sectors:
                sector_data = s.read(self._sectorSize)
                f.seek(sector * self._sectorSize)
                f.write(sector_data)
