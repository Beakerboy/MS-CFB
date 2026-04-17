from ms_dtyp.filetime import Filetime


def test_datetime() -> None:
    date = Filetime.from_msfiletime(0x01D92433C2B823C0)
    assert date.ctime() == "Mon Jan  9 14:07:51 2023"


def test_to_msfiletime() -> None:
    date = "1995-11-16 17:43:45"
    obj = Filetime.fromisoformat(date)
    assert obj.to_msfiletime() == 0x01BAB44B13921E80
    ts = obj.timestamp()
    obj2 = Filetime.fromtimestamp(ts)
    assert obj2.to_msfiletime() == 0x01BAB44B13921E80


def test_from_msfiletime_zero() -> None:
    date = Filetime.from_msfiletime(0)
    assert (date.year, date.month, date.day) == (1601, 1, 1)
    assert (date.hour, date.minute, date.second, date.microsecond) == (0, 0, 0, 0)


def test_from_msfiletime_pre_epoch() -> None:
    unix_epoch_filetime = Filetime.fromisoformat("1970-01-01 00:00:00").to_msfiletime()
    one_second_before_epoch = unix_epoch_filetime - 10_000_000
    date = Filetime.from_msfiletime(one_second_before_epoch)
    assert (date.year, date.month, date.day) == (1969, 12, 31)
    assert (date.hour, date.minute, date.second) == (23, 59, 59)
