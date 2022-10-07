import datetime

import pytest

from calendarium import week
from calendarium.week import Week
from calendarium.week import weeks_count
from calendarium.week_range import WeekRange


def test_init():
    # start + end
    wr1 = WeekRange(Week(2010, 2), Week(2010, 6))
    assert wr1.start_week == Week(2010, 2)
    assert wr1.last_week == Week(2010, 5)
    assert wr1.end_week == Week(2010, 6)
    assert wr1.duration == datetime.timedelta(weeks=4)
    # start + duration
    wr2 = WeekRange(start_week=Week(2002, 50), duration=datetime.timedelta(weeks=6))
    assert wr2.start_week == Week(2002, 50)
    assert wr2.last_week == Week(2003, 3)
    assert wr2.end_week == Week(2003, 4)
    assert wr2.duration == datetime.timedelta(weeks=6)
    # end + duration
    wr3 = WeekRange(end_week=Week(2030, 18), duration=datetime.timedelta(weeks=2))
    assert wr3.start_week == Week(2030, 16)
    assert wr3.last_week == Week(2030, 17)
    assert wr3.end_week == Week(2030, 18)
    assert wr3.duration == datetime.timedelta(weeks=2)
    # start + end + duration
    wr4 = WeekRange(Week(2020, 1), Week(2021, 1), duration=datetime.timedelta(weeks=53))
    assert wr4.start_week == Week(2020, 1)
    assert wr4.last_week == Week(2020, 53)
    assert wr4.end_week == Week(2021, 1)
    assert wr4.duration == datetime.timedelta(weeks=53)

    # start can be after end
    wr5 = WeekRange(Week(2018, 30), Week(2018, 22))
    assert wr5.start_week == Week(2018, 30)
    assert wr5.last_week == Week(2018, 21)
    assert wr5.end_week == Week(2018, 22)
    assert wr5.duration == datetime.timedelta(0)

    wr6 = WeekRange(start_week=Week(2033, 30), weeks=-1)
    assert wr6.start_week == Week(2033, 30)
    assert wr6.end_week == Week(2033, 29)
    assert wr6.duration == datetime.timedelta(0)


def test_init_first_weekday_override():
    # monday -> sunday
    wr1 = WeekRange(Week(2017, 20), Week(2017, 25), first_weekday=week.SUNDAY)
    assert wr1.start_week == Week(2017, 20, week.SUNDAY)
    assert wr1.last_week == Week(2017, 24, week.SUNDAY)
    assert wr1.end_week == Week(2017, 25, week.SUNDAY)
    assert wr1.duration == datetime.timedelta(weeks=5)

    # no override here!
    wr2 = WeekRange(Week(2000, 30, week.SUNDAY), Week(2001, 10, week.SUNDAY))
    assert wr2.start_week == Week(2000, 30, week.SUNDAY)
    assert wr2.last_week == Week(2001, 9, week.SUNDAY)
    assert wr2.end_week == Week(2001, 10, week.SUNDAY)
    assert wr2.duration == datetime.timedelta(weeks=32)

    # sunday -> monday
    wr2 = WeekRange(
        Week(2000, 30, week.SUNDAY), Week(2001, 10, week.SUNDAY), first_weekday=week.MONDAY
    )
    assert wr2.start_week == Week(2000, 30)
    assert wr2.last_week == Week(2001, 9)
    assert wr2.end_week == Week(2001, 10)
    assert wr2.duration == datetime.timedelta(weeks=32)


def test_init_alt():
    wr1 = WeekRange("2022-W01", "2022-W05")
    assert wr1.start_week == Week(2022, 1)
    assert wr1.last_week == Week(2022, 4)
    assert wr1.end_week == Week(2022, 5)
    assert wr1.duration == datetime.timedelta(weeks=4)

    wr2 = WeekRange((1998, 5), (2000, 16))
    assert wr2.start_week == Week(1998, 5)
    assert wr2.last_week == Week(2000, 15)
    assert wr2.end_week == Week(2000, 16)
    assert wr2.duration == datetime.timedelta(weeks=116)

    wr3 = WeekRange("2010-W30", weeks=3)
    assert wr3.start_week == Week(2010, 30)
    assert wr3.last_week == Week(2010, 32)
    assert wr3.end_week == Week(2010, 33)
    assert wr3.duration == datetime.timedelta(weeks=3)

    wr4 = WeekRange(end_week=(2008, 16), weeks=16)
    assert wr4.start_week == Week(2007, 52)
    assert wr4.last_week == Week(2008, 15)
    assert wr4.end_week == Week(2008, 16)
    assert wr4.duration == datetime.timedelta(weeks=16)


def test_init_alt_sunday():
    wr1 = WeekRange("2020-W04", "2020-W10", first_weekday=week.SUNDAY)
    assert wr1.start_week == Week(2020, 4, week.SUNDAY)
    assert wr1.last_week == Week(2020, 9, week.SUNDAY)
    assert wr1.end_week == Week(2020, 10, week.SUNDAY)
    assert wr1.duration == datetime.timedelta(weeks=6)

    wr2 = WeekRange((1998, 5), (2000, 16), first_weekday=week.SUNDAY)
    assert wr2.start_week == Week(1998, 5, week.SUNDAY)
    assert wr2.last_week == Week(2000, 15, week.SUNDAY)
    assert wr2.end_week == Week(2000, 16, week.SUNDAY)
    assert wr2.duration == datetime.timedelta(weeks=115)

    wr3 = WeekRange("2010-W30", weeks=3, first_weekday=week.SUNDAY)
    assert wr3.start_week == Week(2010, 30, week.SUNDAY)
    assert wr3.last_week == Week(2010, 32, week.SUNDAY)
    assert wr3.end_week == Week(2010, 33, week.SUNDAY)
    assert wr3.duration == datetime.timedelta(weeks=3)

    wr4 = WeekRange(end_week=(2008, 16), weeks=16, first_weekday=week.SUNDAY)
    assert wr4.start_week == Week(2007, 52, week.SUNDAY)
    assert wr4.last_week == Week(2008, 15, week.SUNDAY)
    assert wr4.end_week == Week(2008, 16, week.SUNDAY)
    assert wr4.duration == datetime.timedelta(weeks=16)


def test_init_duration_rounding():
    wr1 = WeekRange(start_week=Week(2022, 1), duration=datetime.timedelta(days=10))
    assert wr1.start_week == Week(2022, 1)
    assert wr1.end_week == Week(2022, 2)
    assert wr1.duration == datetime.timedelta(weeks=1)

    wr2 = WeekRange(end_week=Week(2013, 20), duration=datetime.timedelta(days=20))
    assert wr2.start_week == Week(2013, 17)
    assert wr2.end_week == Week(2013, 20)
    assert wr2.duration == datetime.timedelta(weeks=3)


def test_init_invalid():
    # only start
    with pytest.raises(TypeError) as exc_info:
        WeekRange(Week(2010, 1))
    assert str(exc_info.value) == "too few arguments specified for WeekRange"
    # only end
    with pytest.raises(TypeError):
        WeekRange(end_week=Week(1999, 44))
    # only duration
    with pytest.raises(TypeError):
        WeekRange(duration=datetime.timedelta(weeks=5))
    with pytest.raises(TypeError):
        WeekRange(weeks=4)
    # no args
    with pytest.raises(TypeError) as exc_info:
        WeekRange()
    assert str(exc_info.value) == "too few arguments specified for WeekRange"

    # start + end + duration nonmatching
    with pytest.raises(ValueError) as exc_info:
        WeekRange(Week(2000, 1), Week(2000, 5), datetime.timedelta(weeks=2))
    assert str(exc_info.value) == (
        "duration mismatch: expected 28 days, 0:00:00, got 14 days, 0:00:00"
    )

    # first weekday override can cause illegal week number
    assert weeks_count(1998) == 53
    assert weeks_count(1998, week.SUNDAY) == 52
    WeekRange(Week(1997, 52), Week(1998, 53))  # ok
    with pytest.raises(ValueError) as exc_info:
        WeekRange(Week(1997, 52), Week(1998, 53), first_weekday=week.SUNDAY)  # not ok
    assert str(exc_info.value) == "year 1998 has only 52 weeks"


def test_repr():
    assert repr(WeekRange((2022, 1), (2023, 10))) == 'WeekRange(Week(2022, 1), Week(2023, 10))'
    assert repr(WeekRange((1998, 52), (1998, 48))) == 'WeekRange(Week(1998, 52), Week(1998, 48))'
    assert repr(WeekRange((2003, 3), (2003, 6), first_weekday=week.SUNDAY)) == \
           'WeekRange(Week(2003, 3, SUNDAY), Week(2003, 6, SUNDAY))'


def test_str():
    assert str(WeekRange(Week(1999, 1), Week(2000, 10))) == "1999-W01/2000-W10"
    assert str(WeekRange.for_iso_year(2013)) == "2013-W01/2014-W01"
    assert str(WeekRange((2040, 1), (2039, 52))) == "2040-W01/2039-W52"


def test_format():
    wr = WeekRange((1999, 52), (2000, 3))
    assert format(wr) == "1999-W52/2000-W03"
    assert format(wr, "%G-W%V/") == "1999-W52/2000-W03"
    assert format(wr, "week %V/%g: .. ") == "week 52/99 .. week 03/00"
    assert format(wr, "[W|%V|%G]:->") == "[W|52|1999]->[W|03|2000]"


def test_from_str():
    assert WeekRange.from_str("1999-W52/2000-W03") == WeekRange((1999, 52), (2000, 3))
    assert WeekRange.from_str("2040-W01/2042-W13") == WeekRange((2040, 1), (2042, 13))
    assert WeekRange.from_str("1999-W52/2000-W03", first_weekday=week.SUNDAY) == WeekRange(
        Week(1999, 52, week.SUNDAY), Week(2000, 3, week.SUNDAY)
    )


def test_parse():
    assert WeekRange.parse("1999-W52/2000-W03") == WeekRange((1999, 52), (2000, 3))
    # datetime.datetime.strptime doesn't support %g for parsing!
    assert WeekRange.parse("t13/2044 .. t18/2045", "t%V/%G: .. ") == \
           WeekRange((2044, 13), (2045, 18))
    assert WeekRange.parse("[W|01|2013]->[W|09|2014]", "[W|%V|%G]:->") == \
           WeekRange((2013, 1), (2014, 9))


def test_start_end_last_date():
    wr1 = WeekRange((2011, 38), (2013, 4))
    assert wr1.start_date == datetime.date(2011, 9, 19)
    assert wr1.end_date == datetime.date(2013, 1, 21)
    assert wr1.last_date == datetime.date(2013, 1, 20)

    wr2 = WeekRange((1998, 1), (1998, 2))
    assert wr2.start_date == datetime.date(1997, 12, 29)
    assert wr2.end_date == datetime.date(1998, 1, 5)
    assert wr2.last_date == datetime.date(1998, 1, 4)

    wr3 = WeekRange((2022, 30), (2024, 1), first_weekday=week.SUNDAY)
    assert wr3.start_week == Week(2022, 30, week.SUNDAY)
    assert wr3.start_date == datetime.date(2022, 7, 24)
    assert wr3.end_week == Week(2024, 1, week.SUNDAY)
    assert wr3.end_date == datetime.date(2023, 12, 31)
    assert wr3.last_date == datetime.date(2023, 12, 30)


def test_eq():
    wr1 = WeekRange(Week(2022, 3), weeks=4)
    wr2 = WeekRange(Week(2022, 3), Week(2022, 7))
    assert wr1 is not wr2
    assert wr1 == wr2

    assert WeekRange((2001, 40), (2002, 10)) == WeekRange(Week(2001, 40), weeks=22)
    assert WeekRange((2000, 40), (2002, 10)) != WeekRange(Week(2001, 40), weeks=22)
    assert WeekRange((2001, 41), (2002, 10)) != WeekRange(Week(2001, 40), weeks=22)
    assert WeekRange((2001, 40), (2003, 10)) != WeekRange(Week(2001, 40), weeks=22)
    assert WeekRange((2001, 40), (2002, 11)) != WeekRange(Week(2001, 40), weeks=22)
    assert WeekRange((2001, 40), (2002, 10)) != WeekRange(Week(2001, 41), weeks=22)
    assert WeekRange((2001, 40), (2002, 10)) != WeekRange(Week(2001, 40), weeks=23)

    assert WeekRange((2001, 40), (2002, 10), first_weekday=week.SUNDAY) != \
           WeekRange(Week(2001, 40), weeks=22)
    assert WeekRange((2001, 40), (2002, 10)) != WeekRange(Week(2001, 40, week.SUNDAY), weeks=22)
    assert WeekRange((2001, 40), (2002, 10), first_weekday=week.SUNDAY) == \
           WeekRange(Week(2001, 40, week.SUNDAY), weeks=22)

    assert WeekRange("2020-W02", "2020-W05") == WeekRange((2020, 2), (2020, 5))
    assert WeekRange("2020-W02", "2020-W05") != Week(2020, 2)
    assert WeekRange("2020-W02", "2020-W05") != "2020-W02..2020-W05"
    assert WeekRange("2020-W02", "2020-W05") != 20

    # all empty ranges are equal
    assert WeekRange((2000, 1), (2000, 1)) == WeekRange((2004, 30), (2004, 30))
    assert WeekRange((1999, 28), (1999, 20)) == WeekRange((2099, 1), weeks=0)


def test_len():
    assert len(WeekRange((2001, 10), (2001, 13))) == 3
    assert len(WeekRange((2001, 10), (2001, 13), first_weekday=week.SUNDAY)) == 3
    assert len(WeekRange((2004, 30), (2005, 30))) == 53
    assert len(WeekRange.for_iso_year(2000)) == 52
    assert len(WeekRange((1990, 4), weeks=123)) == 123
    assert len(WeekRange((1900, 1), (1900, 1))) == 0
    assert len(WeekRange((1901, 2), (1900, 1))) == 0


def test_iter():
    wr = WeekRange((2001, 51), (2002, 4))
    g = iter(wr)
    assert next(g) == Week(2001, 51)
    assert next(g) == Week(2001, 52)
    assert next(g) == Week(2002, 1)
    assert next(g) == Week(2002, 2)
    assert next(g) == Week(2002, 3)
    with pytest.raises(StopIteration):
        next(g)

    assert list(WeekRange((1990, 4), (1990, 7))) == [Week(1990, 4), Week(1990, 5), Week(1990, 6)]
    assert list(WeekRange((1990, 4), (1990, 4))) == []
    assert list(WeekRange((1990, 4), (1990, 1))) == []


def test_iter_sunday():
    wr = WeekRange((2003, 50), (2004, 3), first_weekday=week.SUNDAY)
    g = iter(wr)
    assert next(g) == Week(2003, 50, week.SUNDAY)
    assert next(g) == Week(2003, 51, week.SUNDAY)
    assert next(g) == Week(2003, 52, week.SUNDAY)
    assert next(g) == Week(2003, 53, week.SUNDAY)
    assert next(g) == Week(2004, 1, week.SUNDAY)
    assert next(g) == Week(2004, 2, week.SUNDAY)
    with pytest.raises(StopIteration):
        next(g)

    assert list(WeekRange(Week(2020, 39, week.SUNDAY), Week(2020, 42, week.SUNDAY))) == [
        Week(2020, 39, week.SUNDAY), Week(2020, 40, week.SUNDAY), Week(2020, 41, week.SUNDAY)
    ]


def test_dates():
    dates = list(WeekRange((2000, 20), weeks=2).dates())
    assert len(dates) == 14
    assert dates[:2] == [datetime.date(2000, 5, 15), datetime.date(2000, 5, 16)]
    assert dates[-2:] == [datetime.date(2000, 5, 27), datetime.date(2000, 5, 28)]

    dates_sun = list(WeekRange((2005, 13), (2005, 16), first_weekday=week.SUNDAY).dates())
    assert len(dates_sun) == 21
    assert dates_sun[:2] == [datetime.date(2005, 3, 27), datetime.date(2005, 3, 28)]
    assert dates_sun[-2:] == [datetime.date(2005, 4, 15), datetime.date(2005, 4, 16)]


def test_total_days():
    assert WeekRange((2010, 1), weeks=1).total_days() == 7
    assert WeekRange((2010, 1), weeks=10).total_days() == 70
    assert WeekRange((2010, 1), weeks=100).total_days() == 700

    assert weeks_count(1997) == 52
    assert WeekRange.for_iso_year(1997).total_days() == 364
    assert weeks_count(1998) == 53
    assert WeekRange.for_iso_year(1998).total_days() == 371
    assert weeks_count(1997, week.SUNDAY) == 53
    assert WeekRange.for_iso_year(1997, first_weekday=week.SUNDAY).total_days() == 371
    assert weeks_count(1998, week.SUNDAY) == 52
    assert WeekRange.for_iso_year(1998, first_weekday=week.SUNDAY).total_days() == 364


def test_contains():
    wr = WeekRange((2005, 40), (2006, 18))

    assert (2005, 1) not in wr
    assert (2005, 10) not in wr
    assert (2005, 39) not in wr
    assert (2005, 40) in wr
    assert (2005, 41) in wr
    assert (2005, 52) in wr
    assert (2006, 1) in wr
    assert (2006, 2) in wr
    assert (2006, 16) in wr
    assert (2006, 17) in wr
    assert (2006, 18) not in wr
    assert (2006, 19) not in wr
    assert (2006, 41) not in wr

    assert Week(2005, 39) not in wr
    assert Week(2005, 40) in wr
    assert Week(2006, 1) in wr
    assert Week(2006, 10) in wr
    assert Week(2006, 20) not in wr

    assert "2005-W30" not in wr
    assert "2005-W50" in wr
    assert "2005-W52" in wr
    assert "2006-W01" in wr
    assert "2006-W04" in wr
    assert "2006-W16" in wr
    assert "2006-W23" not in wr

    assert "2006-01" not in wr
    assert "apples" not in wr
    assert 1453 not in wr

    assert wr.start_date == datetime.date(2005, 10, 3)
    assert wr.end_date == datetime.date(2006, 5, 1)
    assert datetime.date(2005, 10, 2) not in wr
    assert datetime.date(2005, 10, 3) in wr
    assert datetime.date(2006, 4, 30) in wr
    assert datetime.date(2006, 5, 1) not in wr

    wr_empty = WeekRange((2000, 1), (2000, 1))
    assert Week(2000, 1) not in wr_empty
    assert wr_empty.start_date == datetime.date(2000, 1, 3)
    assert datetime.date(2000, 1, 3) not in wr_empty

    # TODO: Week(..., ..., SUNDAY) in WeekRange(..., ..., SUNDAY) ??


def test_add():
    assert WeekRange((2020, 1), (2020, 5)) + datetime.timedelta(weeks=1) == \
           WeekRange((2020, 2), (2020, 6))
    assert WeekRange((1995, 40), weeks=13) + datetime.timedelta(weeks=20) == \
           WeekRange((1996, 8), weeks=13)
    assert datetime.timedelta(weeks=4) + WeekRange((2022, 33), weeks=3) == \
           WeekRange((2022, 37), weeks=3)


def test_bool():
    assert WeekRange((2000, 40), (2001, 10))
    assert WeekRange((2000, 1), (2000, 2))
    assert not WeekRange((2000, 1), (2000, 1))
    assert not WeekRange((2000, 1), (1999, 52))


def test_hash():
    d = dict()
    d[WeekRange((2020, 1), weeks=2)] = 'AAA'
    d[WeekRange((2020, 1), weeks=3)] = 'BBB'
    d[WeekRange((2020, 2), weeks=2)] = 'CCC'
    d[WeekRange((2020, 1), (2020, 3))] = 'AAA+'  # overwrite
    assert d == {
        WeekRange((2020, 1), (2020, 3)): 'AAA+',
        WeekRange((2020, 1), (2020, 4)): 'BBB',
        WeekRange((2020, 2), (2020, 4)): 'CCC',
    }


def test_for_iso_year():
    assert weeks_count(1997) == 52
    wr_1997_mon = WeekRange.for_iso_year(1997)
    assert wr_1997_mon.start_week == Week(1997, 1)
    assert wr_1997_mon.last_week == Week(1997, 52)
    assert wr_1997_mon.end_week == Week(1998, 1)
    assert wr_1997_mon.start_date == datetime.date(1996, 12, 30)
    assert wr_1997_mon.last_date == datetime.date(1997, 12, 28)
    assert wr_1997_mon.end_date == datetime.date(1997, 12, 29)
    assert wr_1997_mon.duration == datetime.timedelta(weeks=52)

    assert weeks_count(1998) == 53
    wr_1998_mon = WeekRange.for_iso_year(1998)
    assert wr_1998_mon.start_week == Week(1998, 1)
    assert wr_1998_mon.last_week == Week(1998, 53)
    assert wr_1998_mon.end_week == Week(1999, 1)
    assert wr_1998_mon.start_date == datetime.date(1997, 12, 29)
    assert wr_1998_mon.last_date == datetime.date(1999, 1, 3)
    assert wr_1998_mon.end_date == datetime.date(1999, 1, 4)
    assert wr_1998_mon.duration == datetime.timedelta(weeks=53)

    assert weeks_count(1997, week.SUNDAY) == 53
    wr_1997_sun = WeekRange.for_iso_year(1997, week.SUNDAY)
    assert wr_1997_sun.start_week == Week(1997, 1, week.SUNDAY)
    assert wr_1997_sun.last_week == Week(1997, 53, week.SUNDAY)
    assert wr_1997_sun.end_week == Week(1998, 1, week.SUNDAY)
    assert wr_1997_sun.start_date == datetime.date(1996, 12, 29)
    assert wr_1997_sun.last_date == datetime.date(1998, 1, 3)
    assert wr_1997_sun.end_date == datetime.date(1998, 1, 4)
    assert wr_1997_sun.duration == datetime.timedelta(weeks=53)

    assert weeks_count(1998, week.SUNDAY) == 52
    wr_1998_sun = WeekRange.for_iso_year(1998, week.SUNDAY)
    assert wr_1998_sun.start_week == Week(1998, 1, week.SUNDAY)
    assert wr_1998_sun.last_week == Week(1998, 52, week.SUNDAY)
    assert wr_1998_sun.end_week == Week(1999, 1, week.SUNDAY)
    assert wr_1998_sun.start_date == datetime.date(1998, 1, 4)
    assert wr_1998_sun.last_date == datetime.date(1999, 1, 2)
    assert wr_1998_sun.end_date == datetime.date(1999, 1, 3)
    assert wr_1998_sun.duration == datetime.timedelta(weeks=52)


def test_for_year():
    # year 2001 starts on MONDAY
    assert datetime.date(2001, 1, 1).weekday() == week.MONDAY
    # 2001-01-01 is also start of the iso week 2001-W01
    assert Week(2001, 1).start_date == datetime.date(2001, 1, 1)
    # last day of 2001 is MONDAY
    assert datetime.date(2001, 12, 31).weekday() == week.MONDAY
    # ... which is also the start of iso week 2002-W01
    assert Week(2002, 1).start_date == datetime.date(2001, 12, 31)
    # => year 2001 contains iso weeks 2001-W01 through 2002-W02 (excl.)
    wr_2001 = WeekRange.for_year(2001)
    assert wr_2001.start_week == Week(2001, 1)
    assert wr_2001.last_week == Week(2002, 1)
    assert wr_2001.end_week == Week(2002, 2)

    # year 2010 starts on FRIDAY
    assert datetime.date(2010, 1, 1).weekday() == week.FRIDAY
    # first MONDAY of 2010 is thus 2010-01-04 == start of the iso week 2010-W01
    assert datetime.date(2010, 1, 4).weekday() == week.MONDAY
    assert Week(2010, 1).start_date == datetime.date(2010, 1, 4)
    # last day of year 2010 is FRIDAY
    assert datetime.date(2010, 12, 31).weekday() == week.FRIDAY
    # first MONDAY of 2011 is thus 2011-01-03 = start of the iso week 2011-W01
    assert datetime.date(2011, 1, 3).weekday() == week.MONDAY
    assert Week(2011, 1).start_date == datetime.date(2011, 1, 3)
    # => year 2010 contains iso weeks 2010-W01 through 2011-W01 (excl.)
    wr_2010 = WeekRange.for_year(2010)
    assert wr_2010.start_week == Week(2010, 1)
    assert wr_2010.last_week == Week(2010, 52)
    assert wr_2010.end_week == Week(2011, 1)

    # year 2013 starts on TUESDAY
    assert datetime.date(2013, 1, 1).weekday() == week.TUESDAY
    # first MONDAY of 2013 is thus 2013-01-07 == start of the iso week 2013-W02
    assert datetime.date(2013, 1, 7).weekday() == week.MONDAY
    assert Week(2013, 2).start_date == datetime.date(2013, 1, 7)
    # last day of 2013 is TUESDAY
    assert datetime.date(2013, 12, 31).weekday() == week.TUESDAY
    # first MONDAY of 2014 is thus 2014-01-06 == start of the iso week 2014-W02
    assert datetime.date(2014, 1, 6).weekday() == week.MONDAY
    assert Week(2014, 2).start_date == datetime.date(2014, 1, 6)
    # => year 2013 contains iso weeks 2013-W02 through 2014-W02 (excl.)
    wr_2013 = WeekRange.for_year(2013)
    assert wr_2013.start_week == Week(2013, 2)
    assert wr_2013.last_week == Week(2014, 1)
    assert wr_2013.end_week == Week(2014, 2)

    # TODO: default args start_with_full=True, end_with_full=False
    # TODO: leap years?
    # TODO: start with sunday


def test_following():
    wr1 = WeekRange((2000, 41), (2000, 45))
    assert (wr2 := wr1.following()) == WeekRange((2000, 45), (2000, 49))
    assert (wr3 := wr2.following()) == WeekRange((2000, 49), (2001, 1))
    assert wr3.following() == WeekRange((2001, 1), (2001, 5))

    wr4 = WeekRange((1990, 20), weeks=40)
    assert (wr5 := wr4.following()) == WeekRange((1991, 8), (1991, 48))
    assert (wr6 := wr5.following()) == WeekRange((1991, 48), (1992, 36))
    assert wr6.following() == WeekRange((1992, 36), (1993, 23))

    empty_following = WeekRange((1990, 20), weeks=0).following()
    assert not empty_following
    assert empty_following.start_week == empty_following.end_week == Week(1990, 20)

    neg_following = WeekRange((2040, 8), (2040, 6)).following()
    assert not neg_following
    assert neg_following.start_week == Week(2040, 6)
    assert neg_following.end_week == Week(2040, 4)


def test_preceding():
    wr1 = WeekRange((2000, 10), (2000, 15))
    assert (wr2 := wr1.preceding()) == WeekRange((2000, 5), (2000, 10))
    assert (wr3 := wr2.preceding()) == WeekRange((1999, 52), (2000, 5))
    assert wr3.preceding() == WeekRange((1999, 47), (1999, 52))

    wr4 = WeekRange((1990, 20), weeks=40)
    assert (wr5 := wr4.preceding()) == WeekRange((1989, 32), (1990, 20))
    assert (wr6 := wr5.preceding()) == WeekRange((1988, 44), (1989, 32))
    assert wr6.preceding() == WeekRange((1988, 4), (1988, 44))

    empty_preceding = WeekRange((1990, 20), weeks=0).preceding()
    assert not empty_preceding
    assert empty_preceding.start_week == empty_preceding.end_week == Week(1990, 20)

    neg_preceding = WeekRange((2040, 8), (2040, 6)).preceding()
    assert not neg_preceding
    assert neg_preceding.start_week == Week(2040, 10)
    assert neg_preceding.end_week == Week(2040, 8)
