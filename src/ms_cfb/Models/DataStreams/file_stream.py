import os
import shutil
from ms_cfb.Models.DataStreams.stream_base import StreamBase


class FileStream(StreamBase):

    def __init__(self, file_path):
        super(FileStream, self).__init__()
        self._data = file_path

    def stream_size(self):
        """
        From StreamBase
        """
        return os.stat(self._data).st_size

    def _extend_data(self, data):
        """
        From StreamBase
        Add new data to the file
        """
        f = open(self._data, "ab")
        f.write(data)

    def to_file(self, path):
        shutil.copy(self._data, path)
        length = os.stat(path).st_size
        sector_size = self._storageChain.get_sector_size()
        if length % sector_size == 0:
            mod = sector_size
        else:
            mod = length % sector_size
        fill = (sector_size - mod) // len(self._padding)
        c = open(path, "ab")
        c.write(self._padding * fill)
