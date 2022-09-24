import calendar
import datetime
from functools import singledispatchmethod

from calendarium.date_range import DateRange

# TODO: weekday enum?
Weekday = int
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

WEEKDAY_NAMES = ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')


get_first_weekday = calendar.firstweekday
set_first_weekday = calendar.setfirstweekday


def first_week_offset(year: int, first_weekday: Weekday = None) -> int:
    """
    Returns number OFFSET -3..+3 such that the first week of given year starts on Jan 1 + OFFSET
    """
    if first_weekday is None:
        first_weekday = get_first_weekday()

    # week 1 is the one with January 4th
    jan_4_weekday = (calendar.monthrange(year, 1)[0] + 3) % 7
    return 3 - (jan_4_weekday - first_weekday) % 7


def weeks_count(year: int, first_weekday: Weekday = None) -> int:
    """Returns number of weeks in given year: 52 or 53"""
    has_leap_week = first_week_offset(year, first_weekday) - calendar.isleap(year) <= -3
    return 52 + has_leap_week


def year_week_num(date: datetime.date, first_weekday: Weekday = None) -> tuple[int, int]:
    """Returns year and week num for given date."""
    year = date.year
    day_in_year = (date - datetime.date(year, 1, 1)).days
    week_num = 1 + (day_in_year - first_week_offset(year, first_weekday)) // 7

    if week_num < 1:
        return year - 1, week_num + weeks_count(year - 1, first_weekday)

    if week_num > weeks_count(year):
        return year + 1, week_num - weeks_count(year, first_weekday)

    return year, week_num


class Week(DateRange):

    __slots__ = ('year', 'week_num')

    @singledispatchmethod
    def __init__(self, year: int, week_num: int, first_weekday: Weekday = None):
        # validate year
        if not datetime.MINYEAR <= year <= datetime.MAXYEAR:
            raise ValueError(f"year {year} is out of range")
        # validate week_num
        if not 1 <= week_num <= 53:
            raise ValueError(f"week_num must be 1..53")
        if week_num == 53 > (year_weeks := weeks_count(year, first_weekday)):
            raise ValueError(f"year {year} has only {year_weeks} weeks")

        self.year = year
        self.week_num = week_num

        day_offset = first_week_offset(self.year, first_weekday) + 7 * (self.week_num - 1)
        start_date = datetime.date(self.year, 1, 1) + datetime.timedelta(days=day_offset)
        super().__init__(start_date=start_date, end_date=start_date + datetime.timedelta(days=7))

    @__init__.register
    def _init_from_date(self, date: datetime.date):
        self.start_date = date
        self.year, self.week_num = year_week_num(date, date.weekday())

    @property
    def first_weekday(self) -> Weekday:
        return self.start_date.weekday()

    def __repr__(self) -> str:
        if self.first_weekday != get_first_weekday():
            first_weekday_part = f', {WEEKDAY_NAMES[self.first_weekday]}'
        else:
            first_weekday_part = ''

        return f'{type(self).__name__}({self.year!r}, {self.week_num!r}{first_weekday_part})'

    def __str__(self) -> str:
        return f"{self.year:04}-W{self.week_num:02}"

    @classmethod
    def from_str(cls, text: str, first_weekday: Weekday = None) -> 'Week':
        y, w = text.split("-W")
        return cls(int(y), int(w), first_weekday)

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        return (
            self.year == other.year
            and self.week_num == other.week_num
            and self.first_weekday == other.first_weekday
        )

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.year, self.week_num, self.first_weekday))

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

    @classmethod
    def for_date(cls, date: datetime.date, first_weekday: Weekday = None) -> 'Week':
        return cls(*year_week_num(date, first_weekday), first_weekday)

    @classmethod
    def today(cls, first_weekday: Weekday = None) -> 'Week':
        return cls.for_date(datetime.date.today(), first_weekday)
