import struct
import uuid
from ms_cfb.Models.DataStreams.directory_stream import DirectoryStream
from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.directory_factory import DirectoryFactory
from ms_cfb.Models.Filesystems.fat_filesystem import FatFilesystem
from ms_cfb.Models.Filesystems.minifat_filesystem import MinifatFilesystem
from typing import Type, TypeVar


T = TypeVar('T', bound='OleFile')


class OleFile:

    # class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        self._minor_version = 62
        self._major_version = 3
        self._sector_shift = 9
        self._mini_sector_shift = 6
        self._first_directory_list_sector = 1
        self._guid = uuid.UUID(int=0x00)
        # if there is no data small enough
        # to be on the minifat chain the root directory
        # and this value have to be set to something special.
        self._first_minichain_sector = 0xFFFFFFFE
        self._mini_sector_cutoff = 4096

        # the FAT chain holds large files, the minifat chain, the minifat data,
        # and the directory tree.
        self._fat_chain = FatFilesystem(2 ** self._sector_shift)

        # The list of pointers to the address of the next file piece
        self._minifat_chain = MinifatFilesystem()

        # A list of directories
        self._directory = RootDirectory()

    def __str__(self: T) -> str:
        version = self.get_version_string()
        output = ('Version ' + version + ' OLE file\n')
        output += ('GUID: ' + str(self.get_guid()) + '\n')
        output += 'File Structure:\n'
        for directory in self._directory.create_file_tree(0):
            output += '\t' * directory[0] + directory[1] + '\n'
        output += 'Directories:\n'
        for directory in self._directory.flatten():
            output += str(directory) + '\n'
        return output

    def set_version(self: T, version: int) -> None:
        if version > 4 or version < 3:
            raise Exception("Version must be 3 or 4")
        self._major_version = version
        if self._major_version == 3:
            self._sector_shift = 9
        else:
            self._sector_shift = 12
        self._fat_chain = FatFilesystem(2 ** self._sector_shift)

    def get_version(self: T) -> int:
        return self._major_version

    def get_version_string(self: T) -> str:
        return str(self._major_version) + '.' + str(self._minor_version)

    def get_guid(self: T) -> uuid.UUID:
        return self._guid

    def set_root_directory(self: T, dir: RootDirectory) -> None:
        self._directory = dir

    def add_directory_entry(self: T, object: 'Directory') -> None:
        """
        Add a storage or stream object to root
        """
        # verify type of object
        self._directory.add_directory(object)

    def header(self: T) -> bytes:
        """
        Create a 512 byte header sector for a OLE object.
        """

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

        format = "<8s16s6H10I"
        header = struct.pack(
            format,
            absig,
            self._guid.bytes_le,
            self._minor_version,
            self._major_version,
            65534,   # BOM
            self._sector_shift,
            self._mini_sector_shift,
            0,    # usReserved
            0,    # ulReserved1
            0,    # csectDir
            self._fat_chain.count_fat_chain_sectors(),
            self._first_directory_list_sector,
            0,    # signature
            self._mini_sector_cutoff,
            self._first_minichain_sector,
            max([len(self._minifat_chain.get_sectors()), 1]),
            self.get_dif_start_sector(),
            self.count_dif_sectors()
        )

        header += self.write_header_fat_sector_list()
        if self._major_version == 4:
            header += b'\x00' * 3584
        return header

    def get_dif_start_sector(self: T) -> int:
        """
        The Fat sector lost in the header can only list the position of 109
        sectors.If more sectors are needed, the DIF sector lists these sector
        numbers.
        """
        if len(self.get_fat_sectors()) <= 109:
            return 0xfffffffe
        # research how Dif works
        return 0

    def count_dif_sectors(self: T) -> int:
        """
        How many sectors of 512 entries are needed to list the positions of the
        remaining FAT sectors.
        What if sectors are not 512 bytes?
        """
        count = self._fat_chain.count_fat_chain_sectors()
        if count <= 109:
            return 0
        return (count - 109 - 1) // (2 ** (self._sector_shift - 2)) + 1

    def write_header_fat_sector_list(self: T) -> None:
        """
        Create a 436 byte stream of the first 109 FAT sectors, padded with
        \\xFF.
        """
        # if the list is longer then 109 entries, need to mange the extended
        # MSAT sectors.
        output = b''
        list = self.get_fat_sectors()
        for sector in list[0:109]:
            output += struct.pack("<I", sector)
        output = output.ljust(436, b'\xff')
        return output

    def get_fat_sectors(self: T) -> list:
        """
        List which sectors contain FAT chain information. They should be on
        128 sector intervals.
        """
        sector_list = []
        number_of_sectors = (len(self._fat_chain) - 1) // 128 + 1
        for i in range(number_of_sectors):
            sector_list.append(i * (2 ** (self._sector_shift - 2)))
        return sector_list

    def build_file(self: T) -> None:
        """
        Build the OLE file data structures from the project data.
        """

        directory_array = self._directory.flatten()
        directory_stream = DirectoryStream()
        fat_sec_size = self._fat_chain.get_sector_size()
        directory_stream.set_storage_sector_size(fat_sec_size)
        self._minifat_chain.set_storage_sector_size(fat_sec_size)
        self._fat_chain.add_stream(directory_stream)

        for stream in directory_array:
            directory_stream.append(stream)
            if stream.get_type() == 2:
                if stream.file_size() > self._mini_sector_cutoff:
                    stream.set_storage_sector_size(fat_sec_size)
                    self._fat_chain.add_stream(stream)
                else:
                    stream.set_storage_sector_size(64)
                    if self._first_minichain_sector == 0xFFFFFFFE:
                        # We have not previously added the minifat file sys
                        # to the fat so do that.
                        mf_chain = self._minifat_chain
                        self._fat_chain.add_stream(self._minifat_chain)
                        self._fat_chain.add_stream(mf_chain.get_streams())

                        # Update the project with the mini start sector
                        start_sector = mf_chain.get_start_sector()
                        self._first_minichain_sector = start_sector

                        # When we add the stream to the minichain, it will
                        # add the stream array to the fat chain.
                        self._minifat_chain.add_stream(stream)

                        # Now we can update the root directory with the sector
                        # of the start of the ministreams
                        stream_sector = mf_chain.get_first_stream_sector()
                        self._directory.set_start_sector(stream_sector)
                    else:
                        self._minifat_chain.add_stream(stream)
                    self._fat_chain.update_stream_sectors()

    def write_file(self: T, path: str) -> None:
        """
        Write the OLE file to disk
        """
        f = open(path, 'wb+')
        f.write(self.header())
        # extend file to full size
        sectors = len(self._fat_chain)
        f.write(b'\x01' * sectors * self._fat_chain.get_sector_size())

        self._fat_chain.to_file("./fatChain.bin")
        b = open("./fatChain.bin", "rb")
        f.seek(2 ** self._sector_shift)
        f.write(b.read())
        b.close()
        f.close()

    def create_file(self: T, path: str) -> None:
        """
        Build and Write the OLE file
        """
        self.build_file()
        self.write_file(path)

    def extract_all(self: T) -> None:
        """
        Extract all the StreamDirectory objects to files.
        """
        for directory in self._directory.flatten():
            if directory.get_type() == 2:
                self.extract_stream(directory.get_name())

    def extract_stream(self: T, name: str) -> None:
        """
        Extract the stream with the given name to a file.
        """
        found = False
        for directory in self._directory.flatten():
            if directory.get_name() == name:
                if directory.get_type() == 2:
                    found = True
                    fo = open(name + '.bin', 'wb')
                    fi = open(self.path, 'rb')
                    sectors = directory.get_sectors()
                    remaining = directory.file_size()
                    bytes_per_sector = 2 ** self._sector_shift
                    if remaining > 4096:
                        # Stream in fat
                        for sector in sectors:
                            offset = (sector + 1) * bytes_per_sector
                            fi.seek(offset)
                            buffer = min(bytes_per_sector, remaining)
                            fo.write(fi.read(buffer))
                            remaining -= buffer
                    else:
                        # Stream in minifat
                        for sector in sectors:
                            mf_sectors_per_sector = bytes_per_sector // 64
                            chain_index = sector // mf_sectors_per_sector
                            extra_bytes = (sector % mf_sectors_per_sector) * 64
                            fat_sectors = self._minifat_chain.get_sectors()
                            fatsector = fat_secrors[chain_index]
                            offset = (fat_sector + 1) * bytes_per_sector + extra_bytes
                            fi.seek(offset)
                            buffer = min(64, remaining)
                            fo.write(fi.read(buffer))
                            remaining -= buffer
                    fo.close()
                else:
                    raise Exception('Stream is not a file.')
        if not found:
            raise Exception('No stream found.')
    
    @classmethod
    def create_from_file(cls: Type[T], path: str) -> T:
        obj = cls()
        obj.path = path
        f = open(path, 'rb')
        header = f.read(76)

        # Read, validate, and set header values.
        format = "<8s16s6H10I"
        (
            absig, guid_le, minor_version, major_version,
            bom, sector_shift, mini_sector_shift, us_reserved,
            ul_reserved1, csect_dir, fat_chain_sectors,
            directory_list_sector, signature, mini_sector_cutoff,
            minichain_sector, minifat_sectors, dif_start_sector,
            dif_sectors
        ) = struct.unpack(format, header)
        if absig != b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            raise Exception('Incorrect signature.')
        obj._guid = uuid.UUID(bytes_le=guid_le)
        obj._minor_version = minor_version
        if major_version == 3 or major_version == 4:
            obj._major_version = major_version
        else:
            raise Exception('Version not supported.')
        if bom != 65534:
            raise Exception('Incorrect Byte Order Mark.')
        if (
            (major_version == 3 and sector_shift == 9) or
            (major_version == 4 and sector_shift == 12)
           ):
            obj._sector_shift = sector_shift
        else:
            raise Exception('Sector shift is not correct.')
        if mini_sector_shift != 6:
            raise Exception('Mini-sector shift is not correct.')
        if not (us_reserved == 0 and ul_reserved1 == 0):
            raise Exception('usReserved must be zero.')
        if csect_dir != 0:
            raise Exception('csectDir must be zero.')
        obj._first_directory_list_sector = directory_list_sector
        if signature != 0:
            raise Exception('Signature must be zero.')
        if mini_sector_cutoff != 4096:
            raise Exception('Mini-sector cuttoff is not correct.')
        obj._first_minichain_sector = minichain_sector
        # Eventually check validity of...
        # minifat_sectors, fat_chain_sectors, dif_start_sector
        # dif_sectors

        # Read FAT sector list.
        num_bytes = 3584 * (major_version - 3) + 436
        fat_sector_list_bytes = f.read(num_bytes)
        num = num_bytes // 4
        format = "<" + str(num) + "I"
        fat_sector_list = struct.unpack(format, fat_sector_list_bytes)

        # read fat sectors and assemble into sector list
        fat = []
        i = 0
        num = 2 ** (sector_shift - 2)
        format = "<" + str(num) + "I"
        sector = fat_sector_list[i]
        while sector != 0xFFFFFFFF:
            f.seek((sector + 1) * 2 ** sector_shift, 0)
            next_fat_bytes = f.read(2 ** sector_shift)
            next_fat = struct.unpack(format, next_fat_bytes)
            fat.extend(next_fat)
            i += 1
            sector = fat_sector_list[i]
        # Assemble directory.
        flat_directories = []
        j = 0
        while directory_list_sector != 0xFFFFFFFE:
            f.seek((directory_list_sector + 1) * 2 ** sector_shift)
            for i in range(2 ** (sector_shift - 7)):
                # Read the 128 byte directory entry.
                directory_bytes = f.read(128)
                if directory_bytes[0] != 0:
                    directory = DirectoryFactory.from_binary(directory_bytes)
                    directory.set_flattened_index(j)
                    j += 1
                    flat_directories.append(directory)
            directory_list_sector = fat[directory_list_sector]
        for directory in flat_directories:
            if directory.prev_index != 0xFFFFFFFF:
                left = flat_directories[directory.prev_index]
                directory.left = left
                left.parent = directory
            if directory.next_index != 0xFFFFFFFF:
                right = flat_directories[directory.next_index]
                directory.right = right
                right.parent = directory
            if directory.sub_index != 0xFFFFFFFF:
                child = flat_directories[directory.sub_index]
                directory.directories.root = child
        obj.set_root_directory(flat_directories[0])

        # extract minifat chain
        return obj
