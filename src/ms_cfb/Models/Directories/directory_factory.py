import struct
from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_dtyp.filetime import Filetime
from typing import TypeVar


T = TypeVar('T', bound='DirectoryFactory')


class DirectoryFactory:

    @classmethod
    def from_binary(cls: T, data: bytes) -> 'Directory':
        obj = cls()
        format = "<64shbb3I16sIQQIII"
        (name,
         name_size,
         type,
         color,
         previous_directory_id,
         next_directory_id,
         subdirectory_id,
         class_id,
         user_flags,
         created,
         modified,
         start_sector,
         file_size,
         zero) = struct.unpack(format, data)
        if type == 5:
            obj = RootDirectory()
            modified = Filetime.from_msfiletime(modified)
        return obj
