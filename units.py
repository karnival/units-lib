# Global dictionary of conversion factors.
factor_dict = {"metres" : (["metres"], 1.0), "millimetres" : (["metres"], 1000.0),
               "coulombs" : (["coulombs"], 1.0), "Newtons" : (["kilograms","metres","seconds^-1","seconds^-1"],1.0),
               "kilograms" : (["kilograms"], 1.0), "seconds^-1" : (["seconds^-1"], 1.0),
               "pounds" : (["kilograms"], 2.204623)
               }
class IncompatibleTypesError(Exception):
        pass

class TypeNotFoundError(Exception):
        pass

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
        if type(new_unit) is Amount:
            if self.unit == new_unit.unit:
                return self
            else:
                factor = self.find_factor(new_unit.unit) 
                return Amount(self.number*factor, new_unit.unit)
        else:
            if self.unit == new_unit:
                return self
            else:
                factor = self.find_factor(new_unit)
                return Amount(self.number*factor, new_unit)

    def find_factor(self, new_unit):
        # Look up conversions to SI, unit by unit. If units are compatible,
        # conversion factor is the product of individual conversion factors.
        try:
            new_list_SI = []
            new_to_SI = 1
            for unit in new_unit.units_list:
                new_list_SI = new_list_SI + factor_dict[unit][0]
                new_to_SI = new_to_SI*factor_dict[unit][1]

            self_list_SI = []
            self_to_SI = 1
            for unit in self.unit.units_list:
                self_list_SI = self_list_SI + factor_dict[unit][0]
                self_to_SI = self_to_SI*factor_dict[unit][1]

            if sorted(new_list_SI) == sorted(self_list_SI):
                return new_to_SI / self_to_SI 
            else:
                raise IncompatibleTypesError("Types are incompatible.")

        except not IncompatibleTypesError:
            raise TypeNotFoundError("Type not found in unit dictionary!")


class Unit(object):
    def __init__(self, units_list):
        self.units_list = units_list
        self.compact_string = ""
        self.stringify()

    def stringify(self):
        self.compact_string = " ".join(self.units_list)

    def __eq__(self, other):
        return (sorted(self.units_list) == sorted(other.units_list))

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
