import struct
from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from ms_dtyp.filetime import Filetime
from typing import TypeVar


T = TypeVar('T', bound='DirectoryFactory')


class DirectoryFactory:

    @classmethod
    def from_binary(cls: T, data: bytes) -> 'Directory':
        format = "<64shbb3I16sIQQIII"
        (name, name_size, type, color,
         previous_directory_id, next_directory_id,
         subdirectory_id, class_id,
         user_flags, created,
         modified, start_sector,
         file_size,
         zero) = struct.unpack(format, data)
        name = str(name, encoding='utf_16_le').rstrip('\x00')
        if (len(name) + 1) * 2 != name_size:
            raise Exception("Name / Size mismatch.")
        modified = Filetime.from_msfiletime(modified)
        created = Filetime.from_msfiletime(created)

        # Set Class_id (GUID)
        if type == 1:
            obj = StorageDirectory(name)
            if file_size != 0:
                raise Exception("File size must be zero.")
        elif type == 2:
            obj = StreamDirectory(name, '')
            obj.bytes_used = file_size
        elif type == 5:
            if name != "Root Entry":
                raise Exception('Root name is not correct.')
            obj = RootDirectory()
            obj.bytes_used = file_size
        obj.set_modified(modified)
        obj.set_created(created)
        obj.set_start_sector(start_sector)
        if color == 0:
            obj.set_color("red")
        else:
            obj.set_color("black")
        obj.prev_index = previous_directory_id
        obj.next_index = next_directory_id
        obj.sub_index = subdirectory_id
        obj.key = name
        return obj
