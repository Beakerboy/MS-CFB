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
        self.left = Node()
        self.right = Node()
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

    def __str__(self: T) -> str:
        return (self.get_name() +
                "\n\tCreated: " + str(self._created) +
                "\n\tModified: " + str(self._modified) +
                "\n\tStart Sector: " + str(self._start_sector) +
                "\n\tSize: " + str(self.file_size()))

    def __lt__(self: T, other: T) -> bool:
        return ((len(self.name), self.name.upper())
                < (len(other.name), other.name.upper()))

    def __le__(self: T, other: T) -> bool:
        return ((len(self.name), self.name.upper())
                <= (len(other.name), other.name.upper()))

    def __gt__(self: T, other: T) -> bool:
        return ((len(self.name), self.name.upper())
                > (len(other.name), other.name.upper()))

    def __ge__(self: T, other: T) -> bool:
        return ((len(self.name), self.name.upper())
                >= (len(other.name), other.name.upper()))

    def __eq__(self: T, other: T) -> bool:
        if other.is_null():
            return False
        return ((len(self.name), self.name.upper())
                == (len(other.name), other.name.upper()))

    def __ne__(self: T, other: T) -> bool:
        if other.is_null():
            return True
        return ((len(self.name), self.name.upper())
                != (len(other.name), other.name.upper()))

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

    def get_name(self: T) -> str:
        return self.name

    def name_size(self: T) -> int:
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def set_additional_sectors(self: T, sector_list: list) -> None:
        self._additional_sectors = sector_list

    def file_size(self: T) -> int:
        return 0

    def to_bytes(self: T) -> bytes:
        format = "<64shbb3I16sIQQIII"
        color = 0 if self.is_red() else 1
        if self._type == 5 and len(self.directories) > 2:
            color = 0
        right = 0
        if self.right.is_null():
            right = 0xFFFFFFFF
        else:
            right = self.right._flattened_index
        dir = struct.pack(
            format,
            self.name.encode("utf_16_le"),
            self.name_size(),
            self._type,
            color,
            self._previous_directory_id,
            right,
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
