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

    def timedelta(self) -> datetime.timedelta:
        return (self.end_date - self.start_date) if self else datetime.timedelta()

    def total_days(self) -> int:
        return self.timedelta().days

    def dates(self) -> Iterator[datetime.date]:
        date = self.start_date
        while date < self.end_date:
            yield date
            date += ONE_DAY

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        # all empty ranges are equal
        if not self and not other:
            return True

        return self.start_date == other.start_date and self.end_date == other.end_date

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.start_date, self.end_date))

    def __bool__(self) -> bool:
        return self.start_date < self.end_date

    def __contains__(self, item) -> bool:
        if not isinstance(item, datetime.date):
            return False

        return self.start_date <= item < self.end_date


class DateRangeDays(DateRange):
    def __iter__(self) -> Iterator[datetime.date]:
        return self.dates()

    def __len__(self) -> int:
        return self.total_days()
