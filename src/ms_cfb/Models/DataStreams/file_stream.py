from ms_cfb.Models.DataStreams.stream_base import StreamBase


class FileStream(StreamBase):

    def __init__(self, file_path):
        super(FileStream, self).__init__()
        self._data = file_path

    def _extendData(self, data):
        """
        Add new data to the file
        """
        f = open(self._data, "ab")
        f.write(data)
