import os
from ms_cfb.Models.DataStreams.array_stream import ArrayStream


class DirectoryStream(ArrayStream):

    def _render_element(self, dir) -> bytes:
        dir.to_file("temp.bin")
        f = open("temp.bin", "rb")
        data = f.read()
        f.close()
        os.remove("temp.bin")
        return data
        
