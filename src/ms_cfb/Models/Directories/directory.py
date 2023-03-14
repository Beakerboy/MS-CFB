import struct
import uuid


class Directory:
    """An OLE directory object"""

    def __init__(self):
        self.name = ""

        # red = 0, black = 1
        self.color = 1

        self._previous_directory_id = 0xFFFFFFFF
        self._next_directory_id = 0xFFFFFFFF
        self._subdirectory_id = 0xFFFFFFFF

        self._class_id = uuid.UUID(int=0x00)

        self.user_flags = 0

        self._created = 0
        self._modified = 0

        # The sector where this stream begins
        # This can either be a minifat sector number or a Fat sector
        # depending on the stream size.
        self._start_sector = 0
        self._type = 0

        self._flattened_index = 0

    def set_created(self, value: int) -> None:
        self._created = value

    def get_created(self) -> int:
        return self._created

    def set_modified(self, value: int) -> None:
        self._modified = value

    def get_modified(self) -> int:
        return self._modified

    def get_type(self) -> int:
        return self._type

    def set_start_sector(self, value: int) -> None:
        self._start_sector = value

    def get_start_sector(self) -> int:
        return self._start_sector

    def set_clsid(self, uuid) -> None:
        self._class_id = uuid

    def name_size(self) -> int:
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def set_additional_sectors(self, sector_list: list) -> None:
        self._additional_sectors = sector_list

    def file_size(self) -> int:
        return 0

    def to_bytes(self) -> bytes:
        format = "<64shbb3I16sIQQIII"

        dir = struct.pack(
            format,
            self.name.encode("utf_16_le"),
            self.name_size(),
            self._type,
            self.color,
            self._previous_directory_id,
            self._next_directory_id,
            self._subdirectory_id,
            self._class_id.bytes_le,
            self.user_flags,
            self._created,
            self._modified,
            self.get_start_sector(),
            self.file_size(),
            0
        )
        return dir
