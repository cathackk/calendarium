import calendar
import datetime
import re
from typing import Any
from typing import Union

from calendarium.date_range import DateRange

# except for leap years
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Month(DateRange):
    # TODO: doctests

    __slots__ = ('year', 'month')

    # TODO: use @singledisatchmethod?
    def __init__(self, *args, year: int = None, month: int = None):
        if year is not None and month is not None:
            if args:
                raise TypeError(
                    f"{type(self).__name__} expects only args or only kwargs, but not both"
                )
            self.year, self.month = int(year), int(month)
        elif year is not None or month is not None:
            raise TypeError(f"{type(self).__name__} requires both year and month, not just one")
        elif len(args) == 1:
            self.year, self.month = Month._ym_tuple(args[0])
        elif len(args) == 2:
            self.year, self.month = int(args[0]), int(args[1])
        else:
            raise TypeError(f"{type(self).__name__} expected 1 or 2 arguments, got {len(args)}")

        start_date = datetime.date(self.year, self.month, 1)

        if self.month < 12:
            # 2022-09 -> end_date = 2022-10-01
            end_date = datetime.date(self.year, self.month + 1, 1)
        elif self.year < datetime.MAXYEAR:
            # 2022-12 -> end_date = 2023-01-01
            end_date = datetime.date(self.year + 1, 1, 1)
        else:
            # 9999-12 -> end_date 9999-31-12 (max date!)
            end_date = datetime.date(datetime.MAXYEAR, 12, 31)

        super().__init__(start_date, end_date)

    @classmethod
    def _ym_tuple(cls, obj: Any) -> tuple[int, int]:
        if isinstance(obj, cls):
            return obj.year, obj.month

        if isinstance(obj, tuple) and len(obj) == 2:
            year, month = obj
            return int(year), int(month)

        if isinstance(obj, str):
            try:
                date = datetime.datetime.strptime(obj, cls.DEFAULT_FORMAT).date()
                return date.year, date.month
            except ValueError as exc:
                raise ValueError(f"failed to parse {cls.__name__} from {obj!r}") from exc

        raise TypeError(f"failed to convert {type(obj).__name__} into {cls.__name__}")

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.year!r}, {self.month!r})'

    DEFAULT_FORMAT = '%Y-%m'

    def __str__(self) -> str:
        return format(self)

    def __format__(self, format_spec: str) -> str:
        return format(self.start_date, format_spec or self.DEFAULT_FORMAT)

    @classmethod
    def parse(cls, month_string: str, format_spec: str = DEFAULT_FORMAT) -> 'Month':
        return cls.for_date(datetime.datetime.strptime(month_string, format_spec).date())

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.year == other.year
            and self.month == other.month
        )

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.ord()))

    def is_leap(self) -> bool:
        return self.month == 2 and calendar.isleap(self.year)

    def days(self) -> int:
        return len(self)

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

    def __sub__(self, other) -> 'MonthDelta':
        # month - month
        if isinstance(other, Month):
            return MonthDelta(self.ord() - other.ord())

        return NotImplemented

    @classmethod
    def for_date(cls, date: datetime.date) -> 'Month':
        return cls(date.year, date.month)

    @classmethod
    def today(cls) -> 'Month':
        return cls.for_date(datetime.date.today())


MonthLike = Union[Month, tuple[int, int], str]


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

    @classmethod
    def from_str(cls, md_string: str) -> 'MonthDelta':
        match = re.fullmatch(r'([+-])?P([+-]?\d+Y)?([+-]?\d+M)?', md_string)
        if not match:
            raise ValueError(f'invalid string for {cls.__name__}: {md_string!r}')

        sign_group, year_group, month_group = match.groups()
        if not year_group and not month_group:
            raise ValueError(f'invalid string for {cls.__name__}: {md_string!r}')

        sign = -1 if sign_group == '-' else +1
        return cls(
            months=sign * int((month_group or '0').rstrip('M')),
            years=sign * int((year_group or '0').rstrip('Y')),
        )

    @classmethod
    def between(cls, start_month: MonthLike, end_month: MonthLike):
        return Month(end_month) - Month(start_month)

    def __eq__(self, other) -> bool:
        return self.months == other.months

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.years, self.months))

    def __neg__(self) -> 'MonthDelta':
        return type(self)(years=-self.years, months=-self.months)

    def __abs__(self) -> 'MonthDelta':
        return type(self)(months=abs(self.total_months()))

    def __bool__(self) -> bool:
        return bool(self.total_months())

    def __add__(self, other):
        # monthdelta + month
        if isinstance(other, Month):
            return type(other).from_ord(other.ord() + self.total_months())

        # monthdelta + monthdelta
        if isinstance(other, MonthDelta):
            return type(other)(months=self.total_months() + other.total_months())

        # monthdelta + date
        if isinstance(other, datetime.date):
            month = Month.for_date(other) + self
            return type(other)(year=month.year, month=month.month, day=min(other.day, len(month)))

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

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.total_months() < other.total_months()

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.total_months() <= other.total_months()

        return NotImplemented
