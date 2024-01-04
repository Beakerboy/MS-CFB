from datetime import datetime, timedelta
from typing import Type, TypeVar


T = TypeVar('T', bound='Filetime')


class Filetime(datetime):

    @classmethod
    def from_msfiletime(cls: Type[T], filetime: int) -> 'Filetime':
        null_date = datetime(1601, 1, 1, 0, 0, 0)
        date_time = null_date + timedelta(microseconds=filetime//10)
        timestamp = date_time.timestamp()
        return Filetime.fromtimestamp(timestamp)

    def to_msfiletime(self: T) -> int:
        """
        Convert to MS Filetime
        """
        reself = datetime(self.year, self.month, self.day, self.hour,
                          self.minute, self.second, self.microsecond)
        dif = reself - datetime(1601, 1, 1, 0, 0, 0)
        filetime = dif / timedelta(microseconds=1) * 10
        return int(filetime)
