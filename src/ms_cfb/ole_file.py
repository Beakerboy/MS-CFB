import struct
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Filesystems.fat_filesystem import FatFilesystem
from ms_cfb.Models.Filesystems.minifat_filesystem import MinifatFilesystem
# from ms_cfb.Models.Entities.Streams.directoryStream import (
#     DirectoryStream
# )


class OleFile:

    # class default constructor
    def __init__(self):

        # Instance Attributes
        self._minor_version = 62
        self._major_version = 3
        self._sector_shift = 9
        self._mini_sector_shift = 6
        self.firstDirectoryListSector = 1

        # if there is no data small enough
        # to be on the minifat chain the root directory
        # and this value have to be set to something special.
        self._first_minichain_sector = 0
        self._mini_sector_cutoff = 4096

        # the FAT chain holds large files, the minifat chain, the minifat data,
        # and the directory tree.
        self._fatChain = FatFilesystem(2 ** self._sector_shift)

        # The list of pointers to the address of the next file piece
        self._minifatChain = MinifatFilesystem(2 ** self._mini_sector_shift)

        # A list of directories
        self._directory = RootDirectory()

    def set_version(self, version):
        if version > 4 or version < 3:
            raise Exception("Version must be 3 or 4")
        self._major_version = version
        if self._major_version == 3:
            self._sector_shift = 9
        else:
            self._sector_shift = 12

    def get_version(self):
        return self._major_version

    def add_directory_entry(self, object):
        """
        Add a storage or stream object to root
        """
        # verify type of object
        self._directory.add_stream(object)

    def header(self):
        """Create a 512 byte header sector for a OLE object."""
        packSymbol = '<' if self.project.endien == 'little' else '>'
        LONG_LONG_ZERO = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

        format = packSymbol + "8s16s6H10I"
        header = struct.pack(
            format,
            absig,
            LONG_LONG_ZERO + LONG_LONG_ZERO,  # clsid
            self._minor_version,
            self._major_version,
            65534,   # BOM
            self._sector_shift,
            self._mini_sector_shift,
            0,    # usReserved
            0,    # ulReserved1
            0,    # csectDir
            self._fatChain.count_fat_chain_sectors(),
            self.firstDirectoryListSector,
            0,    # signature
            self._mini_sector_cutoff,
            self._first_minichain_sector,
            max([len(self._minifatChain.getSectors()), 1]),
            self.getDifStartSector(),
            self.countDifSectors()
        )

        sectFat = self.writeHeaderFatSectorList()
        header += sectFat
        return header

    def getDifStartSector(self):
        """
        The Fat sector lost in the header can only list the position of 109
        sectors.If more sectors are needed, the DIF sector lists these sector
        numbers.
        """
        if len(self.getFatSectors()) <= 109:
            return 0xfffffffe
        # research how Dif works
        return 0

    def countDifSectors(self):
        """
        How many sectors of 512 entries are needed to list the positions of the
        remaining FAT sectors.
        What if sectors are not 512 bytes?
        """
        count = self._fatChain.count_fat_chain_sectors()
        if count <= 109:
            return 0
        return (count - 109 - 1) // (2 ** (self.uSectorShift - 2)) + 1

    def writeHeaderFatSectorList(self):
        """
        Create a 436 byte stream of the first 109 FAT sectors, padded with
        \\xFF.
        """
        packSymbol = '<' if self.project.endien == 'little' else '>'
        # if the list is longer then 109 entries, need to mange the extended
        # MSAT sectors.
        output = b''
        list = self.getFatSectors()
        for sector in list[0:109]:
            output += struct.pack(packSymbol + "I", sector)
        output = output.ljust(436, b'\xff')
        return output

    def getFatSectors(self):
        """
        List which sectors contain FAT chain information. They should be on
        128 sector intervals.
        """
        sectorList = []
        numberOfSectors = (len(self._fatChain) - 1) // 128 + 1
        for i in range(numberOfSectors):
            sectorList.append(i * (2 ** (self.uSectorShift - 2)))
        return sectorList

    def build_file(self):
        """
        Build the OLE file data structures from the project data.
        """

        directoryStream = self._directory.flatten()
        directoryStream.setStorageChain(self._fatChain)
        self._fatChain.addStream(directoryStream)

        self._minifatChain.setStorageChain(self._fatChain)
        self._fatChain.addStream(self._minifatChain)

        for stream in self.streams:
            directoryStream.append(stream)
            if stream.type == 2:
                if stream.fileSize() > self.ulMiniSectorCutoff:
                    self._fatChain.addStream(stream)
                else:
                    if self._first_minichain_sector == 0:
                        self._minifatChain.setStorageChain(self._fatChain)
                        self._fatChain.addStream(self._minifatChain)
                        self._first_minichain_sector = self._minifatChain.get_start_sector()
                    self._minifatChain.addStream(stream)

    def write_file(self, path):
        """
        Write the OLE file to disk
        """
        f = open(path + '/vbaProject.bin', 'wb+')
        f.write(self.header())
        # extend file to full size
        sectors = len(self._fatChain)
        f.write(b'\x00' * sectors * self._fatChain.getSectorSize())

        self._fatChain.write_chain("./fatChain.bin")
        # write directory sectors
        # write minifat chain
        # write minifat data

        # write minifat chain sectors
        f.close()

    def writeFile(self, path):
        """
        Build and Write the OLE file
        """
        self.build_file()
        self.write_file(path)
