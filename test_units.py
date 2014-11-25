# Unit tests for units-lib.
from units import *
from nose.tools import assert_almost_equal, assert_greater, assert_less, assert_equal, assert_sequence_equal

def test_amount_creation():
    a = Amount(5, "metres")
    print(a.number)
    print(a.unit)

def test_conversion():
    print(Amount(5,"metres").to("millimetres"))

def test_addition():
    a = Amount(5, "metres")
    print((a + Amount(2, "metres")).number)
    print((a + Amount(2, "metres")).unit)
    print((a + Amount(2, "millimetres")).number)
    print((a + Amount(2, "millimetres")).unit)

    print(3*metres + 5*millimetres)
    print((3*metres + 5*metres).number)

    print(((4*metres + 1.5*metres)).to("millimetres").number)

def test_multiplication():
    print(3*metres)

def test_inconsistent_units():
    a = Amount(5, "metres")
    print((Amount(2, "millimetres") + a).number)
    print((Amount(2, "millimetres") + a).unit)



