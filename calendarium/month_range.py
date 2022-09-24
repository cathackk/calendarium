import datetime
from typing import Iterator
from typing import Optional

from calendarium.month import Month
from calendarium.month import MonthDelta
from calendarium.month import MonthLike


# TODO: inherit from DateRange?
#  but that way it would iterate over dates
#  and has length of total_days(), not number of months


class MonthRange:

    __slots__ = ('start_month', 'end_month', 'duration')

    def __init__(
        self,
        start_month: Optional[MonthLike] = None,
        end_month: Optional[MonthLike] = None,
        duration: Optional[MonthDelta] = None,
        months: Optional[int] = None,
    ):
        if months is not None:
            if duration is not None:
                raise TypeError(f"{type(self).__name__} doesn't accept both duration and months")
            duration = MonthDelta(months)

        if start_month is not None and end_month is not None:
            self.start_month = Month(start_month)
            self.end_month = Month(end_month)
            self.duration = max(self.end_month - self.start_month, MonthDelta())
            if duration is not None and self.duration != duration:
                raise ValueError(f"duration mismatch: expected {self.duration}, got {duration}")

        elif start_month is not None and duration is not None:
            self.start_month = Month(start_month)
            self.duration = max(duration, MonthDelta())
            self.end_month = self.start_month + duration

        elif end_month is not None and duration is not None:
            self.end_month = Month(end_month)
            self.duration = max(duration, MonthDelta())
            self.start_month = self.end_month - duration

        else:
            raise ValueError(f"too few arguments specified for {type(self).__name__}")

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.start_month!r}, {self.end_month!r})'

    DEFAULT_FORMAT = '%Y-%m/'

    def __str__(self) -> str:
        return format(self)

    def __format__(self, format_spec: str) -> str:
        month_fmt, sep = self.split_format(format_spec or self.DEFAULT_FORMAT)
        return format(self.start_month, month_fmt) + sep + format(self.end_month, month_fmt)

    @classmethod
    def from_str(cls, text: str) -> 'MonthRange':
        return cls.parse(text)

    @classmethod
    def parse(cls, text: str, format_spec: str = DEFAULT_FORMAT) -> 'MonthRange':
        month_fmt, sep = cls.split_format(format_spec)
        start, end = text.split(sep)
        return cls(Month.parse(start, month_fmt), Month.parse(end, month_fmt))

    @staticmethod
    def split_format(format_spec: str) -> tuple[str, str]:
        if ':' in format_spec:
            month_fmt, sep = format_spec.split(':')
            return month_fmt, sep
        else:
            return format_spec[:-1], format_spec[-1]

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        # empty ranges are equal
        if not self and not other:
            return True

        return self.start_month == other.start_month and self.end_month == other.end_month

    def __hash__(self) -> int:
        if self:
            return hash((type(self).__name__, self.start_month.ord(), self.end_month.ord()))
        else:
            return hash((type(self).__name__, 0, 0))

    def __len__(self) -> int:
        return self.duration.total_months()

    def __iter__(self) -> Iterator[Month]:
        return (
            Month.from_ord(mo)
            for mo in range(self.start_month.ord(), self.end_month.ord())
        )

    def __contains__(self, item):
        if isinstance(item, datetime.date):
            return self.start_date <= item < self.end_date

        return self.start_month <= Month(item) < self.end_month

    def __add__(self, other) -> 'MonthRange':
        if isinstance(other, MonthDelta):
            return type(self)(self.start_month + other, self.end_month + other)

        return NotImplemented

    __radd__ = __add__

    def __bool__(self) -> bool:
        return self.start_month < self.end_month

    def days(self) -> Iterator[datetime.date]:
        return (date for month in self for date in month)

    @property
    def start_date(self) -> datetime.date:
        return self.start_month.start_date

    @property
    def end_date(self) -> datetime.date:
        return self.end_month.start_date

    @property
    def last_date(self) -> datetime.date:
        return self.end_month.start_date - datetime.timedelta(1)

    def timedelta(self) -> datetime.timedelta:
        return self.end_date - self.start_date if self else datetime.timedelta(0)

    def total_days(self) -> int:
        return self.timedelta().days

    @classmethod
    def year(cls, year: int) -> 'MonthRange':
        return cls((year, 1), (year + 1, 1))

    @classmethod
    def quarter(cls, year: int, q: int) -> 'MonthRange':
        try:
            return cls(start_month=(year, q * 3 - 2), months=3)
        except ValueError:
            raise ValueError("quarter must be in 1..4")

    @classmethod
    def halfyear(cls, year: int, half: int) -> 'MonthRange':
        try:
            return cls(start_month=(year, half * 6 - 5), months=6)
        except ValueError:
            raise ValueError("half must be 1 or 2")

    def following(self) -> 'MonthRange':
        return type(self)(self.end_month, self.end_month + (self.end_month - self.start_month))

    def preceding(self) -> 'MonthRange':
        return type(self)(self.start_month - (self.end_month - self.start_month), self.start_month)
