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


def test_add_others():
    # TODO: other additions than int
    with pytest.raises(TypeError) as exc_info:
        MonthDelta(1) + 3
    assert str(exc_info.value) == "unsupported operand type(s) for +: 'MonthDelta' and 'int'"

    with pytest.raises(TypeError) as exc_info:
        3 + MonthDelta(1)
    assert str(exc_info.value) == "unsupported operand type(s) for +: 'int' and 'MonthDelta'"


def test_sub_monthdelta():
    assert MonthDelta(3) - MonthDelta(2) == MonthDelta(1)
    assert MonthDelta(4) - MonthDelta(5) == MonthDelta(-1)
    assert MonthDelta(10) - MonthDelta(10) == MonthDelta(0)


def test_sub_others():
    # TODO: other subtractions than int
    with pytest.raises(TypeError) as exc_info:
        MonthDelta(1) - 1
    assert str(exc_info.value) == "unsupported operand type(s) for -: 'MonthDelta' and 'int'"

    with pytest.raises(TypeError) as exc_info:
        1 - MonthDelta(1)
    assert str(exc_info.value) == "unsupported operand type(s) for -: 'int' and 'MonthDelta'"


def test_mul():
    assert MonthDelta(6) * 2 == MonthDelta(years=12)
    assert MonthDelta(0) * 10 == MonthDelta(0)
    assert MonthDelta(1) * (-2) == MonthDelta(-2)


def test_div():
    assert MonthDelta(years=1) // 2 == MonthDelta(6)
    assert MonthDelta(5) // 2 == MonthDelta(2)
    assert MonthDelta(-9) // 3 == MonthDelta(-3)
    assert MonthDelta(-10) // 7 == MonthDelta(-2)
