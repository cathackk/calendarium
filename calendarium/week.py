import calendar
import datetime
from contextlib import contextmanager
from typing import Any
from typing import Optional
from typing import Union

from calendarium.date_range import DateRange
from calendarium.utils import get_arg
from calendarium.utils import validate_args

# TODO: weekday enum?
# TODO: use iso weekday numbering instead? (MON=1, SUN=7)
Weekday = int
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

WEEKDAY_NAMES = ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')

ONE_WEEK = datetime.timedelta(days=7)


def get_first_weekday() -> Weekday:
    return calendar.firstweekday()


def set_first_weekday(first_weekday: Weekday) -> None:
    calendar.setfirstweekday(first_weekday)


def validate_weekday(weekday: Optional[Weekday] = None) -> Weekday:
    if weekday is None:
        return get_first_weekday()

    if not MONDAY <= weekday <= SUNDAY:
        raise calendar.IllegalWeekdayError(weekday)

    return weekday


def first_week_offset(year: int, first_weekday: Weekday = None) -> int:
    """
    Returns number OFFSET -3..+3 between year and ISO year such that the first week of given year
    starts on Jan 1 + OFFSET

    I.e. difference between year and ISO year.
    """

    # note that iso week 1 is the one with January 4th
    return 3 - (3 + calendar.monthrange(year, 1)[0] - validate_weekday(first_weekday)) % 7


def weeks_count(iso_year: int, first_weekday: Weekday = None) -> int:
    """Returns number of weeks in given ISO year: 52 or 53"""
    has_leap_week = first_week_offset(iso_year, first_weekday) - calendar.isleap(iso_year) <= -3
    return 52 + has_leap_week


def isoyear_weeknum(date: datetime.date, first_weekday: Weekday = None) -> tuple[int, int]:
    """Returns year and week num for given date."""
    year = date.year
    day_in_year = (date - datetime.date(year, 1, 1)).days
    week_num = 1 + (day_in_year - first_week_offset(year, first_weekday)) // 7

    if week_num < 1:
        return year - 1, week_num + weeks_count(year - 1, first_weekday)

    if week_num > weeks_count(year, first_weekday):
        return year + 1, week_num - weeks_count(year, first_weekday)

    return year, week_num


def first_date(year: int, weekday: Optional[Weekday] = None) -> datetime.date:
    """Returns first date of given year having the specified weekday."""
    return datetime.date(year, 1, 1 + first_week_offset(year, weekday) % 7)


class Week(DateRange):

    __slots__ = ('iso_year', 'week_num')

    def __init__(self, *args, **kwargs):

        validate_args(3, ('iso_year', 'week_num', 'first_weekday'), args, kwargs)

        if len(args) == 1 and not kwargs:
            self.iso_year, self.week_num, first_weekday = Week._args_tuple(args[0])

        elif len(args) == 1 and kwargs.keys() == {'first_weekday'}:
            self.iso_year, self.week_num, first_weekday = Week._args_tuple(args[0])
            if (first_weekday_override := kwargs['first_weekday']) is not None:
                first_weekday = first_weekday_override

        else:
            self.iso_year = int(get_arg(0, 'iso_year', args, kwargs))
            self.week_num = int(get_arg(1, 'week_num', args, kwargs))
            first_weekday = get_arg(2, 'first_weekday', args, kwargs, default=None)

        # validate year
        if not datetime.MINYEAR <= self.iso_year <= datetime.MAXYEAR:
            raise ValueError(f"year {self.iso_year} is out of range")
        # validate week_num
        if not 1 <= self.week_num <= 53:
            raise ValueError(f"week_num must be 1..53")
        if self.week_num == 53 > (year_weeks := weeks_count(self.iso_year, first_weekday)):
            raise ValueError(f"year {self.iso_year} has only {year_weeks} weeks")

        day_offset = first_week_offset(self.iso_year, first_weekday) + 7 * (self.week_num - 1)
        start_date = datetime.date(self.iso_year, 1, 1) + datetime.timedelta(days=day_offset)
        super().__init__(start_date=start_date, end_date=start_date + ONE_WEEK)

    @classmethod
    def _args_tuple(cls, obj: Any) -> tuple[int, int, Optional[Weekday]]:
        if isinstance(obj, cls):
            return obj.iso_year, obj.week_num, obj.first_weekday

        if isinstance(obj, tuple) and len(obj) == 2:
            iso_year, week_num = obj
            return int(iso_year), int(week_num), None

        if isinstance(obj, tuple) and len(obj) == 3:
            iso_year, week_num, first_weekday = obj
            return int(iso_year), int(week_num), first_weekday

        if isinstance(obj, str):
            y, w = obj.split("-W")
            return int(y), int(w), None

        raise TypeError(
            f"failed to convert single value of type {type(obj).__name__!r} into {cls.__name__}"
        )

    @classmethod
    def for_date(cls, date: datetime.date, first_weekday: Weekday = None) -> 'Week':
        return cls(*isoyear_weeknum(date, first_weekday), first_weekday)

    @classmethod
    def today(cls, first_weekday: Weekday = None) -> 'Week':
        return cls.for_date(datetime.date.today(), first_weekday)

    @property
    def first_weekday(self) -> Weekday:
        return self.start_date.weekday()

    def __repr__(self) -> str:
        if self.first_weekday != get_first_weekday():
            first_weekday_part = f', {WEEKDAY_NAMES[self.first_weekday]}'
        else:
            first_weekday_part = ''

        return f'{type(self).__name__}({self.iso_year!r}, {self.week_num!r}{first_weekday_part})'

    DEFAULT_FORMAT = "%G-W%V"

    def __str__(self) -> str:
        return format(self)

    def __format__(self, format_spec: str) -> str:
        return format(self.start_date, format_spec or self.DEFAULT_FORMAT)

    @classmethod
    def from_str(cls, text: str, first_weekday: Weekday = None) -> 'Week':
        # TODO: use parse
        y, w = text.split("-W")
        return cls(int(y), int(w), first_weekday)

    @classmethod
    def parse(
        cls, week_string: str, format_spec: str = DEFAULT_FORMAT, first_weekday: Weekday = None
    ) -> 'Week':
        # note that %g is supported for formatting, but not for parsing!
        return cls.for_date(
            date=datetime.datetime.strptime(
                f"{week_string} __{validate_weekday(first_weekday)}",
                f"{format_spec} __%w"
            ).date(),
            first_weekday=first_weekday
        )

    def toordinal(self) -> int:
        return self.start_date.toordinal()

    @classmethod
    def fromordinal(cls, ordinal: int) -> 'Week':
        return cls.starting_at(datetime.date.fromordinal(ordinal))

    @classmethod
    def starting_at(cls, date: datetime.date) -> 'Week':
        return cls.for_date(date, first_weekday=date.weekday())

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        return self.start_date == other.start_date

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.toordinal()))

    def __getitem__(self, weekday: Weekday) -> datetime.date:
        return self.start_date + datetime.timedelta(days=(weekday - self.first_weekday) % 7)

    def __lt__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.start_date < other.start_date

        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.start_date <= other.start_date

        return NotImplemented

    def __add__(self, other) -> 'Week':
        if isinstance(other, datetime.timedelta):
            return Week.for_date(self.start_date + other, first_weekday=self.first_weekday)

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return self.start_date - other.start_date

        if isinstance(other, datetime.timedelta):
            return Week.for_date(self.start_date - other, first_weekday=self.first_weekday)

        return NotImplemented


WeekLike = Union[Week, tuple[int, int], str]


@contextmanager
def having_first_weekday(first_weekday: Weekday) -> Weekday:
    original_first_weekday = get_first_weekday()
    set_first_weekday(first_weekday)

    try:
        yield first_weekday
    finally:
        set_first_weekday(original_first_weekday)
