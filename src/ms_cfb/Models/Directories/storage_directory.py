from ms_cfb.Models.Directories.directory import Directory
from rbtree import RedBlackTree
from typing import TypeVar


T = TypeVar('T', bound='StorageDirectory')


class StorageDirectory(Directory):

    def __init__(self: T, name: str) -> None:
        super(StorageDirectory, self).__init__()
        self.name = name
        self._type = 1
        self.directories = RedBlackTree()

    def file_size(self: T) -> int:
        return 0

    def minifat_sectors_used(self: T) -> int:
        size = 0
        for dir in self.directories:
            size += dir.minifat_sectors_used()
        return size

    def add_directory(self: T, dir: 'Directory') -> None:
        self.directories.insert(dir)

    def flatten(self: T) -> list:
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

    def set_child(self: T) -> None:
        self._subdirectory_id = self.directories.get_root()._flattened_index
        for child in self.directories:
            if child._type == 1:
                child.set_child()
