from ms_cfb.Models.DataStreams.file_stream import FileStream


def test_constructor() -> None:
    path = "./foo.txt"
    stream = FileStream(path)
    assert isinstance(stream, FileStream)
