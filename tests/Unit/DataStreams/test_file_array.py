from ms_cfb.Models.DataStreams.file_array import FileArray


def test_constructor() -> None:
    stream = FileArray()
    assert isinstance(stream, FileArray)


def test_stream_size() -> None:
    stream = FileArray()
    stream.set_storage_size(512)
    file1 = open('file1.bin', 'ab')
    file1.write(b'\x01')
    file1.close()
    stream.append('file1.bin')
    assert stream.stream_size() == 512
    
    
