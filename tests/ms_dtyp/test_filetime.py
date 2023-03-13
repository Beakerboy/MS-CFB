from ms_dtyp.filetime import Filetime


def test_datetime():
    time = Filetime.from_msfiletime(0x01D92433C2B823C0)
    assert date.ctime() == "Mon Jan  9 14:07:51 2023"
