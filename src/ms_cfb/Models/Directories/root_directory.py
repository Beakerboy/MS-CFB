from ms_cfb.Models.Directories.storage_directory import StorageDirectory


class RootDirectory(StorageDirectory):

    def __init__(self):
        super(RootDirectory, self).__init__("Root Entry")
        self._type = 5

    def set_created(self, created) -> None:
        raise Exception("Root Directory must have created date of zero.")

    def file_size(self) -> int:
        """
        The number of bytes allocated in the minifat storage.
        """
        # Need to use the value from the header
        minifat_sector_size = 64
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size * minifat_sector_size

    def addModule(self, module) -> None:
        self.directories[0].addModule(module)

    def addFile(self, stream) -> None:
        self.directories[0].addFile(stream)
