from ms_cfb.Models.Directories.stream_directory import StreamDirectory


def test_StreamDirectory():
    stub = ModuleStub()
    dir = StreamDirectory.createFromModule(stub)
    assert dir.type == 2
    assert dir.getData() == "foo"


def test_add_created():
    dir = StreamDirectory()
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_created(date)


def test_add_created():
    dir = StreamDirectory()
    with pytest.raises(Exception):
        date = 0x12345
        dir.set_modified(date)


class FieldStub:
    value = 'stub'


class ModuleStub():

    def __init__(self):
        self.modName = FieldStub()

    def getData(self):
        return "foo"
