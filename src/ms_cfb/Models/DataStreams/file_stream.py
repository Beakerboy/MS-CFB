import os
import shutil
from ms_cfb.Models.DataStreams.stream_base import StreamBase
from typing import TypeVar


T = TypeVar('T', bound='FileStream')


class FileStream(StreamBase):

    def __init__(self: T, file_path: str) -> None:
        super(FileStream, self).__init__()
        self._data = file_path

    def stream_size(self: T) -> int:
        """
        From StreamBase
        """
        return os.stat(self._data).st_size

    def _extend_data(self: T, data: bytes) -> None:
        """
        From StreamBase
        Add new data to the file
        """
        f = open(self._data, "ab")
        f.write(data)

    def to_file(self: T, path: str) -> None:
        shutil.copy(self._data, path)
        length = os.stat(path).st_size
        if length % self._storage_sector_size == 0:
            mod = self._storage_sector_size
        else:
            mod = length % self._storage_sector_size
        fill = (self._storage_sector_size - mod) // len(self._padding)
        c = open(path, "ab")
        c.write(self._padding * fill)
