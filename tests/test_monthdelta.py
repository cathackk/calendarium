import datetime

import pytest

from calendarium.month import Month
from calendarium.month import MonthDelta


def test_init():
    def ym(md: MonthDelta) -> tuple[int, int]:
        return md.years, md.months

    assert ym(MonthDelta()) == (0, 0)
    assert ym(MonthDelta(1)) == (0, 1)
    assert ym(MonthDelta(11)) == (0, 11)
    assert ym(MonthDelta(12)) == (1, 0)
    assert ym(MonthDelta(40)) == (3, 4)
    assert ym(MonthDelta(-1)) == (0, -1)
    assert ym(MonthDelta(-11)) == (0, -11)
    assert ym(MonthDelta(-12)) == (-1, 0)
    assert ym(MonthDelta(-15)) == (-1, -3)


def test_total_months():
    assert MonthDelta().total_months() == 0
    assert MonthDelta(0).total_months() == 0
    assert MonthDelta(1).total_months() == 1
    assert MonthDelta(40).total_months() == 40
    assert MonthDelta(months=40).total_months() == 40

    assert MonthDelta(years=1).total_months() == 12
    assert MonthDelta(years=2, months=0).total_months() == 24
    assert MonthDelta(years=3, months=1).total_months() == 37
    assert MonthDelta(years=4, months=20).total_months() == 68
    assert MonthDelta(years=100).total_months() == 1200


def test_repr():
    assert repr(MonthDelta(3)) == 'MonthDelta(months=3)'
    assert repr(MonthDelta(0)) == 'MonthDelta(0)'
    assert repr(MonthDelta(-1)) == 'MonthDelta(months=-1)'
    assert repr(MonthDelta(12)) == 'MonthDelta(years=1)'
    assert repr(MonthDelta(years=1)) == 'MonthDelta(years=1)'
    assert repr(MonthDelta(years=3, months=9)) == 'MonthDelta(years=3, months=9)'
    assert repr(MonthDelta(years=3, months=12)) == 'MonthDelta(years=4)'
    assert repr(MonthDelta(years=4, months=20)) == 'MonthDelta(years=5, months=8)'
    assert repr(MonthDelta(months=100)) == 'MonthDelta(years=8, months=4)'


def test_str():
    assert str(MonthDelta()) == "P0M"
    assert str(MonthDelta(1)) == "P1M"
    assert str(MonthDelta(11)) == "P11M"
    assert str(MonthDelta(12)) == "P1Y"
    assert str(MonthDelta(13)) == "P1Y1M"
    assert str(MonthDelta(20)) == "P1Y8M"
    assert str(MonthDelta(100)) == "P8Y4M"

    assert str(MonthDelta(-1)) == "-P1M"
    assert str(MonthDelta(-20)) == "-P1Y8M"


def test_from_str():
    assert MonthDelta.from_str('P0M') == MonthDelta()
    assert MonthDelta.from_str('P0Y') == MonthDelta()

    assert MonthDelta.from_str('P1M') == MonthDelta(1)
    assert MonthDelta.from_str('P3M') == MonthDelta(3)
    assert MonthDelta.from_str('P12M') == MonthDelta(12)
    assert MonthDelta.from_str('P1Y') == MonthDelta(years=1)
    assert MonthDelta.from_str('P2Y') == MonthDelta(years=12)
    assert MonthDelta.from_str('P3Y6M') == MonthDelta(years=3, months=6)

    assert MonthDelta.from_str('-P1M') == -MonthDelta(1)
    assert MonthDelta.from_str('P-1M') == MonthDelta(-1)
    assert MonthDelta.from_str('-P-1M') == -MonthDelta(-1)
    assert MonthDelta.from_str('-P1Y') == -MonthDelta(years=1)
    assert MonthDelta.from_str('P-1Y') == MonthDelta(years=-1)
    assert MonthDelta.from_str('-P-1Y') == -MonthDelta(years=-1)
    assert MonthDelta.from_str('-P1Y1M') == -MonthDelta(years=1, months=1)
    assert MonthDelta.from_str('P-1Y1M') == MonthDelta(years=-1, months=1)
    assert MonthDelta.from_str('P1Y-1M') == MonthDelta(years=1, months=-1)
    assert MonthDelta.from_str('P-1Y-1M') == MonthDelta(years=-1, months=-1)
    assert MonthDelta.from_str('-P-1Y-1M') == -MonthDelta(years=-1, months=-1)


def test_from_str_invalid():
    for value in ['XXX', '1Y', 'P', 'p1y', 'P 1Y', 'PY']:
        print(value)
        with pytest.raises(ValueError) as exc_info:
            MonthDelta.from_str(value)
        assert str(exc_info.value) == f"invalid string for MonthDelta: {value!r}"


def test_eq():
    assert MonthDelta() == MonthDelta()
    assert MonthDelta(0) == MonthDelta()
    assert MonthDelta(1) == MonthDelta(1)
    assert MonthDelta(1) != MonthDelta(2)
    assert MonthDelta(1) != MonthDelta(-1)
    assert MonthDelta(-1) != MonthDelta(1)
    assert MonthDelta(years=2) == MonthDelta(24)

    a = MonthDelta(10)
    b = MonthDelta(10)
    assert a is not b
    assert a == b


def test_neg():
    assert MonthDelta() == -MonthDelta()
    assert MonthDelta(-1) == -MonthDelta(1)
    assert MonthDelta(2) == -MonthDelta(-2)
    assert MonthDelta(-20) == -MonthDelta(years=1, months=8)
    assert MonthDelta(years=-5, months=-1) == -MonthDelta(years=5, months=1)


def test_add_monthdelta():
    assert MonthDelta(1) + MonthDelta(1) == MonthDelta(2)
    assert MonthDelta(1) + MonthDelta() == MonthDelta(1)
    assert MonthDelta(years=1) + MonthDelta(-5) == MonthDelta(7)
    assert MonthDelta(12) + MonthDelta(years=-1) == MonthDelta()


def test_add_month():
    # see also test_month.test_add_monthdelta
    assert Month(2000, 1) + MonthDelta(1) == Month(2000, 2)
    assert Month(2000, 1) + MonthDelta(years=2) == Month(2002, 1)
    assert Month(2022, 3) + MonthDelta(-3) == Month(2021, 12)
    assert Month(2013, 4) + MonthDelta(0) == Month(2013, 4)
    assert MonthDelta(3) + Month(2016, 1) == Month(2016, 4)


def test_add_date():
    assert datetime.date(2021, 10, 12) + MonthDelta(1) == datetime.date(2021, 11, 12)
    assert datetime.date(1988, 3, 20) + MonthDelta(3) == datetime.date(1988, 6, 20)

    assert datetime.date(1999, 1, 31) + MonthDelta(1) == datetime.date(1999, 2, 28)
    assert datetime.date(2000, 1, 31) + MonthDelta(1) == datetime.date(2000, 2, 29)
    assert datetime.date(1999, 1, 30) + MonthDelta(13) == datetime.date(2000, 2, 29)

    assert datetime.date(2021, 5, 31) + MonthDelta(4) == datetime.date(2021, 9, 30)
    assert datetime.date(2024, 2, 29) + MonthDelta(years=1) == datetime.date(2025, 2, 28)
    assert datetime.date(2024, 2, 29) + MonthDelta(years=4) == datetime.date(2028, 2, 29)

    # adding MonthDelta and date is not always associative
    assert datetime.date(2010, 1, 31) + (MonthDelta(1) + MonthDelta(1)) == datetime.date(2010, 3, 31)
    assert (datetime.date(2010, 1, 31) + MonthDelta(1)) + MonthDelta(1) == datetime.date(2010, 3, 28)


def test_add_others():
    for obj in [0, 3, None, False]:
        with pytest.raises(TypeError) as exc_info:
            MonthDelta(1) + obj
        assert str(exc_info.value) == "unsupported operand type(s) for +: " \
                                      f"'MonthDelta' and '{type(obj).__name__}'"

        with pytest.raises(TypeError) as exc_info:
            obj + MonthDelta(1)
        assert str(exc_info.value) == "unsupported operand type(s) for +: " \
                                      f"'{type(obj).__name__}' and 'MonthDelta'"


def test_sub_monthdelta():
    assert MonthDelta(3) - MonthDelta(2) == MonthDelta(1)
    assert MonthDelta(4) - MonthDelta(5) == MonthDelta(-1)
    assert MonthDelta(10) - MonthDelta(10) == MonthDelta(0)


def test_sub_date():
    assert datetime.date(2000, 1, 1) - MonthDelta(1) == datetime.date(1999, 12, 1)
    assert datetime.date(2021, 3, 14) - MonthDelta(years=15) == datetime.date(2006, 3, 14)

    with pytest.raises(TypeError) as exc_info:
        MonthDelta(1) - datetime.date(2000, 1, 1)
    assert str(exc_info.value) == "unsupported operand type(s) for -: 'MonthDelta' and 'datetime.date'"


def test_sub_others():
    for obj in [0, 3, None, False]:
        with pytest.raises(TypeError) as exc_info:
            MonthDelta(1) - obj
        assert str(exc_info.value) == "unsupported operand type(s) for -: " \
                                      f"'MonthDelta' and '{type(obj).__name__}'"

        with pytest.raises(TypeError) as exc_info:
            obj - MonthDelta(1)
        assert str(exc_info.value) == "unsupported operand type(s) for -: " \
                                      f"'{type(obj).__name__}' and 'MonthDelta'"


def test_mul():
    assert MonthDelta(6) * 2 == MonthDelta(years=12)
    assert MonthDelta(0) * 10 == MonthDelta(0)
    assert MonthDelta(1) * (-2) == MonthDelta(-2)


def test_div():
    assert MonthDelta(years=1) // 2 == MonthDelta(6)
    assert MonthDelta(5) // 2 == MonthDelta(2)
    assert MonthDelta(-9) // 3 == MonthDelta(-3)
    assert MonthDelta(-10) // 7 == MonthDelta(-2)


def test_compare():
    assert MonthDelta(1) < MonthDelta(2)
    assert MonthDelta(3) > MonthDelta(2)
    assert MonthDelta(10) <= MonthDelta(12)
    assert MonthDelta(9) <= MonthDelta(9)
    assert MonthDelta(-1) >= MonthDelta(-5)
    assert MonthDelta(4) >= MonthDelta(4)
    assert MonthDelta(1) > MonthDelta(-1)


def test_bool():
    assert not MonthDelta(0)
    assert MonthDelta(1)
    assert MonthDelta(100)
    assert MonthDelta(-1)


def test_abs():
    assert abs(MonthDelta(-15)) == MonthDelta(15)
    assert abs(MonthDelta(-1)) == MonthDelta(1)
    assert abs(MonthDelta(0)) == MonthDelta(0)
    assert abs(MonthDelta(2)) == MonthDelta(2)


def test_between():
    assert MonthDelta.between(Month(2003, 1), Month(2003, 5)) == MonthDelta(4)
    assert MonthDelta.between((2010, 4), (2014, 4)) == MonthDelta(years=4)
    assert MonthDelta.between("2011-12", "2012-06") == MonthDelta(6)
