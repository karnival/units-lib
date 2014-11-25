# Unit tests for units-lib.
from units import *
from nose.tools import assert_almost_equal, assert_greater, assert_less,\
assert_equal, assert_sequence_equal, assert_true, assert_false

def test_amount_creation():
    assert_equal(Amount(5,"metres").number, 5)
    assert_equal(Amount(5,"metres").unit, "metres")
    assert_equal((5*metres).unit, "metres")

def test_conversion():
    print(Amount(5,"metres").to("millimetres"))

def test_addition():
    print(3*metres + 5*millimetres)
    print((3*metres + 5*metres).number)

    print(((4*metres + 1.5*metres)).to("millimetres").number)

def test_equality():
    assert_true(3*metres==3*metres)
    assert_true(3*metres==3000*millimetres)
    assert_false(3*metres==3001*millimetres)
    assert_false(3*metres==2*metres)

def test_multiplication():
    print(3*metres)

def test_inconsistent_units():
    pass
