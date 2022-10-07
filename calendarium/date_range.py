import datetime
from typing import Iterator


ONE_DAY = datetime.timedelta(days=1)


class DateRange:

    __slots__ = ('start_date', 'end_date')

    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date = start_date
        self.end_date = end_date

    @property
    def last_date(self) -> datetime.date:
        return self.end_date - ONE_DAY

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_date - self.start_date

    def __iter__(self) -> Iterator[datetime.date]:
        date = self.start_date
        while date < self.end_date:
            yield date
            date += ONE_DAY

    def __contains__(self, item) -> bool:
        if not isinstance(item, datetime.date):
            return False

        return self.start_date <= item < self.end_date

    def __len__(self) -> int:
        return (self.end_date - self.start_date).days
