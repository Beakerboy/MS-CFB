import struct
from ms_cfb.Models.Directories.root_directory import RootDirectory


class DirectoryFactory:

    @classmethod
    def from_bin(cls, data):
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
            raise Exception(modified.isoformat())
