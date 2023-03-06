from ms_cfb.Models.DataStreams.stream_base import StreamBase


class FileStream(StreamBase):

    def _extendData(self, data):
        """
        Add new data to the file
        """
        f = open.(self._data, "ab")
        f.write(data)
