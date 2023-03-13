from datetime import datetime, timedelta


class Filetime(datetime):

    @classmethod
    def from_msfiletime(cls, filetime: int):
        null_date = datetime(1601, 1, 1, 0, 0, 0)
        date_time = null_date + timedelta(microseconds=filetime//10)
        timestamp = date_time.timestamp()
        return Filetime.fromtimestamp(timestamp)

    def to_msfiletime(self) -> int:
        """
        Convert to MS Filetime
        """
        return (self - datetime(1601, 1, 1, 0, 0, 0)) * 10
