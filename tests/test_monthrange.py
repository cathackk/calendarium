import datetime

import pytest

from calendarium.month import Month
from calendarium.month import MonthDelta
from calendarium.month_range import MonthRange


def test_init():
    # start + end
    mr1 = MonthRange(Month(2010, 10), Month(2011, 2))
    assert mr1.start_month == Month(2010, 10)
    assert mr1.end_month == Month(2011, 2)
    assert mr1.duration == MonthDelta(4)
    # start + duration
    mr2 = MonthRange(start_month=Month(2014, 3), duration=MonthDelta(4))
    assert mr2.start_month == Month(2014, 3)
    assert mr2.end_month == Month(2014, 7)
    assert mr2.duration == MonthDelta(4)
    # end + duration
    mr3 = MonthRange(end_month=Month(2015, 8), duration=MonthDelta(6))
    assert mr3.start_month == Month(2015, 2)
    assert mr3.end_month == Month(2015, 8)
    assert mr3.duration == MonthDelta(6)
    # start + end + duration
    mr4 = MonthRange(Month(1998, 12), Month(1999, 12), duration=MonthDelta(years=1))
    assert mr4.start_month == Month(1998, 12)
    assert mr4.end_month == Month(1999, 12)
    assert mr4.duration == MonthDelta(years=1)

    # start can be after end
    mr5 = MonthRange(Month(2010, 10), Month(2010, 9))
    assert mr5.start_month == Month(2010, 10)
    assert mr5.end_month == Month(2010, 9)
    assert mr5.duration == MonthDelta(0)


def test_init_alt():
    mr1 = MonthRange("2022-01", "2022-04")
    assert mr1.start_month == Month(2022, 1)
    assert mr1.end_month == Month(2022, 4)
    assert mr1.duration == MonthDelta(3)

    mr2 = MonthRange((1998, 5), (2001, 4))
    assert mr2.start_month == Month(1998, 5)
    assert mr2.end_month == Month(2001, 4)
    assert mr2.duration == MonthDelta(years=2, months=11)

    mr3 = MonthRange("2001-11", months=4)
    assert mr3.start_month == Month(2001, 11)
    assert mr3.end_month == Month(2002, 3)
    assert mr3.duration == MonthDelta(4)

    mr4 = MonthRange(end_month=(1970, 1), months=12)
    assert mr4.start_month == Month(1969, 1)
    assert mr4.end_month == Month(1970, 1)
    assert mr4.duration == MonthDelta(12)


def test_init_invalid():
    # only start
    with pytest.raises(ValueError) as exc_info:
        MonthRange(Month(2020, 1))
    assert str(exc_info.value) == "too few arguments specified for MonthRange"
    # only end
    with pytest.raises(ValueError):
        MonthRange(end_month=Month(2020, 1))
    # only duration
    with pytest.raises(ValueError):
        MonthRange(duration=MonthDelta(8))
    # no args
    with pytest.raises(ValueError) as exc_info:
        MonthRange()
    assert str(exc_info.value) == "too few arguments specified for MonthRange"

    # start + end + duration nonmatching
    with pytest.raises(ValueError) as exc_info:
        MonthRange(Month(2020, 1), Month(2020, 2), MonthDelta(3))
    assert str(exc_info.value) == "duration mismatch: expected P1M, got P3M"


def test_repr():
    assert repr(MonthRange((2013, 4), (2014, 10))) == 'MonthRange(Month(2013, 4), Month(2014, 10))'
    assert repr(MonthRange((1999, 1), (1998, 2))) == 'MonthRange(Month(1999, 1), Month(1998, 2))'


def test_str():
    assert str(MonthRange(Month(2000, 1), Month(2002, 10))) == "2000-01/2002-10"
    assert str(MonthRange.year(1999)) == "1999-01/2000-01"
    assert str(MonthRange((2013, 1), (2015, 12))) == "2013-01/2015-12"
    assert str(MonthRange((2020, 10), (2020, 6))) == "2020-10/2020-06"


def test_format():
    mr = MonthRange((1999, 12), (2003, 4))
    assert format(mr) == "1999-12/2003-04"
    assert format(mr, '%Y-%m/') == "1999-12/2003-04"
    assert format(mr, '%b %y: .. ') == "Dec 99 .. Apr 03"
    assert format(mr, '[%B %Y]:->') == "[December 1999]->[April 2003]"
    # TODO: escape `:`


def test_from_str():
    assert MonthRange.from_str("2001-01/2004-10") == MonthRange((2001, 1), (2004, 10))
    assert MonthRange.from_str("2004-12/2005-02") == MonthRange((2004, 12), (2005, 2))
    assert MonthRange.from_str("2000-01/1990-01") == MonthRange((2000, 1), (1990, 1))


def test_parse():
    assert MonthRange.parse("1999-12/2003-04") == MonthRange((1999, 12), (2003, 4))
    assert MonthRange.parse("Jun 2019..Jul 2021", '%b %Y:..') == MonthRange((2019, 6), (2021, 7))


def test_start_end_last_date():
    mr1 = MonthRange(Month(2011, 8), Month(2013, 4))
    assert mr1.start_date == datetime.date(2011, 8, 1)
    assert mr1.end_date == datetime.date(2013, 4, 1)
    assert mr1.last_date == datetime.date(2013, 3, 31)

    mr2 = MonthRange(Month(2040, 1), Month(2040, 3))
    assert mr2.start_date == datetime.date(2040, 1, 1)
    assert mr2.end_date == datetime.date(2040, 3, 1)
    assert mr2.last_date == datetime.date(2040, 2, 29)

    mr3 = MonthRange((2020, 4), (2020, 4))
    assert mr3.start_date == datetime.date(2020, 4, 1)
    assert mr3.end_date == datetime.date(2020, 4, 1)
    assert mr3.last_date == datetime.date(2020, 3, 31)


def test_eq():
    m1 = MonthRange(Month(2020, 1), duration=MonthDelta(3))
    m2 = MonthRange(Month(2020, 1), Month(2020, 4))
    assert m1 is not m2
    assert m1 == m2

    assert MonthRange((2001, 5), (2001, 8)) == MonthRange(Month(2001, 5), months=3)
    assert MonthRange((2000, 5), (2001, 8)) != MonthRange(Month(2001, 5), months=3)
    assert MonthRange((2001, 6), (2001, 8)) != MonthRange(Month(2001, 5), months=3)
    assert MonthRange((2001, 5), (2002, 8)) != MonthRange(Month(2001, 5), months=3)
    assert MonthRange((2001, 5), (2001, 9)) != MonthRange(Month(2001, 5), months=3)
    assert MonthRange((2001, 5), (2001, 8)) != MonthRange(Month(2002, 5), months=3)
    assert MonthRange((2001, 5), (2001, 8)) != MonthRange(Month(2001, 9), months=3)
    assert MonthRange((2001, 5), (2001, 8)) != MonthRange(Month(2001, 5), months=4)
    assert MonthRange((2001, 5), (2001, 8)) != MonthRange(Month(2001, 5), months=-3)

    assert MonthRange("2001-01", "2002-01") == MonthRange(Month(2001, 1), Month(2002, 1))
    assert MonthRange("2001-01", "2002-01") != Month(2001, 1)
    assert MonthRange("2001-01", "2002-01") != "2001-01..2002-01"
    assert MonthRange("2001-01", "2002-01") != 20

    # all empty ranges are equal
    assert MonthRange((2001, 5), (2001, 5)) == MonthRange((2021, 4), (2021, 3))
    assert MonthRange((2002, 1), (2000, 1)) == MonthRange((2002, 1), (2001, 1))


def test_len():
    assert len(MonthRange((2001, 1), (2001, 4))) == 3
    assert len(MonthRange((2003, 12), (2004, 8))) == 8
    assert len(MonthRange((1980, 1), (1980, 1))) == 0
    assert len(MonthRange((1980, 1), (1979, 1))) == 0


def test_iter():
    mr = MonthRange((2001, 3), (2001, 6))
    g = iter(mr)
    assert next(g) == Month(2001, 3)
    assert next(g) == Month(2001, 4)
    assert next(g) == Month(2001, 5)
    with pytest.raises(StopIteration):
        next(g)

    assert list(MonthRange((1999, 10), (2000, 3))) == [
        Month(1999, 10), Month(1999, 11), Month(1999, 12), Month(2000, 1), Month(2000, 2)
    ]

    assert list(MonthRange((1999, 10), (1999, 10))) == []
    assert list(MonthRange((1999, 10), (1999, 6))) == []


def test_days():
    mr = MonthRange((2004, 12), (2005, 3))
    g = mr.days()
    assert next(g) == datetime.date(2004, 12, 1)
    assert next(g) == datetime.date(2004, 12, 2)
    assert next(g) == datetime.date(2004, 12, 3)
    for _ in range(85):
        next(g)
    assert next(g) == datetime.date(2005, 2, 27)
    assert next(g) == datetime.date(2005, 2, 28)
    with pytest.raises(StopIteration):
        next(g)

    mr_2004 = MonthRange.year(2004)
    dates_2004 = list(mr_2004.days())
    assert len(dates_2004) == 366
    assert dates_2004[0] == datetime.date(2004, 1, 1) == mr_2004.start_date
    assert dates_2004[-1] == datetime.date(2004, 12, 31) == mr_2004.last_date

    assert list(MonthRange((2000, 1), (1999, 12)).days()) == []


def test_total_days():
    assert MonthRange.year(2004).total_days() == 366
    assert MonthRange.year(2005).total_days() == 365
    assert MonthRange((2001, 2), months=3).total_days() == 89  # 28 + 31 + 30
    assert MonthRange((2001, 6), months=3).total_days() == 92  # 30 + 31 + 31
    assert MonthRange((2005, 12), (2006, 2)).total_days() == 62  # 31 + 31
    assert MonthRange((2005, 3), (2005, 3)).total_days() == 0
    assert MonthRange((2005, 3), (2000, 5)).total_days() == 0


def test_timedelta():
    assert MonthRange((1999, 12), (2000, 2)).timedelta() == datetime.timedelta(days=62)
    assert MonthRange((2004, 3), (2004, 8)).timedelta() == datetime.timedelta(days=153)
    assert MonthRange((2000, 1), (2000, 1)).timedelta() == datetime.timedelta(days=0)
    assert MonthRange((2000, 1), (1900, 1)).timedelta() == datetime.timedelta(days=0)


def test_contains():
    mr = MonthRange((2020, 11), (2021, 3))

    assert (2020, 1) not in mr
    assert (2020, 10) not in mr
    assert (2020, 11) in mr
    assert (2020, 12) in mr
    assert (2021, 2) in mr
    assert (2021, 3) not in mr
    assert (2021, 12) not in mr

    assert Month(2020, 12) in mr
    assert Month(2021, 2) in mr
    assert Month(2021, 3) not in mr
    assert Month(2021, 12) not in mr

    assert "2020-10" not in mr
    assert "2020-11" in mr
    assert "2021-02" in mr
    assert "2021-03" not in mr

    assert datetime.date(2020, 10, 31) not in mr
    assert datetime.date(2020, 11, 1) in mr
    assert datetime.date(2020, 11, 5) in mr
    assert datetime.date(2020, 12, 28) in mr
    assert datetime.date(2021, 2, 28) in mr
    assert datetime.date(2021, 3, 1) not in mr

    mr_empty = MonthRange((2000, 1), (2000, 1))
    assert Month(2000, 1) not in mr_empty
    assert datetime.date(2000, 1, 1) not in mr_empty


def test_add():
    assert MonthRange((2020, 11), months=3) + MonthDelta(1) == MonthRange((2020, 12), months=3)
    assert MonthRange((1988, 10), months=5) + MonthDelta(12) == MonthRange((1989, 10), months=5)
    assert MonthDelta(3) + MonthRange((2000, 1), (2000, 3)) == MonthRange((2000, 4), (2000, 6))

    assert str(MonthRange((2000, 1), (2000, 1)) + MonthDelta(1)) == "2000-02/2000-02"


def test_bool():
    assert not MonthRange((2000, 1), months=0)
    assert not MonthRange((2000, 1), (1999, 1))
    assert MonthRange((2000, 1), months=1)
    assert MonthRange((2000, 1), (2001, 1))


def test_year():
    assert MonthRange.year(2000) == MonthRange((2000, 1), (2001, 1))
    assert MonthRange.year(1776) == MonthRange((1776, 1), (1777, 1))


def test_halfyear():
    assert MonthRange.halfyear(1999, 1) == MonthRange((1999, 1), (1999, 7))
    assert MonthRange.halfyear(1999, 2) == MonthRange((1999, 7), (2000, 1))

    for half in [-1, 0, 3, 4]:
        with pytest.raises(ValueError) as exc_info:
            MonthRange.halfyear(2020, half)
        assert str(exc_info.value) == "half must be 1 or 2"


def test_quarter():
    assert MonthRange.quarter(2021, 1) == MonthRange((2021, 1), (2021, 4))
    assert MonthRange.quarter(2021, 2) == MonthRange((2021, 4), (2021, 7))
    assert MonthRange.quarter(2021, 3) == MonthRange((2021, 7), (2021, 10))
    assert MonthRange.quarter(1888, 4) == MonthRange((1888, 10), (1889, 1))

    for q in [-10, -1, 0, 5, 10]:
        with pytest.raises(ValueError) as exc_info:
            MonthRange.quarter(1999, q)
        assert str(exc_info.value) == "quarter must be in 1..4"


def test_following():
    mr1 = MonthRange((2000, 8), (2000, 11))
    assert (mr2 := mr1.following()) == MonthRange((2000, 11), (2001, 2))
    assert (mr3 := mr2.following()) == MonthRange((2001, 2), (2001, 5))
    assert mr3.following() == MonthRange((2001, 5), (2001, 8))

    mr4 = MonthRange((2020, 1), (2020, 12))
    assert (mr5 := mr4.following()) == MonthRange((2020, 12), (2021, 11))
    assert (mr6 := mr5.following()) == MonthRange((2021, 11), (2022, 10))
    assert mr6.following() == MonthRange((2022, 10), (2023, 9))

    empty_following = MonthRange((1990, 1), (1990, 1)).following()
    assert not empty_following
    assert empty_following.start_month == empty_following.end_month == Month(1990, 1)

    neg_following = MonthRange((2004, 3), (2004, 1)).following()
    assert not neg_following
    assert neg_following.start_month == Month(2004, 1)
    assert neg_following.end_month == Month(2003, 11)


def test_preceding():
    mr1 = MonthRange((2000, 8), (2000, 11))
    assert (mr2 := mr1.preceding()) == MonthRange((2000, 5), (2000, 8))
    assert (mr3 := mr2.preceding()) == MonthRange((2000, 2), (2000, 5))
    assert mr3.preceding() == MonthRange((1999, 11), (2000, 2))

    mr4 = MonthRange((2020, 1), (2020, 12))
    assert (mr5 := mr4.preceding()) == MonthRange((2019, 2), (2020, 1))
    assert (mr6 := mr5.preceding()) == MonthRange((2018, 3), (2019, 2))
    assert mr6.preceding() == MonthRange((2017, 4), (2018, 3))

    empty_preceding = MonthRange((2000, 4), (2000, 4)).preceding()
    assert not empty_preceding
    assert empty_preceding.start_month == empty_preceding.end_month == Month(2000, 4)

    neg_preceding = MonthRange((2015, 3), (2014, 12)).preceding()
    assert not neg_preceding
    assert neg_preceding.start_month == Month(2015, 6)
    assert neg_preceding.end_month == Month(2015, 3)
