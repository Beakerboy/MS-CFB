from ms_cfb.Models.Directories.directory import Directory


class StorageDirectory(Directory):

    def __init__(self, name):
        super(StorageDirectory, self).__init__()
        self.name = name
        self._type = 1
        self.directories = []

    def file_size(self):
        return 0

    def minifat_sectors_used(self):
        size = 0
        for dir in self.directories:
            size += dir.minifat_sectors_used()
        return size

    def padded_bytes_used(self):
        size = 0
        for dir in self.directories:
            size += dir.padded_bytes_used()
        return size

    def add_directory(self, stream):
        self.directories.append(stream)

    def create_binary_tree(self):
        pass

    def flatten(self):
        self.flat = [self]
        for child in self.directories:
            if child._type == 2:
                self.flat.append(child)
            else:
                self.flat.extend(child.flatten())
        i = 0
        for dir in self.flat:
            dir._flattened_index = i
            i += 1
        return self.flat

    def set_child(self):
        if len(self.directories) == 1:
            self._subdirectory_id = self.directories[0]._flattened_index
        for child in self.directories:
            if child._type == 1:
                child.set_child()
