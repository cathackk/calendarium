import datetime
from typing import Iterator
from typing import Optional

from calendarium.week import first_date
from calendarium.week import ONE_WEEK
from calendarium.week import Week
from calendarium.week import Weekday
from calendarium.week import WeekLike


class WeekRange:

    __slots__ = ('start_week', 'end_week', 'duration')

    def __init__(
        self,
        start_week: Optional[WeekLike] = None,
        end_week: Optional[WeekLike] = None,
        duration: Optional[datetime.timedelta] = None,
        weeks: Optional[int] = None,
        first_weekday: Optional[Weekday] = None,
    ):
        if weeks is not None:
            if duration is not None:
                raise TypeError(f"{type(self).__name__} doesn't accept both duration and weeks")
            duration = datetime.timedelta(weeks=weeks)

        if start_week is not None and end_week is not None:
            self.start_week = Week(start_week, first_weekday=first_weekday)
            self.end_week = Week(end_week, first_weekday=first_weekday)
            self.duration = max(self.end_week - self.start_week, datetime.timedelta())
            if duration is not None and self.duration != duration:
                raise ValueError(f"duration mismatch: expected {self.duration}, got {duration}")

        elif start_week is not None and duration is not None:
            self.start_week = Week(start_week, first_weekday=first_weekday)
            self.end_week = self.start_week + duration
            self.duration = max(self.end_week - self.start_week, datetime.timedelta())

        elif end_week is not None and duration is not None:
            self.end_week = Week(end_week, first_weekday=first_weekday)
            self.start_week = self.end_week - duration
            self.duration = max(self.end_week - self.start_week, datetime.timedelta())

        else:
            raise TypeError(f"too few arguments specified for {type(self).__name__}")

    @property
    def last_week(self) -> Week:
        return self.end_week - ONE_WEEK

    @property
    def first_weekday(self) -> Weekday:
        return self.start_week.first_weekday

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.start_week!r}, {self.end_week!r})'

    DEFAULT_FORMAT = '%G-W%V/'

    def __str__(self) -> str:
        return format(self)

    def __format__(self, format_spec: str) -> str:
        week_fmt, sep = self.split_format(format_spec or self.DEFAULT_FORMAT)
        return format(self.start_week, week_fmt) + sep + format(self.end_week, week_fmt)

    @classmethod
    def from_str(cls, text: str, first_weekday: Optional[Weekday] = None) -> 'WeekRange':
        start, end = text.split('/')
        return cls(Week.from_str(start, first_weekday), Week.from_str(end, first_weekday))

    @classmethod
    def parse(cls, text: str, format_spec: str = DEFAULT_FORMAT) -> 'WeekRange':
        week_fmt, sep = cls.split_format(format_spec)
        start, end = text.split(sep)
        return cls(Week.parse(start, week_fmt), Week.parse(end, week_fmt))

    @staticmethod
    def split_format(format_spec: str) -> tuple[str, str]:
        if ':' in format_spec:
            week_fmt, sep = format_spec.split(':')
            return week_fmt, sep
        else:
            return format_spec[:-1], format_spec[-1]

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        # empty ranges are equal
        if not self and not other:
            return True

        return self.start_week == other.start_week and self.end_week == other.end_week

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.start_week.toordinal(), self.end_week.toordinal()))

    @property
    def start_date(self) -> datetime.date:
        return self.start_week.start_date

    @property
    def last_date(self) -> datetime.date:
        return self.last_week.last_date

    @property
    def end_date(self) -> datetime.date:
        return self.end_week.start_date

    def total_days(self) -> int:
        return self.duration.days

    def __bool__(self) -> bool:
        return self.start_week < self.end_week

    def __len__(self) -> int:
        return self.total_days() // 7

    def __iter__(self) -> Iterator[Week]:
        return (
            Week.fromordinal(wo)
            for wo in range(self.start_week.toordinal(), self.end_week.toordinal(), 7)
        )

    def __contains__(self, item) -> bool:
        if isinstance(item, datetime.date):
            return self.start_date <= item < self.end_date

        try:
            week = Week(item)
        except (ValueError, TypeError):
            return False

        return self.start_week <= week < self.end_week

    def __add__(self, other) -> 'WeekRange':
        if not isinstance(other, datetime.timedelta):
            return NotImplemented

        return type(self)(self.start_week + other, self.end_week + other)

    __radd__ = __add__

    def dates(self) -> Iterator[datetime.date]:
        return (date for week in self for date in week)

    @classmethod
    def for_iso_year(cls, iso_year: int, first_weekday: Weekday = None) -> 'WeekRange':
        return cls(
            start_week=Week(iso_year, 1, first_weekday),
            end_week=Week(iso_year + 1, 1, first_weekday),
        )

    @classmethod
    def for_year(cls, year: int, first_weekday: Weekday = None) -> 'WeekRange':
        return cls(
            start_week=Week.starting_at(first_date(year, first_weekday)),
            end_week=Week.starting_at(first_date(year + 1, first_weekday))
        )

    def following(self) -> 'WeekRange':
        # doesn't use duration because of negative range corner cases
        return type(self)(self.end_week, self.end_week + (self.end_week - self.start_week))

    def preceding(self) -> 'WeekRange':
        # doesn't use duration because of negative range corner cases
        return type(self)(self.start_week - (self.end_week - self.start_week), self.start_week)
