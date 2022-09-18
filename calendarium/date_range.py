import datetime
from typing import Iterator


class DateRange:
    # TODO: implement properly
    def __init__(self, rangelike):
        self.start_date = rangelike.start_date
        self.end_date = rangelike.end_date

    def __iter__(self) -> Iterator[datetime.date]:
        date = self.start_date
        while date < self.end_date:
            yield date
            date += datetime.timedelta(days=1)
