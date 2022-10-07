import calendar
import datetime

import pytest
from freezegun import freeze_time

from calendarium import week
from calendarium.week import first_date
from calendarium.week import first_week_offset
from calendarium.week import Week
from calendarium.week import weeks_count


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


def test_first_date():
    assert first_date(2001, week.MONDAY) == datetime.date(2001, 1, 1)
    assert first_date(2001, week.TUESDAY) == datetime.date(2001, 1, 2)
    assert first_date(2001, week.SUNDAY) == datetime.date(2001, 1, 7)

    assert first_date(2002, week.MONDAY) == datetime.date(2002, 1, 7)
    assert first_date(2002, week.TUESDAY) == datetime.date(2002, 1, 1)
    assert first_date(2002, week.THURSDAY) == datetime.date(2002, 1, 3)

    assert first_date(2003, week.MONDAY) == datetime.date(2003, 1, 6)
    assert first_date(2003, week.TUESDAY) == datetime.date(2003, 1, 7)
    assert first_date(2003, week.SATURDAY) == datetime.date(2003, 1, 4)

    assert first_date(2004, week.MONDAY) == datetime.date(2004, 1, 5)
    assert first_date(2004, week.WEDNESDAY) == datetime.date(2004, 1, 7)
    assert first_date(2004, week.THURSDAY) == datetime.date(2004, 1, 1)

    assert first_date(2005, week.MONDAY) == datetime.date(2005, 1, 3)
    assert first_date(2005, week.FRIDAY) == datetime.date(2005, 1, 7)
    assert first_date(2005, week.SATURDAY) == datetime.date(2005, 1, 1)

    assert first_date(2006, week.MONDAY) == datetime.date(2006, 1, 2)
    assert first_date(2006, week.SUNDAY) == datetime.date(2006, 1, 1)
    assert first_date(2006, week.SATURDAY) == datetime.date(2006, 1, 7)

    assert first_date(2010, week.MONDAY) == datetime.date(2010, 1, 4)
    assert first_date(2010, week.THURSDAY) == datetime.date(2010, 1, 7)
    assert first_date(2010, week.FRIDAY) == datetime.date(2010, 1, 1)

    with pytest.raises(calendar.IllegalWeekdayError) as exc_info:
        first_date(2000, weekday=10)
    assert str(exc_info.value) == "bad weekday number 10; must be 0 (Monday) to 6 (Sunday)"


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


def test_init_single_arg():
    assert Week("2015-W05") == Week(2015, 5)
    assert Week((2004, 48)) == Week(2004, 48)
    assert Week((2003, 1, None)) == Week(2003, 1)
    assert Week((1999, 1, week.SUNDAY)) == Week(1999, 1, week.SUNDAY)

    assert Week("2011-W01", first_weekday=week.SUNDAY) == Week(2011, 1, week.SUNDAY)
    assert Week((1990, 33), first_weekday=week.SUNDAY) == Week(1990, 33, week.SUNDAY)


def test_init_copy():
    original_monday = Week(2008, 8)
    assert original_monday.first_weekday == week.MONDAY
    copy_monday = Week(original_monday)
    assert copy_monday is not original_monday
    assert copy_monday == original_monday

    original_sunday = Week(2008, 8, week.SUNDAY)
    copy_sunday = Week(original_sunday)
    assert copy_sunday is not original_sunday
    assert copy_sunday == original_sunday

    copy_fwd_override = Week(original_monday, first_weekday=week.SUNDAY)
    assert copy_fwd_override == copy_sunday == original_sunday

    copy_sunday_no_override = Week(original_sunday, first_weekday=None)
    assert copy_sunday_no_override is not original_sunday
    assert copy_sunday_no_override == original_sunday
    assert copy_sunday_no_override == copy_sunday


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

    with pytest.raises(calendar.IllegalWeekdayError) as exc_info:
        Week(2000, 1, first_weekday=7)
    assert str(exc_info.value) == "bad weekday number 7; must be 0 (Monday) to 6 (Sunday)"

    with pytest.raises(calendar.IllegalWeekdayError) as exc_info:
        Week(2000, 1, first_weekday=-1)
    assert str(exc_info.value) == "bad weekday number -1; must be 0 (Monday) to 6 (Sunday)"

    # TODO: Week(1, 1) and Week(9999, -1) for misc first_weekdays


def test_init_invalid_type():
    with pytest.raises(TypeError) as exc_info:
        Week()
    assert str(exc_info.value) == "function missing required argument 'iso_year' (pos 1)"

    with pytest.raises(TypeError) as exc_info:
        Week(2000)
    assert str(exc_info.value) == "failed to convert single value of type 'int' into Week"

    with pytest.raises(TypeError) as exc_info:
        Week(2000, iso_year=2000)
    assert str(exc_info.value) == "function argument given by name ('iso_year') and position (1)"

    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1, iso_year=2000)
    assert str(exc_info.value) == "function argument given by name ('iso_year') and position (1)"

    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1, week_num=2)
    assert str(exc_info.value) == "function argument given by name ('week_num') and position (2)"

    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1, iso_year=2000, week_num=1)
    assert str(exc_info.value) == "function accepts at most 3 arguments (4 given)"

    with pytest.raises(TypeError):
        Week(2000, 1, week.SUNDAY, first_weekday=week.MONDAY)
    assert str(exc_info.value) == "function accepts at most 3 arguments (4 given)"

    with pytest.raises(TypeError) as exc_info:
        Week(first_weekday=week.SUNDAY)
    assert str(exc_info.value) == "function missing required argument 'iso_year' (pos 1)"

    with pytest.raises(TypeError) as exc_info:
        Week(iso_year=2000)
    assert str(exc_info.value) == "function missing required argument 'week_num' (pos 2)"

    with pytest.raises(TypeError) as exc_info:
        Week(week_num=20)
    assert str(exc_info.value) == "function missing required argument 'iso_year' (pos 1)"

    with pytest.raises(TypeError) as exc_info:
        Week(iso_year=20, first_weekday=week.SUNDAY)
    assert str(exc_info.value) == "function missing required argument 'week_num' (pos 2)"

    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1, oranges=2000)
    assert str(exc_info.value) == "'oranges' is an invalid keyword argument for this function"

    with pytest.raises(TypeError) as exc_info:
        Week(apples=2000)
    assert str(exc_info.value) == "'apples' is an invalid keyword argument for this function"


def test_for_date():
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


def test_for_date_sunday():
    assert Week.for_date(datetime.date(2008, 3, 23), week.SUNDAY) == Week(2008, 13, week.SUNDAY)

    with week.having_first_weekday(week.SUNDAY):
        assert Week.for_date(datetime.date(1996, 12, 21)) == Week(1996, 51)
        assert Week.for_date(datetime.date(1996, 12, 22)) == Week(1996, 52)
        assert Week.for_date(datetime.date(1996, 12, 28)) == Week(1996, 52)
        assert Week.for_date(datetime.date(1996, 12, 29)) == Week(1997, 1)
        assert Week.for_date(datetime.date(1996, 12, 31)) == Week(1997, 1)
        assert Week.for_date(datetime.date(1997, 1, 1)) == Week(1997, 1)
        assert Week.for_date(datetime.date(1997, 1, 4)) == Week(1997, 1)
        assert Week.for_date(datetime.date(1997, 1, 5)) == Week(1997, 2)
        assert Week.for_date(datetime.date(1997, 1, 11)) == Week(1997, 2)
        assert Week.for_date(datetime.date(1997, 1, 12)) == Week(1997, 3)
        assert Week.for_date(datetime.date(1997, 12, 27)) == Week(1997, 52)
        assert Week.for_date(datetime.date(1997, 12, 28)) == Week(1997, 53)
        assert Week.for_date(datetime.date(1997, 12, 29)) == Week(1997, 53)
        assert Week.for_date(datetime.date(1997, 12, 31)) == Week(1997, 53)
        assert Week.for_date(datetime.date(1998, 1, 1)) == Week(1997, 53)
        assert Week.for_date(datetime.date(1998, 1, 3)) == Week(1997, 53)
        assert Week.for_date(datetime.date(1998, 1, 4)) == Week(1998, 1)
        assert Week.for_date(datetime.date(1998, 1, 10)) == Week(1998, 1)
        assert Week.for_date(datetime.date(1998, 1, 11)) == Week(1998, 2)


def test_repr():
    assert repr(Week(2000, 1)) == 'Week(2000, 1)'
    assert repr(Week(1776, 34)) == 'Week(1776, 34)'
    assert repr(Week(1998, 15, first_weekday=week.SUNDAY)) == 'Week(1998, 15, SUNDAY)'


def test_str():
    assert str(Week(2000, 1)) == "2000-W01"
    assert str(Week(1776, 34)) == "1776-W34"
    assert str(Week(476, 20)) == "0476-W20"
    assert str(Week(1998, 15, first_weekday=week.SUNDAY)) == "1998-W15"


def test_format():
    assert format(Week(2000, 1)) == "2000-W01"
    assert format(Week(2013, 19), "%G-W%V") == "2013-W19"
    assert format(Week(1995, 9), "%V/%g") == "09/95"
    assert format(Week(2077, 3), "[W|%V|%g]") == "[W|03|77]"


def test_from_str():
    assert Week.from_str("2000-W01") == Week(2000, 1)
    assert Week.from_str("2013-W48") == Week(2013, 48)
    assert Week.from_str("2023-W05", week.SUNDAY) == Week(2023, 5, week.SUNDAY)
    assert Week.from_str("2016-W52", week.SUNDAY) == Week(2016, 52, week.SUNDAY)


def test_parse():
    assert Week.parse("2000-W01") == Week(2000, 1)
    assert Week.parse("2000-W01", first_weekday=week.SUNDAY) == Week(2000, 1, week.SUNDAY)
    assert Week.parse("2013-W19", "%G-W%V") == Week(2013, 19)
    assert Week.parse("09/1995", "%V/%G") == Week(1995, 9)
    assert Week.parse("[W|03|2077]", "[W|%V|%G]") == Week(2077, 3)
    assert Week.parse("[W|40|2022]", "[W|%V|%G]", week.SUNDAY) == Week(2022, 40, week.SUNDAY)


def test_starting_at():
    w1 = Week.starting_at(datetime.date(2003, 4, 4))
    assert w1.start_date == datetime.date(2003, 4, 4)
    assert w1.last_date == datetime.date(2003, 4, 10)
    assert w1.end_date == datetime.date(2003, 4, 11)
    assert w1.first_weekday == week.FRIDAY

    w2 = Week.starting_at(datetime.date(1990, 12, 30))
    assert w2.start_date == datetime.date(1990, 12, 30)
    assert w2.last_date == datetime.date(1991, 1, 5)
    assert w2.end_date == datetime.date(1991, 1, 6)
    assert w2.first_weekday == week.SUNDAY


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


def test_sub():
    # week - week
    assert Week(2020, 20) - Week(2020, 15) == datetime.timedelta(weeks=5)
    assert Week(1997, 1) - Week(1996, 51) == datetime.timedelta(weeks=2)
    assert Week(2015, 1) - Week(2014, 1) == datetime.timedelta(weeks=52)
    assert Week(2000, 1) - Week(2000, 1) == datetime.timedelta(0)
    assert Week(2010, 30) - Week(2010, 40) == datetime.timedelta(weeks=-10)
    assert Week(2020, 10, week.MONDAY) - Week(2020, 8, week.SUNDAY) == datetime.timedelta(days=15)
    # week - timedelta
    assert Week(2000, 30) - datetime.timedelta(weeks=10) == Week(2000, 20)
    assert Week(2000, 30, week.SUNDAY) - datetime.timedelta(weeks=1) == Week(2000, 29, week.SUNDAY)
    # rounded
    assert Week(1995, 16) - datetime.timedelta(days=30) == Week(1995, 11)
    assert Week(1999, 30, week.SUNDAY) - datetime.timedelta(days=40) == Week(1999, 24, week.SUNDAY)


def test_sub_invalid():
    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1) - 10
    assert str(exc_info.value) == "unsupported operand type(s) for -: 'Week' and 'int'"

    with pytest.raises(TypeError) as exc_info:
        None - Week(2000, 3)
    assert str(exc_info.value) == "unsupported operand type(s) for -: 'NoneType' and 'Week'"


def test_add():
    # week + timedelta
    assert Week(2020, 1) + datetime.timedelta(weeks=4) == Week(2020, 5)
    assert Week(1997, 50, week.SUNDAY) + datetime.timedelta(weeks=3) == Week(1997, 53, week.SUNDAY)
    assert Week(1997, 50, week.SUNDAY) + datetime.timedelta(weeks=4) == Week(1998, 1, week.SUNDAY)
    assert datetime.timedelta(weeks=40) + Week(2030, 5) == Week(2030, 45)
    assert datetime.timedelta(weeks=1) + Week(2019, 3, week.SUNDAY) == Week(2019, 4, week.SUNDAY)


def test_add_invalid():
    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1) + Week(2002, 2)
    assert str(exc_info.value) == "unsupported operand type(s) for +: 'Week' and 'Week'"

    with pytest.raises(TypeError) as exc_info:
        Week(2000, 1) + 30
    assert str(exc_info.value) == "unsupported operand type(s) for +: 'Week' and 'int'"

    with pytest.raises(TypeError) as exc_info:
        datetime.date(2000, 1, 1) + Week(2009, 4)
    assert str(exc_info.value) == "unsupported operand type(s) for +: 'datetime.date' and 'Week'"


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


def test_first_weekday_context():
    assert week.get_first_weekday() == week.MONDAY
    assert Week(2002, 1).first_weekday == week.MONDAY
    assert Week(2038, 40).first_weekday == week.MONDAY

    with week.having_first_weekday(week.SUNDAY) as ctx:
        assert ctx is week.SUNDAY
        assert week.get_first_weekday() == week.SUNDAY
        assert Week(2002, 1).first_weekday == week.SUNDAY
        assert Week(2038, 40).first_weekday == week.SUNDAY

    assert Week(2002, 1).first_weekday == week.MONDAY
    assert Week(2038, 40).first_weekday == week.MONDAY

    week.set_first_weekday(week.SATURDAY)

    assert Week(2002, 1).first_weekday == week.SATURDAY
    assert Week(2038, 40).first_weekday == week.SATURDAY

    with week.having_first_weekday(week.FRIDAY) as ctx:
        assert ctx is week.FRIDAY
        assert week.get_first_weekday() == week.FRIDAY
        assert Week(2002, 1).first_weekday == week.FRIDAY
        assert Week(2038, 40).first_weekday == week.FRIDAY

    assert Week(2002, 1).first_weekday == week.SATURDAY
    assert Week(2038, 40).first_weekday == week.SATURDAY

    week.set_first_weekday(week.MONDAY)
