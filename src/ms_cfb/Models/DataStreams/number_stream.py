from ms_cfb.Models.DataStreams.array_stream import ArrayStream


class NumberStream(ArrayStream):

    def _render_element(self, element) -> bytes:
        return element.to_bytes(4, "little")

    def stream_size(self) -> int:
        return len(self._data) * 4
