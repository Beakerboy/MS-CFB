from ms_cfb.Models.DataStreams.stream_base import StreamBase


class ArrayStream(StreamBase):

    def to_file(self, path):
        f = open(path, "wb")
        for element in self._data:
            f.write(self._render_element(element))
        f.close()

    def _render_element(self, element) -> bytes:
        raise Exception("must be implemented")
