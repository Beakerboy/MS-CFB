import os
from ms_cfb.Models.DataStreams.array_stream import ArrayStream
from ms_cfb.Models.DataStreams.file_stream import FileStream


class FileArray(ArrayStream):

    def _render_element(self, dir: 'FileStream') -> bytes:
        dir.to_file("temp.bin")
        f = open("temp.bin", "rb")
        data = f.read()
        f.close()
        os.remove("temp.bin")
        return data
