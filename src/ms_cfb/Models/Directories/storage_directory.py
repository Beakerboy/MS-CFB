from ms_cfb.Models.Directories.directory import Directory
from rbtree import RedBlackTree
from typing import TypeVar


T = TypeVar('T', bound='StorageDirectory')


class StorageDirectory(Directory):
    """
    A StorageDirectory represents a file system diresctory. It adds a red-black
    tree to the parent class as a way to organize its contents.
    """

    def __init__(self: T, name: str) -> None:
        super(StorageDirectory, self).__init__()
        self.name = name
        self._key = (len(self.name), self.name.upper())
        self._type = 1
        self.directories = RedBlackTree()

    def __str__(self: T) -> str:
        return (self.get_name() +
                "\n\tCreated: " + str(self._created) +
                "\n\tModified: " + str(self._modified) +
                "\n\tGUID: " + str(self._class_id))

    def get_subdirectory_index(self: T) -> int:
        """
        Overriding Directory.get_subdirectory_index()
        If the red-black tree has a root, return its flattened index.
        """
        node = self.directories.get_root()
        if node.is_null():
            return 0xFFFFFFFF
        return node._flattened_index

    def minifat_sectors_used(self: T) -> int:
        size = 0
        for dir in self.directories:
            size += dir.minifat_sectors_used()
        return size

    def add_directory(self: T, dir: 'Directory') -> None:
        self.directories.insert(dir)

    def flatten(self: T) -> list:
        flat = [self]
        for child in self.directories:
            if child._type != 2:
                flat.extend(child.flatten())
            else:
                flat.append(child)
        i = 0
        for dir in flat:
            dir._flattened_index = i
            i += 1
        return flat

    def create_file_tree(self: T, depth: int) -> list:
        tree = [(depth, self.name)]
        for child in self.directories:
            if child._type != 2:
                tree.extend(child.create_file_tree(depth + 1))
            else:
                tree.append((depth + 1, child.name))
        return tree
