import datetime


class Filetime(datetime):

    @classmethod
    from_msfiletime(cls, filetime: int):
        _FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
        date_time = _FILETIME_null_date + datetime.timedelta(microseconds=self._filetime//10)
        timestamp = date_time.timestamp()
        return Filetime.fromtimestamp(timestamp)

    to_msfiletime(self) -> int:
        """
        Convert to MS Filetime
        """
        return (self - datetime.datetime(1601, 1, 1, 0, 0, 0)) * 10
