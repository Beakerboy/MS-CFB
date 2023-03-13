from ms_dtyp.filetime import Filetime


def test_datetime():
    date = Filetime.from_msfiletime(0x01D92433C2B823C0)
    assert date.ctime() == "Mon Jan  9 14:07:51 2023"


def test_to_msfiletime():
    date = "1995/11/16 17:43:45"
    obj = Filetime.fromisoformat(date)
    assert obj.to_msfiletime() == 0x01BAB44B13921E80
