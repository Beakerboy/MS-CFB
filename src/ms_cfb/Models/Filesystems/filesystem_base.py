import os
import string
from random import choice


class FilesystemBase:

    def __init__(self, size) -> None:
        # The number of bytes in each sector
        self._sector_size = size

        # The next available sector on the chain
        self._next_free_sector = 0

        # Each stream begins at the start of a sector and is padded to fill
        # the end of a sector.
        self._streams = []

    def __len__(self) -> int:
        return self._next_free_sector

    def get_sector_size(self) -> int:
        """
        Get the number of bytes in each sector
        """
        return self._sector_size

    def get_chain(self) -> list:
        """
        Express the sector chain as a list of ints
        """
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

    def _reserve_next_free_sector(self) -> int:
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

    def request_new_sectors(self, stream) -> None:
        """
        the size of the stream has changed, based on the new size, are
        additional sectors needed?
        """
        size = stream.stream_size()
        have = len(stream.get_sectors())
        if (have * self._sector_size) < size:
            needed = (size - 1) // self._sector_size + 1
            self.extend_chain(stream, needed - have)

    def add_stream(self, stream) -> None:
        sector = self._start_new_chain()
        stream.set_start_sector(sector)
        stream.set_storage_chain(self)
        sectors_needed = (stream.stream_size() - 1) // self._sector_size
        sectors_needed = max(sectors_needed, 0)
        if sectors_needed > 0:
            self.extend_chain(stream, sectors_needed)
        self._streams.append(stream)

    def _start_new_chain(self) -> int:
        # Increase the necessary chain resources by one address
        new_sector = self._reserve_next_free_sector()
        return new_sector

    def write_chain(self, path) -> None:
        """
        write the chain list to a file.
        """
        chain = self.get_chain()
        f = open(path, "wb")
        # Each address is 4 bytes
        for address in chain:
            f.write(address.to_bytes(4, "little"))

    def write_streams(self, path) -> None:
        sectors = len(self)
        f = open(path, "wb")
        f.write(b'\x02' * sectors * self._sector_size)
        i = 0
        for stream in self._streams:
            sectors = stream.get_sectors()
            rand = ''.join([choice(string.ascii_letters) for i in range(5)])
            filename = "stream" + str(i) + rand + ".bin"
            stream.to_file(filename)
            s = open(filename, "rb")
            for sector in sectors:
                sector_data = s.read(self._sector_size)
                f.seek(sector * self._sector_size)
                f.write(sector_data)
            s.close()
            os.remove(filename)
            i += 1
