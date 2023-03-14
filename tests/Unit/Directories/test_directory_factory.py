def test_from_binary():
    data = (b''
            + b'R\x00o\x00o\x00t\x00 \x00E\x00n\x00t\x00'
            + b'r\x00y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x16\x00\x05\x01\xff\xff\xff\xff\xff\xff\xff\xff\x01\x00\x00\x00'
            + b'\x00gaVT\xc1\xce\x11\x85S\x00\xaa\x00\xa1\xf9['
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\xbe\xab0'
            + b'\x00\x00\x00\x00\x03\x00\x00\x00@\x02\x00\x00\x00\x00\x00\x00')
    root = DirectoryFactory.from_binary(data)
