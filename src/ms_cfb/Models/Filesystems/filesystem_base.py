class FilesystemBase:

    def __init__(self, size):
        # The number of bytes in each sector
        self._sector_size = size

        # The next available sector on the chain
        self._nextFreeSector = 0

        # Each stream begins at the start of a sector and is padded to fill
        # the end of a sector.
        self._streams = []

    def __len__(self):
        return self._nextFreeSector

    def getSectorSize(self):
        """
        Get the number of bytes in each sector
        """
        return self._sector_size

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

    def _reserveNextFreeSector(self):
        sector = self._nextFreeSector
        self._nextFreeSector += 1
        return sector

    def extendChain(self, stream, number):
        """
        """
        sectorList = []
        for i in range(number):
            sectorList.append(self._reserveNextFreeSector())
        stream.setAdditionalSectors(sectorList)

    def requestNewSectors(self, stream):
        """
        the size of the stream has changed, based on the new size, are
        additional sectors needed?
        """
        size = stream.streamSize()
        have = len(stream.getSectors())
        if (have * self._sector_size) < size:
            needed = (size - 1) // self._sector_size + 1
            self.extendChain(stream, needed - have)
        pass

    def add_stream(self, stream):
        sector = self._startNewChain()
        stream.set_start_sector(sector)
        sectorsNeeded = max((stream.streamSize() - 1) // self._sector_size, 0)
        if sectorsNeeded > 0:
            self.extendChain(stream, sectorsNeeded)
        self._streams.append(stream)

    def _startNewChain(self):
        # Increase the necessary chain resources by one address
        newSector = self._reserveNextFreeSector()
        return newSector

    def write_chain(self, path):
        """
        write the chain list to a file.
        """
        chain = self.getChain()
        f = open(path, "wb")
        # Each address is 4 bytes
        for address in chain:
            f.write(address.to_bytes(4, "little"))

    def write_streams(self, path):
        sectors = len(self)
        f = open(path, "wb")
        f.write(b'\x00' * sectors * self._sector_size)
        for stream in self._streams:
            sectors = stream.getSectors()
            s = open(stream.file, "rb")
            for sector in sectors:
                sector_data = s.read(self._sector_size)
                f.seek(sector * self._sector_size)
                f.write(sector_data)
