import os
import shutil
from ms_cfb.Models.DataStreams.stream_base import StreamBase


class FileStream(StreamBase):

    def __init__(self, file_path):
        super(FileStream, self).__init__()
        self._data = file_path

    def streamSize(self):
        """
        From StreamBase
        """
        return os.stat(self._data).st_size

    def _extendData(self, data):
        """
        From StreamBase
        Add new data to the file
        """
        f = open(self._data, "ab")
        f.write(data)

    def to_file(self, path):
        shutil.copy(self._data, path)
    
