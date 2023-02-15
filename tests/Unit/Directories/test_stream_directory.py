from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from ms_cfb.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)


def test_StreamDirectory():
    stub = ModuleStub()
    dir = StreamDirectory.createFromModule(stub)
    assert dir.type == 2
    assert dir.getData() == "foo"


class FieldStub:
    value = stub
    
class ModuleStub():
    
    def __init__(self):
        self.modName = FieldStub()

    def getData(self):
        return "foo"
