from ms_cfb.Models.Directories.streamDirectory import StreamDirectory
from ms_cfb.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)


def test_StreamDirectory():
    stub = ModuleStub()
    dir = StreamDirectory.createFromModule(stub)
    assert dir.type == 2
    assert dir.getData() == "foo"


class ModuleStub():

    def __init__(self):
        self.modName = DoubleEncodedString([0x0019, 0x0047], "stub")

    def getData(self):
        return "foo"
