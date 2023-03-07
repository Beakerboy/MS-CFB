from ms_cfb.Models.DataStreams.stream_base import StreamBase


class ArrayStream(StreamBase):

    to_file(path):
        f = open(path, "wb")
        for element in self._data:
            f.write(self._render_element(element))
        f.close()
