from ms_cfb.Models.DataStreams.file_array import FileArray


def test_constructor() -> None:
    stream = FileArray()
    assert isinstance(stream, FileArray)
