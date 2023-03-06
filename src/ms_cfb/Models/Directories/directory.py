import struct
import uuid


class Directory:
    """An OLE directory object"""

    def __init__(self):
        self.name = ""

        # red = 0, black = 1
        self.color = 1

        self.previousDirectoryId = 0xFFFFFFFF
        self.nextDirectoryId = 0xFFFFFFFF
        self.subDirectoryId = 0xFFFFFFFF

        self._class_id = uuid.UUID(int=0x00)

        self.userFlags = 0

        self._created = 0
        self._modified = 0

        # The sector where this stream begins
        # This can either be a minifat sector number or a Fat sector
        # depending on the stream size.
        self._startSector = 0
        self._type = 0

    def set_created(self, value):
        self._created = value

    def get_created(self):
        return self._created

    def set_modified(self, value):
        self._modified = value

    def get_modified(self):
        return self._modified

    def get_type(self) -> int:
        return self._type

    def setStartSector(self, value):
        self._startSector = value

    def getStartSector(self):
        return self._startSector

    def nameSize(self):
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def setAdditionalSectors(self, sectorList):
        self._additionalSectors = sectorList

    def file_size(self):
        return 0

    def to_bytes(self, codePageName):
        format = "<64shbb3I"

        dir = struct.pack(
            format,
            self.name.encode("utf_16_le"),
            self.nameSize(),
            self._type,
            self.color,
            self.previousDirectoryId,
            self.nextDirectoryId,
            self.subDirectoryId
        )
        dir += self._class_id.bytes_le
        dir += struct.pack(
            "<IQQIII",
            self.userFlags,
            self._created,
            self._modified,
            self._startSector,
            self.file_size(),
            0
        )
        return dir
