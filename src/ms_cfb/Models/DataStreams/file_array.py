import os
from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from typing import TypeVar


T = TypeVar('T', bound='FileArray')


class FileArray(ArrayStream):
    """
    A FileArray is an array of FileStream objects.
    """

    def _render_element(self: T, index: int) -> bytes:
        """
        Implements ArrayStream._render_element()
        """
        dir = self._data[index]
        dir.to_file("temp.bin")
        f = open("temp.bin", "rb")
        data = f.read()
        f.close()
        os.remove("temp.bin")
        return data
