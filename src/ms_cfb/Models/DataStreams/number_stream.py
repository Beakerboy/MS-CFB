from ms_cfb.Models.DataStreams.array_stream import ArrayStream


class NumberStream(ArrayStream):

    def _render_element(self, element) -> bytes:
        return element.to_bytes(4, "little")
        
