# Unit tests for units-lib.
from units import *
from nose.tools import assert_almost_equal, assert_greater, assert_less,\
assert_equal, assert_sequence_equal, assert_true, assert_false

def test_amount_creation():
    assert_equal((5*metres).unit, metres.unit)

def test_conversion():
    assert_equal((5*metres).to(millimetres.unit), 5000*millimetres)

    try:
        (5*metres).to(coulombs)
    except IncompatibleTypesError:
        assert True 

def test_addition():
    assert_equal((3*metres + 5*millimetres), 3.005*metres)
    assert_equal((3*metres + 5*millimetres), 3005*millimetres)
    assert_equal((3*metres + 5*millimetres).to(metres).number, 3.005)

def test_equality():
    assert_true(3*metres==3*metres)
    assert_true(3*metres==3000*millimetres)
    assert_false(3*metres==3001*millimetres)
    assert_false(3*metres==2*metres)
    assert_false(3*metres==3)

def test_multiplication():
    assert_equal(3*metres*5, 15*metres)
    assert_equal((3*metres * 5*coulombs), 15*metres*coulombs)
    assert_equal(metres*metres*metres*millimetres,
                 millimetres*metres*metres*metres)

    a = 3*metres*millimetres * 5*coulombs*metres
    b = 0.015*metres*metres*metres*coulombs

    assert_equal((3*metres*millimetres * 5*coulombs*metres), 0.015*metres*metres*metres*coulombs)

def test_division():
    2*metres/seconds + 3*inches/minutes

def test_inconsistent_units():
    try:
        3*metres + 5*coulombs
    except IncompatibleTypesError:
        assert True
