# Unit tests for units-lib.
import units-lib as u
from nose.tools import assert_almost_equal, assert_greater, assert_less, assert_equal, assert_sequence_equal

def test_amount_creation():
    a = u.Amount(5, "metres")
    print(a.number)
    print(a.unit)

def test_conversion():
    print(u.Amount(5,"metres").to("millimetres"))

def test_addition():
    print((a + u.Amount(2, "metres")).number)
    print((a + u.Amount(2, "metres")).unit)
    print((a + u.Amount(2, "millimetres")).number)
    print((a + u.Amount(2, "millimetres")).unit)

    print(3*metres + 5*millimetres)
    print((3*metres + 5*metres).number)

    print(((4*metres + 1.5*metres)).to("millimetres").number)

def test_multiplication():
    print(3*metres)

def test_inconsistent_units():
    print((u.Amount(2, "millimetres") + a).number)
    print((u.Amount(2, "millimetres") + a).unit)



