import os
from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.DataStreams.file_stream import FileStream
from typing import TypeVar


T = TypeVar('T', bound='FileArray')


class FileArray(ArrayStream):

    def stream_size(self: T) -> int:
        sum = 0
        for stream in self._data:
            sectors = ((stream.stream_size() - 1) // 64 + 1)
            sum += sectors * 64
        return sum

    def _render_element(self: T, dir: 'FileStream') -> bytes:
        dir.to_file("temp.bin")
        f = open("temp.bin", "rb")
        data = f.read()
        f.close()
        os.remove("temp.bin")
        return data
