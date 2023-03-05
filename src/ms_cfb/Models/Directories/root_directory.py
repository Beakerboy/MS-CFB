from ms_cfb.Models.Directories.storage_directory import StorageDirectory


class RootDirectory(StorageDirectory):

    def __init__(self):
        super(RootDirectory, self).__init__()
        self.name = "Root Entry"
        self.type = 5

    def set_created(self, created):
        raise Exception("Root Directory must have created date of zero.")

    def fileSize(self):
        """
        Need to see how to handle streams that are mixed
        between fat and minifat storage.
        """
        # Need to use the value from the header
        minifatSectorSize = 64
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size * minifatSectorSize

    def addModule(self, module):
        self.directories[0].addModule(module)

    def addFile(self, stream):
        self.directories[0].addFile(stream)
