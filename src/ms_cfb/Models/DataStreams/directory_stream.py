from ms_cfb.Models.DataStreams.array_stream import ArrayStream


class DirectoeyStream(ArrayStream):

    def _render_element(self, dir) -> bytes:
        return dir.to_bytes()

    def stream_size(self) -> int:
        return len(self._data) * 16 * 8
