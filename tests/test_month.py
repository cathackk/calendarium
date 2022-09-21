import datetime
from typing import Iterable

from freezegun import freeze_time
import pytest

from calendarium.month import Month
from calendarium.month import MonthDelta


def test_init():
    m1 = Month(2001, 12)
    assert m1.year == 2001
    assert m1.month == 12

    m2 = Month(year=1998, month=3)
    assert m2.year == 1998
    assert m2.month == 3


def test_init_alt():
    m1 = Month("2001-10")
    assert m1.year == 2001
    assert m1.month == 10

    m2 = Month((1999, 3))
    assert m2.year == 1999
    assert m2.month == 3

    m3 = Month(m2)
    assert m3.year == 1999
    assert m3.month == 3


def test_init_invalid():
    with pytest.raises(TypeError) as exc_info:
        Month()
    assert str(exc_info.value) == "Month expected 1 or 2 arguments, got 0"

    with pytest.raises(TypeError) as exc_info:
        Month(1999, 2, 3)
    assert str(exc_info.value) == "Month expected 1 or 2 arguments, got 3"

    with pytest.raises(TypeError) as exc_info:
        Month(2003, 1, year=2002, month=4)
    assert str(exc_info.value) == "Month expects only args or only kwargs, but not both"

    with pytest.raises(ValueError) as exc_info:
        Month("xxx")
    assert str(exc_info.value) == "failed to parse Month from 'xxx'"



def test_init_year_validation():
    for year in [1, 100, 333, 1000, 1453, 1999, 2000, 2100, 5011, 9999]:
        assert Month(year, 1).year == year
        assert Month(year, 12).year == year

    for year in (-1167, -1, 0, 10_000, 40_000):
        with pytest.raises(ValueError) as exc_info:
            Month(year, 1)

        assert str(exc_info.value) == f"year {year} is out of range"


def test_init_month_number_validation():
    for month_number in range(1, 13):
        assert Month(2000, month_number).month == month_number

    for month_number in (-1, 0, 13, 20):
        with pytest.raises(ValueError) as exc_info:
            Month(2022, month_number)

        assert str(exc_info.value) == "month must be in 1..12"


def test_repr():
    assert repr(Month(2022, 9)) == 'Month(2022, 9)'
    assert repr(Month(1998, 11)) == 'Month(1998, 11)'
    assert repr(Month(500, 11)) == 'Month(500, 11)'


def test_str():
    assert str(Month(2001, 1)) == "2001-01"
    assert str(Month(2013, 10)) == "2013-10"


def test_format():
    m = Month(2022, 9)
    assert format(m) == "2022-09"
    assert format(m, '%m/%Y') == "09/2022"
    assert format(m, '%b %y') == 'Sep 22'
    assert format(m, '%B %Y') == 'September 2022'


def test_parse():
    assert Month.parse("2022-09") == Month(2022, 9)
    assert Month.parse("12/2013", '%m/%Y') == Month(2013, 12)
    # https://pubs.opengroup.org/onlinepubs/007904875/functions/strptime.html -> %y
    assert Month.parse("Oct 80", '%b %y') == Month(1980, 10)
    assert Month.parse("Feb 50", '%b %y') == Month(2050, 2)
    assert Month.parse("January 1999", '%B %Y') == Month(1999, 1)


def test_ord():
    assert Month(1970, 1).ord() == 0
    assert Month(1970, 2).ord() == 1
    assert Month(1970, 12).ord() == 11
    assert Month(1971, 1).ord() == 12
    assert Month(2000, 1).ord() == 360
    assert Month(2022, 9).ord() == 632
    assert Month(1969, 12).ord() == -1
    assert Month(1950, 1).ord() == -240


def test_from_ord():
    assert Month.from_ord(0) == Month(1970, 1)
    assert Month.from_ord(1) == Month(1970, 2)
    assert Month.from_ord(11) == Month(1970, 12)
    assert Month.from_ord(12) == Month(1971, 1)
    assert Month.from_ord(360) == Month(2000, 1)
    assert Month.from_ord(632) == Month(2022, 9)
    assert Month.from_ord(-1) == Month(1969, 12)
    assert Month.from_ord(-240) == Month(1950, 1)


def test_start_end_date():
    m1 = Month(2003, 1)
    assert m1.start_date == datetime.date(2003, 1, 1)
    assert m1.end_date == datetime.date(2003, 2, 1)

    m10 = Month(2022, 10)
    assert m10.start_date == datetime.date(2022, 10, 1)
    assert m10.end_date == datetime.date(2022, 11, 1)

    m12 = Month(1999, 12)
    assert m12.start_date == datetime.date(1999, 12, 1)
    assert m12.end_date == datetime.date(2000, 1, 1)


def test_last_date():
    assert Month(2003, 1).last_date == datetime.date(2003, 1, 31)
    assert Month(2003, 2).last_date == datetime.date(2003, 2, 28)
    assert Month(2008, 3).last_date == datetime.date(2008, 3, 31)
    assert Month(2022, 4).last_date == datetime.date(2022, 4, 30)
    assert Month(2030, 12).last_date == datetime.date(2030, 12, 31)

    # leap years
    assert Month(1600, 2).last_date == datetime.date(1600, 2, 29)
    assert Month(1700, 2).last_date == datetime.date(1700, 2, 28)
    assert Month(1800, 2).last_date == datetime.date(1800, 2, 28)
    assert Month(1900, 2).last_date == datetime.date(1900, 2, 28)
    assert Month(2000, 2).last_date == datetime.date(2000, 2, 29)
    assert Month(2004, 2).last_date == datetime.date(2004, 2, 29)
    assert Month(2096, 2).last_date == datetime.date(2096, 2, 29)
    assert Month(2100, 2).last_date == datetime.date(2100, 2, 28)


def test_days():
    assert Month(2022, 2).days() == 28
    assert Month(2022, 9).days() == 30
    assert Month(2022, 10).days() == 31
    assert [Month(2001, m).days() for m in range(1, 13)] == \
           [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    assert [Month(2004, m).days() for m in range(1, 13)] == \
           [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def test_len():
    for month in [Month(2022, 2), Month(2024, 2), Month(1998, 1), Month(2400, 4)]:
        assert month.days() == len(month)


def test_is_leap():
    def leaps(year_range: range) -> list[Month]:
        return [
            month
            for y in year_range
            for m in range(1, 13)
            if (month := Month(y, m)).is_leap()
        ]

    assert leaps(range(1996, 2016)) == [
        Month(1996, 2), Month(2000, 2), Month(2004, 2), Month(2008, 2), Month(2012, 2)
    ]

    assert leaps(range(2092, 2112)) == [
        Month(2092, 2), Month(2096, 2), Month(2104, 2), Month(2108, 2)
    ]

    assert leaps(range(800, 2800, 100)) == [
        Month(800, 2), Month(1200, 2), Month(1600, 2), Month(2000, 2), Month(2400, 2)
    ]


def test_iter():
    day_1, day_2, *_, day_30, day_31 = Month(2022, 1)
    assert day_1 == datetime.date(2022, 1, 1)
    assert day_2 == datetime.date(2022, 1, 2)
    assert day_30 == datetime.date(2022, 1, 30)
    assert day_31 == datetime.date(2022, 1, 31)

    days = list(Month(1985, 11))
    assert len(days) == 30
    for day, date_ in enumerate(days, start=1):
        assert date_.year == 1985
        assert date_.month == 11
        assert date_.day == day


def test_contains():
    assert datetime.date(2020, 9, 10) not in Month(2021, 9)
    assert datetime.date(2021, 8, 31) not in Month(2021, 9)
    assert datetime.date(2021, 9, 1) in Month(2021, 9)
    assert datetime.date(2021, 9, 15) in Month(2021, 9)
    assert datetime.date(2021, 9, 30) in Month(2021, 9)
    assert datetime.date(2021, 10, 1) not in Month(2021, 9)
    assert datetime.date(2022, 9, 10) not in Month(2021, 9)


def test_eq():
    assert Month(2022, 9) == Month(2022, 9)

    assert Month(2001, 1) == Month(2001, 1)
    assert Month(2001, 1) != Month(2001, 2)
    assert Month(2001, 1) != Month(2002, 1)
    assert Month(2001, 1) != Month(2002, 2)

    assert Month("2022-01") == Month(2022, 1)
    assert Month("2013-10") == Month(2013, 10)

    assert Month("2022-01") != "2022-01"
    assert Month(2001, 1) != (2001, 1)
    assert Month(2001, 1) != 15


def test_comparison():
    assert Month(2001, 3) < Month(2001, 4)
    assert Month(2001, 4) < Month(2001, 9)
    assert Month(2001, 9) < Month(2002, 1)
    assert Month(2001, 12) < Month(2002, 12)

    assert Month(2001, 4) > Month(2001, 1)
    assert Month(2001, 9) > Month(2001, 8)
    assert Month(2002, 1) > Month(2001, 10)
    assert Month(2002, 4) > Month(2001, 4)

    assert Month(2001, 1) <= Month(2001, 1)
    assert Month(2001, 1) >= Month(2001, 1)


def test_comparison_others():
    with pytest.raises(TypeError) as exc_info:
        _ = Month(2001, 1) > 3

    assert str(exc_info.value) == "'>' not supported between instances of 'Month' and 'int'"

    with pytest.raises(TypeError) as exc_info:
        _ = 3 > Month(2001, 1)

    assert str(exc_info.value) == "'>' not supported between instances of 'int' and 'Month'"


def test_hash():
    d = {Month(2001, 1): 144, Month(2001, 2): 180, Month(2001, 3): 333}
    assert d[Month(2001, 1)] == 144
    assert d[Month(2001, 2)] == 180
    assert d[Month(2001, 3)] == 333
    assert Month(2001, 4) not in d

    m1 = Month(2002, 1)
    m2 = Month(2002, 1)
    assert m1 is not m2
    assert hash(m1) == hash(m2)


def test_for_date():
    assert Month.for_date(datetime.date(2022, 9, 18)) == Month(2022, 9)
    assert Month.for_date(datetime.date(2001, 1, 1)) == Month(2001, 1)
    assert Month.for_date(datetime.date(2001, 1, 31)) == Month(2001, 1)
    assert Month.for_date(datetime.date(2001, 12, 31)) == Month(2001, 12)
    assert Month.for_date(datetime.date(2002, 1, 1)) == Month(2002, 1)


def test_today():
    with freeze_time("2013-03-28"):
        assert Month.today() == Month(2013, 3)

    with freeze_time("2038-12-31"):
        assert Month.today() == Month(2038, 12)

    with freeze_time("2039-01-01"):
        assert Month.today() == Month(2039, 1)


def test_add_monthdelta():
    assert Month(2022, 5) + MonthDelta(1) == Month(2022, 6)
    assert Month(2022, 12) + MonthDelta(1) == Month(2023, 1)
    assert Month(1998, 10) + MonthDelta(4) == Month(1999, 2)
    assert Month(1990, 1) + MonthDelta(-1) == Month(1989, 12)
    assert Month(1990, 1) + MonthDelta(-12) == Month(1989, 1)
    assert Month(2100, 1) + MonthDelta(0) == Month(2100, 1)

    assert MonthDelta(1) + Month(2001, 1) == Month(2001, 2)
    assert MonthDelta(-10) + Month(2001, 1) == Month(2000, 3)


def test_add_others():
    month = Month(2019, 1)
    for added in [1, Month(2021, 1), datetime.date(2022, 1, 1), datetime.timedelta(days=31), None]:
        with pytest.raises(TypeError) as exc_info_1:
            month + added
        assert str(exc_info_1.value).startswith("unsupported operand type(s) for +: 'Month' and '")

        with pytest.raises(TypeError) as exc_info_2:
            added + month
        assert str(exc_info_2.value).startswith("unsupported operand type(s) for +: '")
        assert str(exc_info_2.value).endswith("' and 'Month'")


def test_sub_monthdelta():
    assert Month(2022, 5) - MonthDelta(1) == Month(2022, 4)
    assert Month(2022, 5) - MonthDelta(5) == Month(2021, 12)
    assert Month(2022, 5) - MonthDelta(13) == Month(2021, 4)
    assert Month(1990, 1) - MonthDelta(1) == Month(1989, 12)
    assert Month(1990, 1) - MonthDelta(12) == Month(1989, 1)
    assert Month(1990, 1) - MonthDelta(-1) == Month(1990, 2)
    assert Month(1990, 1) - MonthDelta(0) == Month(1990, 1)


def test_sub_month():
    assert Month(2022, 5) - Month(2022, 4) == MonthDelta(1)
    assert Month(2022, 5) - Month(2022, 3) == MonthDelta(2)
    assert Month(2022, 5) - Month(2022, 1) == MonthDelta(4)
    assert Month(2022, 5) - Month(2021, 12) == MonthDelta(5)

    assert Month(1998, 1) - Month(1997, 10) == MonthDelta(3)
    assert Month(1998, 1) - Month(1997, 12) == MonthDelta(1)
    assert Month(1998, 1) - Month(1998, 1) == MonthDelta(0)
    assert Month(1998, 1) - Month(1998, 2) == MonthDelta(-1)
    assert Month(1998, 1) - Month(1998, 4) == MonthDelta(-3)

    assert Month(2100, 1) - Month(1900, 1) == MonthDelta(2400)


def test_sub_others():
    month = Month(2019, 1)
    for subtraction in [0, 1, datetime.date(2022, 1, 1), datetime.timedelta(days=31), None]:
        with pytest.raises(TypeError) as exc_info:
            month - subtraction
        assert str(exc_info.value).startswith("unsupported operand type(s) for -: 'Month' and '")

    for subtracted in [0, 1, MonthDelta(1), datetime.date(2022, 1, 1), datetime.timedelta(days=31), None]:
        with pytest.raises(TypeError) as exc_info:
            subtracted - month
        assert str(exc_info.value).startswith("unsupported operand type(s) for -: '")
        assert str(exc_info.value).endswith("' and 'Month'")
