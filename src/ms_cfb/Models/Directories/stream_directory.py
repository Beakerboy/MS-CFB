import is
from ms_cfb.Models.Directories.directory import Directory


class StreamDirectory(Directory):

    def __init__(self):
        super(StreamDirectory, self).__init__()
        self.type = 2

        # How many bytes does this item reserve in the file.
        # This includes padding to fill a sector or ministream.
        self.bytesUsed = 0
        self.file_path = ""

    def set_created(self, datetime):
        raise Exception("File Directory must have created date of zero.")

    def set_modified(self, datetime):
        raise Exception("File Directory must have modified date of zero.")

    def set_file(path):
        self.file_path = path

    def setBytesReserved(self, quantity):
        self.bytesUsed = quantity

    def fileSize(self) -> int:
        """
        Size in bytes of the file
        """
        return os.stat(self.file_path).st_size

    def minifatSectorsUsed(self):
        return (self.fileSize() - 1) // 64 + 1
