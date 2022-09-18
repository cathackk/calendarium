import datetime
from typing import Iterator

from calendarium.date_range import DateRange

# except for leap years
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Month:
    # TODO: doctests

    __slots__ = ('year', 'month', 'start_date', 'end_date')

    def __init__(self, year: int, month: int):
        self.year = int(year)
        self.month = int(month)
        self.start_date = datetime.date(self.year, self.month, 1)

        if self.month < 12:
            # 2022-09 -> end_date = 2022-10-01
            self.end_date = datetime.date(self.year, self.month + 1, 1)
        elif self.year < datetime.MAXYEAR:
            # 2022-12 -> end_date = 2023-01-01
            self.end_date = datetime.date(self.year + 1, 1, 1)
        else:
            # 9999-12 -> end_date 9999-31-12 (max date!)
            self.end_date = datetime.date(datetime.MAXYEAR, 12, 31)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.year!r}, {self.month!r})'

    DEFAULT_FORMAT = '%Y-%m'

    def __str__(self) -> str:
        return format(self)

    def __format__(self, format_spec: str) -> str:
        return format(self.start_date, format_spec or self.DEFAULT_FORMAT)

    @classmethod
    def from_str(cls, month_string: str) -> 'Month':
        return cls.parse(month_string)

    @classmethod
    def parse(cls, month_string: str, format_spec: str = DEFAULT_FORMAT) -> 'Month':
        return cls.for_date(datetime.datetime.strptime(month_string, format_spec).date())

    def __eq__(self, other) -> bool:
        return self.year == other.year and self.month == other.month

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.ord()))

    def is_leap(self) -> bool:
        return (
            self.month == 2
            and self.year % 4 == 0
            and (self.year % 100 != 0 or self.year % 400 == 0)
        )

    def days(self) -> int:
        return DAYS_IN_MONTH[self.month - 1] + self.is_leap()

    def __len__(self) -> int:
        return self.days()

    def __iter__(self) -> Iterator[datetime.date]:
        return iter(DateRange(self))

    def __contains__(self, date) -> bool:
        return self.start_date <= date < self.end_date

    def __lt__(self, other) -> bool:
        if isinstance(other, Month):
            return self.ord() < other.ord()

        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, Month):
            return self.ord() <= other.ord()

        return NotImplemented

    EPOCH = (1970, 1)
    EPOCH_Y, EPOCH_M = EPOCH

    def ord(self) -> int:
        return (self.year - self.EPOCH_Y) * 12 + (self.month - self.EPOCH_M)

    @classmethod
    def from_ord(cls, ord_: int) -> 'Month':
        year, month = divmod(ord_, 12)
        return cls(year + cls.EPOCH_Y, month + cls.EPOCH_M)

    def __sub__(self, other):
        # month - month
        if isinstance(other, Month):
            return MonthDelta(self.ord() - other.ord())

        return NotImplemented

    @property
    def last_date(self) -> datetime.date:
        return datetime.date(self.year, self.month, len(self))

    @classmethod
    def for_date(cls, date: datetime.date) -> 'Month':
        return cls(date.year, date.month)

    @classmethod
    def today(cls) -> 'Month':
        return cls.for_date(datetime.date.today())


class MonthDelta:
    __slots__ = ('years', 'months')

    def __init__(self, months: int = 0, *, years: int = 0):
        total_months = int(years * 12 + months)
        self.years, self.months = divmod(abs(total_months), 12)
        if total_months < 0:
            self.years, self.months = -self.years, -self.months

    def total_months(self) -> int:
        return self.years * 12 + self.months

    def __repr__(self) -> str:
        def parts():
            if self.years:
                yield f'years={self.years!r}'
            if self.months:
                yield f'months={self.months!r}'
        kwargs_repr = ', '.join(parts()) or '0'
        return f'{type(self).__name__}({kwargs_repr})'

    def __str__(self) -> str:
        def parts():
            if self.years:
                yield f'{abs(self.years)}Y'
            if self.months:
                yield f'{abs(self.months)}M'

        sign = '-' if self.total_months() < 0 else ''
        parts_str = ''.join(parts()) or '0M'
        return f'{sign}P{parts_str}'

    def __eq__(self, other) -> bool:
        return self.months == other.months

    def __neg__(self) -> 'MonthDelta':
        return type(self)(years=-self.years, months=-self.months)

    def __add__(self, other):
        # monthdelta + month
        if isinstance(other, Month):
            return type(other).from_ord(other.ord() + self.total_months())

        # monthdelta + monthdelta
        if isinstance(other, MonthDelta):
            return type(self)(self.total_months() + other.total_months())

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        try:
            return self + (-other)
        except TypeError:
            return NotImplemented

    def __rsub__(self, other):
        try:
            return (-self) + other
        except TypeError:
            return NotImplemented

    def __mul__(self, other):
        return type(self)(self.total_months() * other)

    def __floordiv__(self, other):
        return type(self)(self.total_months() // other)
