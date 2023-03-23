import struct
import uuid
from ms_dtyp.filetime import Filetime
from rbtree import Node
from typing import TypeVar


T = TypeVar('T', bound='Directory')


class Directory(Node):
    """An OLE directory object"""

    def __init__(self: T) -> None:
        Node.__init__(self)
        self.name = ""

        self._previous_directory_id = 0xFFFFFFFF
        self._next_directory_id = 0xFFFFFFFF
        self._subdirectory_id = 0xFFFFFFFF

        self._class_id = uuid.UUID(int=0x00)

        self._user_flags = 0

        self._created = Filetime(1601, 1, 1)
        self._modified = Filetime(1601, 1, 1)

        # The sector where this stream begins
        # This can either be a minifat sector number or a Fat sector
        # depending on the stream size.
        self._start_sector = 0
        self._type = 0

        self._flattened_index = 0

    def set_created(self: T, value: Filetime) -> None:
        self._created = value

    def get_created(self: T) -> Filetime:
        return self._created

    def set_modified(self: T, value: Filetime) -> None:
        self._modified = value

    def get_modified(self: T) -> Filetime:
        return self._modified

    def get_type(self: T) -> int:
        return self._type

    def set_start_sector(self: T, value: int) -> None:
        self._start_sector = value

    def get_start_sector(self: T) -> int:
        return self._start_sector

    def set_clsid(self: T, clsid: uuid.UUID) -> None:
        self._class_id = clsid

    def name_size(self: T) -> int:
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def set_additional_sectors(self: T, sector_list: list) -> None:
        self._additional_sectors = sector_list

    def file_size(self: T) -> int:
        return 0

    def to_bytes(self: T) -> bytes:
        format = "<64shbb3I16sIQQIII"

        dir = struct.pack(
            format,
            self.name.encode("utf_16_le"),
            self.name_size(),
            self._type,
            0 if self.is_red() else 1,
            self._previous_directory_id,
            self._next_directory_id,
            self._subdirectory_id,
            self._class_id.bytes_le,
            self._user_flags,
            self._created.to_msfiletime(),
            self._modified.to_msfiletime(),
            self.get_start_sector(),
            self.file_size(),
            0
        )
        return dir
