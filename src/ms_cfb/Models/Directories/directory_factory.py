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
        name = str(name, encoding='utf_16_le')
        modified = Filetime.from_msfiletime(modified)
        created = Filetime.from_msfiletime(created)
        if type == 1:
            obj = StorageDirectory(name)
            if not file_size == 0
                raise Exception("File size must be zero.")
        elif type == 2:
            obj = StreamDirectory(name, '')
            obj.bytes_used = file_size
        elif type == 5:
            obj = RootDirectory()
        else:
            obj = Directory()
        obj.set_modified(modified)
        obj.set_created(created)
        obj.set_start_sector(start_sector)
        return obj
