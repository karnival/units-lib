# Global dictionary of conversion factors.
factor_dict = {("metres", "metres") : 1, ("metres", "millimetres") : 1000,
               ("millimetres", "metres") : 0.001}

# Amount of some quantity -- e.g. 5*metres.
class Amount(object):
    def __init__(self, number, unit):
        self.number = number
        self.unit = unit

    def __add__(self, other):
        return Amount((other.to(self.unit).number + self.number), self.unit)

    def __radd__(self, other):
        return self.__add__(self, other)

    # Multiplication by unitless scalars only.
    def __mul__(self, other):
        if isinstance(other, (int, long, float)):
            return Amount(other*self.number, self.unit)
        elif self.unit is None and other.unit is not None:
            return Amount(self.number * other.number, other.unit)
        elif other.unit is None and self.unit is not None:
            return Amount(self.number * other.number, self.unit)
        elif other.unit is None and self.unit is None:
            return self.number*other.number
        elif isinstance(other, Amount):
            return Amount(other.number*self.number, self.unit * other.unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        try:
            converted = other.to(self.unit)
        except:
            pass
        else:
            return self.number==converted.number

    def to(self, new_unit):
        if self.unit == new_unit:
            return self
        else:
            factor = factor_dict[self.unit.compact_string, new_unit.compact_string]
            return Amount(self.number*factor, new_unit)

class Unit(object):
    def __init__(self, units_list):
        self.units_list = units_list
        self.compact_string = ""
        self.stringify()

    def stringify(self):
        self.compact_string = " ".join(self.units_list)

    def __eq__(self, other):
        return (self.compact_string == other.compact_string)

    def __mul__(self, other):
        return Unit(self.units_list + other.units_list)

    def __rmul__(self, other):
        return self.__mul__(self, other)

MetresUnit = Unit(["metres"])
MillimetresUnit = Unit(["millimetres"])
CoulombsUnit = Unit(["coulombs"])

metres = Amount(1, MetresUnit)
millimetres = Amount(1, MillimetresUnit)
coulombs = Amount(1, CoulombsUnit)
