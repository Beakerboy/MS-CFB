import struct
import uuid
from ms_dtyp.filetime import Filetime
from red_black_dict_mod import RedBlackTree
from typing import TypeVar


T = TypeVar('T', bound='Directory')


class Directory(RedBlackTree):
    """An OLE directory object"""

    def __init__(self: T) -> None:
        # This object is a node in a red-black tree.
        RedBlackTree.__init__(self)

        # The directory to the left on the tree.
        self.left = RedBlackTree()

        # The directory to the right on the tree.
        self.right = RedBlackTree()

        # The object's name.
        self.name = ""

        # A GUID for this object.
        self._class_id = uuid.UUID(int=0x00)

        # todo:
        self._user_flags = 0

        # Creation and Modification dates.
        self._created = Filetime(1601, 1, 1)
        self._modified = Filetime(1601, 1, 1)

        # The sector where this stream begins
        # This can either be a minifat sector number or a Fat sector
        # depending on the stream size.
        self._start_sector = 0

        # The directory type.
        # probably can be removed.
        self._type = 0

        # This object's index in the flattened representation of the tree.
        self._flattened_index = 0

    def __str__(self: T) -> str:
        return (self.get_name() +
                "\n\tCreated: " + str(self._created) +
                "\n\tModified: " + str(self._modified) +
                "\n\tGUID: " + str(self._class_id) +
                "\n\tStart Sector: " + str(self.get_start_sector()) +
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
        return self.get_key() != other.get_key()

    def get_key(self: T) -> tuple[int, str]:
        return (len(self.name), self.name.upper())

    def set_color(self: T, value: str) -> None:
        is_blk = str == "black"
        self.is_black = is_blk

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

    def get_clsid(self: T) -> uuid.UUID:
        return self._class_id

    def get_name(self: T) -> str:
        return self.name

    def name_size(self: T) -> int:
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def set_additional_sectors(self: T, sector_list: list) -> None:
        self._additional_sectors = sector_list

    def file_size(self: T) -> int:
        return 0

    def set_flattened_index(self: T, index: int) -> None:
        self._flattened_index = index

    def get_subdirectory_index(self: T) -> int:
        """
        The the root node of the red-black tree which organizes the streams
        within a storage directory.
        """
        return 0xFFFFFFFF

    def to_bytes(self: T, color:int = 1, left:int = 0xFFFFFFFF, right:int = 0xFFFFFFFF) -> bytes:
        format = "<64shbb3I16sIQQIII"
        if self._type == 5 and len(self.directories) > 2:
            color = 0
        dir = struct.pack(
            format,
            self.name.encode("utf_16_le"),
            self.name_size(),
            self._type,
            color,
            left,
            right,
            self.get_subdirectory_index(),
            self._class_id.bytes_le,
            self._user_flags,
            self._created.to_msfiletime(),
            self._modified.to_msfiletime(),
            self.get_start_sector(),
            self.file_size(),
            0
        )
        return dir
