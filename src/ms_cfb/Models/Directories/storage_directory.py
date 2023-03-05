from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory


class StorageDirectory(Directory):

    def __init__(self, name):
        super(StorageDirectory, self).__init__()
        self.name = name
        self._type = 1
        self.directories = []

    def fileSize(self):
        return 0

    def minifatSectorsUsed(self):
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size

    def paddedBytesUsed(self):
        size = 0
        for dir in self.directories:
            size += dir.paddedBytesUsed()
        return size

    def addModule(self, module):
        stream = StreamDirectory()
        stream.name = module.modName.value
        stream.module = module
        self.directories.append(stream)

    def addFile(self, stream):
        self.directories.append(stream)

    def createBinaryTree(self):
        pass

    def flatten(self):
        self.flat = [self]
        for child in self.directories:
            if child.type == 2:
                self.flat.append(child)
            else:
                self.flat.extend(child.flatten())
        return self.flat
