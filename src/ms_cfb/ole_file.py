import argparse
import os
import struct
import uuid
from ms_cfb.Models.DataStreams.directory_stream import DirectoryStream
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from ms_cfb.Models.Filesystems.fat_filesystem import FatFilesystem
from ms_cfb.Models.Filesystems.minifat_filesystem import MinifatFilesystem


class OleFile:

    # class default constructor
    def __init__(self):

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

    def set_version(self, version: int) -> None:
        if version > 4 or version < 3:
            raise Exception("Version must be 3 or 4")
        self._major_version = version
        if self._major_version == 3:
            self._sector_shift = 9
        else:
            self._sector_shift = 12
        self._fat_chain = FatFilesystem(2 ** self._sector_shift)

    def get_version(self) -> int:
        return self._major_version

    def set_root_directory(self, dir) -> None:
        self._directory = dir

    def add_directory_entry(self, object) -> None:
        """
        Add a storage or stream object to root
        """
        # verify type of object
        self._directory.add_directory(object)

    def header(self) -> bytes:
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

    def get_dif_start_sector(self) -> int:
        """
        The Fat sector lost in the header can only list the position of 109
        sectors.If more sectors are needed, the DIF sector lists these sector
        numbers.
        """
        if len(self.get_fat_sectors()) <= 109:
            return 0xfffffffe
        # research how Dif works
        return 0

    def count_dif_sectors(self) -> int:
        """
        How many sectors of 512 entries are needed to list the positions of the
        remaining FAT sectors.
        What if sectors are not 512 bytes?
        """
        count = self._fat_chain.count_fat_chain_sectors()
        if count <= 109:
            return 0
        return (count - 109 - 1) // (2 ** (self._sector_shift - 2)) + 1

    def write_header_fat_sector_list(self):
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

    def get_fat_sectors(self) -> list:
        """
        List which sectors contain FAT chain information. They should be on
        128 sector intervals.
        """
        sector_list = []
        number_of_sectors = (len(self._fat_chain) - 1) // 128 + 1
        for i in range(number_of_sectors):
            sector_list.append(i * (2 ** (self._sector_shift - 2)))
        return sector_list

    def build_file(self) -> None:
        """
        Build the OLE file data structures from the project data.
        """

        directory_array = self._directory.flatten()
        self._directory.set_child()
        directory_stream = DirectoryStream()

        self._fat_chain.add_stream(directory_stream)

        for stream in directory_array:
            directory_stream.append(stream)
            if stream.get_type() == 2:
                if stream.file_size() > self._mini_sector_cutoff:
                    self._fat_chain.add_stream(stream)
                else:
                    if self._first_minichain_sector == 0xFFFFFFFE:
                        # We have not previously added the minifat file sys
                        # to the fat so do that.
                        mf_chain = self._minifat_chain
                        self._fat_chain.add_stream(self._minifat_chain)

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

    def write_file(self, path: str) -> None:
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

    def create_file(self, path: str) -> None:
        """
        Build and Write the OLE file
        """
        self.build_file()
        self.write_file(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The directory that contains your files.")
    parser.add_argument("-v", "--version", type=int, choices=[3, 4],
                        help="The OLE version to use.")
    parser.add_argument("-o", "--output",
                        help="The output file name.")
    parser.add_argument("-x", "--extra",
                        help="Path to exta directory settings yml file.")
    args = parser.parse_args()
    ole_file = OleFile()
    if args.version == 4:
        ole_file.set_version(4)
    root = RootDirectory()
    obj = os.scandir(args.directory)
    for entry in obj:
        if entry.is_dir():
            root.add_directory(create_storage(entry))
        else:
            dir = StreamDirectory(entry.name, entry.path)
            root.add_directory(dir)
    mod_time = os.stat(args.directory).st_mtime
    root.set_modified(int(mod_time))
    ole_file.set_root_directory(root)
    ole_file.create_file(args.output)


def create_storage(direntry):
    dir = StorageDirectory(direntry.name)
    obj = os.scandir(direntry.path)
    for entry in obj:
        if entry.is_dir():
            dir.add_directory(create_storage(entry))
        else:
            stream = StreamDirectory(entry.name, entry.path)
            dir.add_directory(stream)
    mod_time = Filetime.fromtimestamp(os.stat(direntry.path).st_mtime)
    dir.set_modified(mod_time.tomsfiletime())
    return dir


if __name__ == '__main__':
    main()
