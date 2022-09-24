import calendar
import datetime

import pytest
from freezegun import freeze_time

from calendarium import week
from calendarium.week import first_week_offset
from calendarium.week import Week
from calendarium.week import weeks_count


def test_first_week_offset_monday():
    # first weekday = MONDAY
    # Mon: 2010-01-04, 2016-01-04 -> W01 starts (Y)-01-04 -> offset = 3
    assert first_week_offset(2010) == 3
    assert first_week_offset(2016) == 3
    # Tue: 2005-01-04, 2000-01-04 -> W01 starts (Y)-01-03 -> offset = 2
    assert first_week_offset(2005) == 2
    assert first_week_offset(2000) == 2
    # Wed: 2006-01-04, 2012-01-04 -> W01 starts (Y)-01-02 -> offset = 1
    assert first_week_offset(2006) == 1
    assert first_week_offset(2012) == 1
    # Thu: 2001-01-04, 2024-01-04 -> W01 starts (Y)-01-01 -> offset = 0
    assert first_week_offset(2001) == 0
    assert first_week_offset(2024) == 0
    # Fri: 2002-01-04, 2008-01-04 -> W01 starts (Y-1)-12-31 -> offset = -1
    assert first_week_offset(2002) == -1
    assert first_week_offset(2008) == -1
    # Sat: 2003-01-04, 2020-01-04 -> W01 starts (Y-1)-12-30 -> offset = -2
    assert first_week_offset(2003) == -2
    assert first_week_offset(2020) == -2
    # Sun: 2009-01-04, 2004-01-04 -> W01 starts (Y-1)-12-29 -> offset = -3
    assert first_week_offset(2009) == -3
    assert first_week_offset(2004) == -3


def test_first_week_offset_sunday():
    # first weekday = SUNDAY
    # Sun: 2009-01-04, 2004-01-04 -> W01 starts (Y)-01-04 -> offset = 3
    assert first_week_offset(2009, week.SUNDAY) == 3
    assert first_week_offset(2004, week.SUNDAY) == 3
    # Mon: 2010-01-04, 2016-01-04 -> W01 starts (Y)-01-03 -> offset = 2
    assert first_week_offset(2010, week.SUNDAY) == 2
    assert first_week_offset(2016, week.SUNDAY) == 2
    # Tue: 2005-01-04, 2000-01-04 -> W01 starts (Y)-01-02 -> offset = 1
    assert first_week_offset(2005, week.SUNDAY) == 1
    assert first_week_offset(2000, week.SUNDAY) == 1
    # Wed: 2006-01-04, 2012-01-04 -> W01 starts (Y)-01-01 -> offset = 0
    assert first_week_offset(2006, week.SUNDAY) == 0
    assert first_week_offset(2012, week.SUNDAY) == 0
    # Thu: 2001-01-04, 2024-01-04 -> W01 starts (Y-1)-12-31 -> offset = -1
    assert first_week_offset(2001, week.SUNDAY) == -1
    assert first_week_offset(2024, week.SUNDAY) == -1
    # Fri: 2002-01-04, 2008-01-04 -> W01 starts (Y-1)-12-30 -> offset = -2
    assert first_week_offset(2002, week.SUNDAY) == -2
    assert first_week_offset(2008, week.SUNDAY) == -2
    # Sat: 2003-01-04, 2020-01-04 -> W01 starts (Y-1)-12-29 -> offset = -3
    assert first_week_offset(2003, week.SUNDAY) == -3
    assert first_week_offset(2020, week.SUNDAY) == -3


def test_init_starting_monday():
    wm_2022_01 = Week(2022, 1)
    assert wm_2022_01.start_date == datetime.date(2022, 1, 3)
    assert wm_2022_01.last_date == datetime.date(2022, 1, 9)
    assert wm_2022_01.end_date == datetime.date(2022, 1, 10)
    assert wm_2022_01.first_weekday == week.MONDAY

    wm_2022_02 = Week(2022, 2)
    assert wm_2022_02.start_date == datetime.date(2022, 1, 10)
    assert wm_2022_02.last_date == datetime.date(2022, 1, 16)
    assert wm_2022_02.end_date == datetime.date(2022, 1, 17)
    assert wm_2022_02.first_weekday == week.MONDAY

    wm_2022_12 = Week(2022, 12)
    assert wm_2022_12.start_date == datetime.date(2022, 3, 21)
    assert wm_2022_12.last_date == datetime.date(2022, 3, 27)
    assert wm_2022_12.end_date == datetime.date(2022, 3, 28)
    assert wm_2022_12.first_weekday == week.MONDAY

    wm_2015_01 = Week(2015, 1)
    assert wm_2015_01.start_date == datetime.date(2014, 12, 29)
    assert wm_2015_01.last_date == datetime.date(2015, 1, 4)
    assert wm_2015_01.end_date == datetime.date(2015, 1, 5)
    assert wm_2015_01.first_weekday == week.MONDAY

    wm_2015_30 = Week(2015, 30)
    assert wm_2015_30.start_date == datetime.date(2015, 7, 20)
    assert wm_2015_30.last_date == datetime.date(2015, 7, 26)
    assert wm_2015_30.end_date == datetime.date(2015, 7, 27)
    assert wm_2015_30.first_weekday == week.MONDAY

    wm_2015_52 = Week(2015, 52)
    assert wm_2015_52.start_date == datetime.date(2015, 12, 21)
    assert wm_2015_52.last_date == datetime.date(2015, 12, 27)
    assert wm_2015_52.end_date == datetime.date(2015, 12, 28)
    assert wm_2015_52.first_weekday == week.MONDAY

    wm_2015_53 = Week(2015, 53)
    assert wm_2015_53.start_date == datetime.date(2015, 12, 28)
    assert wm_2015_53.last_date == datetime.date(2016, 1, 3)
    assert wm_2015_53.end_date == datetime.date(2016, 1, 4)
    assert wm_2015_53.first_weekday == week.MONDAY

    wm_2016_01 = Week(2016, 1)
    assert wm_2016_01.start_date == datetime.date(2016, 1, 4)
    assert wm_2016_01.last_date == datetime.date(2016, 1, 10)
    assert wm_2016_01.end_date == datetime.date(2016, 1, 11)
    assert wm_2016_01.first_weekday == week.MONDAY

    assert [Week(year, 1).start_date for year in range(2000, 2020)] == [
        datetime.date(2000, 1, 3),
        datetime.date(2001, 1, 1),
        datetime.date(2001, 12, 31),  # 2002
        datetime.date(2002, 12, 30),  # 2003
        datetime.date(2003, 12, 29),  # 2004
        datetime.date(2005, 1, 3),
        datetime.date(2006, 1, 2),
        datetime.date(2007, 1, 1),
        datetime.date(2007, 12, 31),  # 2008
        datetime.date(2008, 12, 29),  # 2009
        datetime.date(2010, 1, 4),
        datetime.date(2011, 1, 3),
        datetime.date(2012, 1, 2),
        datetime.date(2012, 12, 31),  # 2013
        datetime.date(2013, 12, 30),  # 2014
        datetime.date(2014, 12, 29),  # 2015
        datetime.date(2016, 1, 4),
        datetime.date(2017, 1, 2),
        datetime.date(2018, 1, 1),
        datetime.date(2018, 12, 31),  # 2019
    ]


def test_init_starting_sunday():
    ws_2022_1 = Week(2022, 1, first_weekday=week.SUNDAY)
    assert ws_2022_1.start_date == datetime.date(2022, 1, 2)
    assert ws_2022_1.last_date == datetime.date(2022, 1, 8)
    assert ws_2022_1.end_date == datetime.date(2022, 1, 9)
    assert ws_2022_1.first_weekday == week.SUNDAY

    ws_2015_01 = Week(2015, 1, first_weekday=week.SUNDAY)
    assert ws_2015_01.start_date == datetime.date(2015, 1, 4)
    assert ws_2015_01.last_date == datetime.date(2015, 1, 10)
    assert ws_2015_01.end_date == datetime.date(2015, 1, 11)
    assert ws_2015_01.first_weekday == week.SUNDAY

    ws_2015_30 = Week(2015, 30, first_weekday=week.SUNDAY)
    assert ws_2015_30.start_date == datetime.date(2015, 7, 26)
    assert ws_2015_30.last_date == datetime.date(2015, 8, 1)
    assert ws_2015_30.end_date == datetime.date(2015, 8, 2)
    assert ws_2015_30.first_weekday == week.SUNDAY

    ws_2015_52 = Week(2015, 52, first_weekday=week.SUNDAY)
    assert ws_2015_52.start_date == datetime.date(2015, 12, 27)
    assert ws_2015_52.last_date == datetime.date(2016, 1, 2)
    assert ws_2015_52.end_date == datetime.date(2016, 1, 3)
    assert ws_2015_52.first_weekday == week.SUNDAY

    with pytest.raises(ValueError) as exc_info:
        Week(2015, 53, first_weekday=week.SUNDAY)
    assert str(exc_info.value) == "year 2015 has only 52 weeks"

    ws_2016_01 = Week(2016, 1, first_weekday=week.SUNDAY)
    assert ws_2016_01.start_date == datetime.date(2016, 1, 3)
    assert ws_2016_01.last_date == datetime.date(2016, 1, 9)
    assert ws_2016_01.end_date == datetime.date(2016, 1, 10)
    assert ws_2016_01.first_weekday == week.SUNDAY

    assert [Week(year, 1, week.SUNDAY).start_date for year in range(2000, 2020)] == [
        datetime.date(2000, 1, 2),
        datetime.date(2000, 12, 31),  # 2001
        datetime.date(2001, 12, 30),  # 2002
        datetime.date(2002, 12, 29),  # 2003
        datetime.date(2004, 1, 4),
        datetime.date(2005, 1, 2),
        datetime.date(2006, 1, 1),
        datetime.date(2006, 12, 31),  # 2007
        datetime.date(2007, 12, 30),  # 2008
        datetime.date(2009, 1, 4),
        datetime.date(2010, 1, 3),
        datetime.date(2011, 1, 2),
        datetime.date(2012, 1, 1),
        datetime.date(2012, 12, 30),  # 2013
        datetime.date(2013, 12, 29),  # 2014
        datetime.date(2015, 1, 4),
        datetime.date(2016, 1, 3),
        datetime.date(2017, 1, 1),
        datetime.date(2017, 12, 31),  # 2018
        datetime.date(2018, 12, 30),  # 2019
    ]


def test_init_from_date():
    assert Week(datetime.date(2010, 5, 17)) == Week(2010, 20)
    assert Week(datetime.date(2010, 5, 16)) == Week(2010, 20, week.SUNDAY)
    assert Week(datetime.date(2014, 12, 29)) == Week(2015, 1)
    assert Week(datetime.date(2015, 1, 4)) == Week(2015, 1, week.SUNDAY)


def test_init_invalid_value():
    with pytest.raises(ValueError) as exc_info:
        Week(2000, 0)
    assert str(exc_info.value) == "week_num must be 1..53"

    with pytest.raises(ValueError) as exc_info:
        Week(2000, 53)
    assert str(exc_info.value) == "year 2000 has only 52 weeks"

    with pytest.raises(ValueError) as exc_info:
        Week(2000, 54)
    assert str(exc_info.value) == "week_num must be 1..53"

    with pytest.raises(ValueError) as exc_info:
        Week(40_000, 10)
    assert str(exc_info.value) == "year 40000 is out of range"

    # TODO: Week(1, 1) and Week(9999, -1) for misc first_weekdays


def test_init_invalid_type():
    with pytest.raises(TypeError):
        Week(2000)
    with pytest.raises(TypeError):
        Week(2000, year=2000)
    with pytest.raises(TypeError):
        Week(2000, 1, year=2000)
    with pytest.raises(TypeError):
        Week(2000, 1, year=2000, week_num=1)
    with pytest.raises(TypeError):
        Week(2000, 1, week.SUNDAY, first_weekday=week.MONDAY)


def test_weeks_count_monday():
    assert weeks_count(1997) == 52
    assert weeks_count(1998) == 53
    assert [year for year in range(1999, 2030) if weeks_count(year) == 53] == [
        2004, 2009, 2015, 2020, 2026
    ]


def test_weeks_count_sunday():
    assert weeks_count(1996, first_weekday=week.SUNDAY) == 52
    assert weeks_count(1997, first_weekday=week.SUNDAY) == 53
    assert [year for year in range(1998, 2032) if weeks_count(year, week.SUNDAY) == 53] == [
        2003, 2008, 2014, 2020, 2025, 2031
    ]


def test_repr():
    assert repr(Week(2000, 1)) == 'Week(2000, 1)'
    assert repr(Week(1776, 34)) == 'Week(1776, 34)'
    assert repr(Week(1998, 15, first_weekday=week.SUNDAY)) == 'Week(1998, 15, SUNDAY)'


def test_str():
    assert str(Week(2000, 1)) == "2000-W01"
    assert str(Week(1776, 34)) == "1776-W34"
    assert str(Week(476, 20)) == "0476-W20"
    assert str(Week(1998, 15, first_weekday=week.SUNDAY)) == "1998-W15"


def test_from_str():
    assert Week.from_str("2000-W01") == Week(2000, 1)
    assert Week.from_str("2013-W48") == Week(2013, 48)
    assert Week.from_str("2023-W05", week.SUNDAY) == Week(2023, 5, week.SUNDAY)
    assert Week.from_str("2016-W52", week.SUNDAY) == Week(2016, 52, week.SUNDAY)


def test_eq():
    assert Week(2000, 1) == Week(2000, 1)
    assert Week(2000, 2) == Week(2000, 2)
    assert Week(2001, 1) == Week(2001, 1)
    assert Week(2000, 1, week.SUNDAY) == Week(2000, 1, week.SUNDAY)

    assert Week(2000, 1) != Week(2000, 2)
    assert Week(2000, 1) != Week(2001, 1)
    assert Week(2000, 1) != Week(2000, 1, week.SUNDAY)


def test_hash():
    d = dict()
    d[Week(2020, 30)] = 'A'
    d[Week(2020, 31)] = 'B'
    d[Week(2020, 30)] = 'C'  # overwrite
    assert d == {
        Week(2020, 30): 'C',
        Week(2020, 31): 'B',
    }


def test_compare():
    assert Week(2015, 1) < Week(2016, 1)
    assert Week(2020, 1) > Week(2016, 1)
    assert Week(2018, 12) < Week(2018, 13)
    assert Week(2018, 14) > Week(2018, 13)

    assert Week(2016, 52) <= Week(2017, 1)
    assert Week(2017, 1) <= Week(2017, 1)
    assert Week(2020, 1) >= Week(2017, 1)
    assert Week(2017, 1) >= Week(2017, 1)


def test_iter():
    # dates
    dates_2021_01 = list(Week(2021, 1))
    assert len(dates_2021_01) == 7
    assert dates_2021_01[0] == datetime.date(2021, 1, 4)
    assert dates_2021_01[2] == datetime.date(2021, 1, 6)
    assert dates_2021_01[6] == datetime.date(2021, 1, 10)

    dates_2012_40 = list(Week(2012, 40, first_weekday=week.SUNDAY))
    assert len(dates_2012_40) == 7
    assert dates_2012_40[0] == datetime.date(2012, 9, 30)
    assert dates_2012_40[1] == datetime.date(2012, 10, 1)
    assert dates_2012_40[6] == datetime.date(2012, 10, 6)


def test_contains():
    # date in week?
    wm_2014_33 = Week(2014, 33)
    assert wm_2014_33.start_date == datetime.date(2014, 8, 11)
    assert wm_2014_33.end_date == datetime.date(2014, 8, 18)
    assert datetime.date(2013, 8, 13) not in wm_2014_33
    assert datetime.date(2014, 8, 10) not in wm_2014_33
    assert datetime.date(2014, 8, 11) in wm_2014_33
    assert datetime.date(2014, 8, 14) in wm_2014_33
    assert datetime.date(2014, 8, 17) in wm_2014_33
    assert datetime.date(2014, 8, 18) not in wm_2014_33
    assert datetime.date(2015, 8, 13) not in wm_2014_33

    ws_1980_04 = Week(1980, 4, week.SUNDAY)
    assert ws_1980_04.start_date == datetime.date(1980, 1, 20)
    assert ws_1980_04.end_date == datetime.date(1980, 1, 27)
    assert datetime.date(1970, 1, 22) not in ws_1980_04
    assert datetime.date(1980, 1, 1) not in ws_1980_04
    assert datetime.date(1980, 1, 19) not in ws_1980_04
    assert datetime.date(1980, 1, 20) in ws_1980_04
    assert datetime.date(1980, 1, 21) in ws_1980_04
    assert datetime.date(1980, 1, 26) in ws_1980_04
    assert datetime.date(1980, 1, 27) not in ws_1980_04
    assert datetime.date(1990, 1, 22) not in ws_1980_04


def test_len():
    # always 7
    assert all(
        len(Week(year, week_num)) == 7
        for year in [1990, 2000, 2013]
        for week_num in [1, 10, 40, 52]
    )


def test_for_date():
    # Week.for_date(date, first_weekday) -> Week
    assert Week.for_date(datetime.date(1998, 8, 1)) == Week(1998, 31)
    assert Week.for_date(datetime.date(1998, 8, 2)) == Week(1998, 31)
    assert Week.for_date(datetime.date(1998, 8, 3)) == Week(1998, 32)
    assert Week.for_date(datetime.date(1998, 8, 5)) == Week(1998, 32)
    assert Week.for_date(datetime.date(1998, 8, 9)) == Week(1998, 32)
    assert Week.for_date(datetime.date(1998, 8, 10)) == Week(1998, 33)

    assert Week.for_date(datetime.date(2008, 12, 28)) == Week(2008, 52)
    assert Week.for_date(datetime.date(2008, 12, 29)) == Week(2009, 1)
    assert Week.for_date(datetime.date(2008, 12, 31)) == Week(2009, 1)
    assert Week.for_date(datetime.date(2009, 1, 4)) == Week(2009, 1)
    assert Week.for_date(datetime.date(2009, 1, 5)) == Week(2009, 2)
    assert Week.for_date(datetime.date(2009, 12, 27)) == Week(2009, 52)
    assert Week.for_date(datetime.date(2009, 12, 28)) == Week(2009, 53)
    assert Week.for_date(datetime.date(2009, 12, 31)) == Week(2009, 53)
    assert Week.for_date(datetime.date(2010, 1, 1)) == Week(2009, 53)
    assert Week.for_date(datetime.date(2010, 1, 3)) == Week(2009, 53)
    assert Week.for_date(datetime.date(2010, 1, 4)) == Week(2010, 1)

    assert Week.for_date(datetime.date(2008, 3, 23)) == Week(2008, 12)
    assert Week.for_date(datetime.date(2008, 3, 23), week.SUNDAY) == Week(2008, 13, week.SUNDAY)


def test_today():
    with freeze_time("2022-09-25"):
        assert Week.today() == Week(2022, 38)
        assert Week.today().start_date == datetime.date(2022, 9, 19)

        assert Week.today(first_weekday=week.SUNDAY) == Week(2022, 39, first_weekday=week.SUNDAY)
        assert Week.today(first_weekday=week.SUNDAY).start_date == datetime.date(2022, 9, 25)

    with freeze_time("1995-12-31"):
        assert Week.today() == Week(1995, 52)
        assert Week.today().start_date == datetime.date(1995, 12, 25)

        assert Week.today(first_weekday=week.SUNDAY) == Week(1996, 1, first_weekday=week.SUNDAY)
        assert Week.today(first_weekday=week.SUNDAY).start_date == datetime.date(1995, 12, 31)

    with freeze_time("2030-05-15"):
        assert Week.today() == Week(2030, 20)
        assert Week.today().start_date == datetime.date(2030, 5, 13)

        assert Week.today(first_weekday=week.SUNDAY) == Week(2030, 20, first_weekday=week.SUNDAY)
        assert Week.today(first_weekday=week.SUNDAY).start_date == datetime.date(2030, 5, 12)


def test_getitem():
    wm_1990_20 = Week(1990, 20)
    assert wm_1990_20.start_date == datetime.date(1990, 5, 14)
    assert wm_1990_20.first_weekday == week.MONDAY
    assert wm_1990_20[week.MONDAY] == datetime.date(1990, 5, 14)
    assert wm_1990_20[week.WEDNESDAY] == datetime.date(1990, 5, 16)
    assert wm_1990_20[week.SATURDAY] == datetime.date(1990, 5, 19)
    assert wm_1990_20[week.SUNDAY] == datetime.date(1990, 5, 20)

    wm_1970_53 = Week(1970, 53)
    assert wm_1970_53.start_date == datetime.date(1970, 12, 28)
    assert wm_1970_53.first_weekday == week.MONDAY
    assert wm_1970_53[week.MONDAY] == datetime.date(1970, 12, 28)
    assert wm_1970_53[week.THURSDAY] == datetime.date(1970, 12, 31)
    assert wm_1970_53[week.FRIDAY] == datetime.date(1971, 1, 1)
    assert wm_1970_53[week.SUNDAY] == datetime.date(1971, 1, 3)

    ws_1956_33 = Week(1956, 33, first_weekday=week.SUNDAY)
    assert ws_1956_33.start_date == datetime.date(1956, 8, 12)
    assert ws_1956_33.first_weekday == week.SUNDAY
    assert ws_1956_33[week.SUNDAY] == datetime.date(1956, 8, 12)
    assert ws_1956_33[week.MONDAY] == datetime.date(1956, 8, 13)
    assert ws_1956_33[week.FRIDAY] == datetime.date(1956, 8, 17)
    assert ws_1956_33[week.SATURDAY] == datetime.date(1956, 8, 18)


def test_set_first_weekday():
    assert week.get_first_weekday() == week.MONDAY
    assert calendar.firstweekday() == week.MONDAY

    assert Week(2020, 1).start_date.weekday() == week.MONDAY

    week.set_first_weekday(week.SUNDAY)
    assert week.get_first_weekday() == week.SUNDAY
    assert calendar.firstweekday() == week.SUNDAY

    assert Week(2020, 1).start_date.weekday() == week.SUNDAY

    calendar.setfirstweekday(week.MONDAY)
    assert week.get_first_weekday() == week.MONDAY
    assert calendar.firstweekday() == week.MONDAY

    assert Week(2020, 2).start_date.weekday() == week.MONDAY
