import struct
import uuid
from ms_dtyp.filetime import Filetime
from rbtree.rbtree import Node
from typing import TypeVar


T = TypeVar('T', bound='Directory')


class Directory(Node):
    """An OLE directory object"""

    def __init__(self: T) -> None:
        # This object is a node in a red-black tree.
        Node.__init__(self)

        # The directory to the left on the tree.
        self.left = Node()

        # The directory to the right on the tree.
        self.right = Node()

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

    @property
    def key(self: T) -> tuple:
        return (len(self.name), self.name.upper())

    @key.setter
    def key(self: T, value: None = None) -> None:
        pass

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
        left = 0
        if self.left.is_null():
            left = 0xFFFFFFFF
        else:
            left = self.left._flattened_index
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
