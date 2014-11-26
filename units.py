import yaml
import os

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

    def __div__(self, other):
        if isinstance(other, (int, long, float)):
            return Amount(other/self.number, self.unit)
        elif self.unit is None and other.unit is not None:
            return Amount(self.number / other.number, 1/other.unit)
        elif other.unit is None and self.unit is not None:
            return Amount(self.number / other.number, self.unit)
        elif other.unit is None and self.unit is None:
            return self.number/other.number
        elif isinstance(other, Amount):
            return Amount(other.number/self.number, self.unit / other.unit)

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
                factor = self.unit.find_factor(new_unit)
                return Amount(self.number*factor, new_unit)



class Unit(object):
    def __init__(self, units_dict, name, factor):
        self.units_dict = units_dict
        self.units_list = [i for i in self.units_dict]
        self.name = name
        self.factor = factor

    def __eq__(self, other):
        return (self.units_dict == other.units_dict and self.factor == other.factor)

    def __mul__(self, other):
        # Add together dictionary items with matching keys.
        union_dict = [(k, self.units_dict[k] + other.units_dict[k]) for k in
                       set(self.units_dict) & set(other.units_dict)]

        self_not_other = [(k, self.units_dict[k]) for k in set(self.units_dict)
                          - set(other.units_dict)]

        other_not_self = [(k, other.units_dict[k]) for k in set(other.units_dict)
                          - set(self.units_dict)]

        return_dict = dict(union_dict + self_not_other + other_not_self)

        return Unit(return_dict, self.name + other.name, self.factor*other.factor)

    def __rmul__(self, other):
        return self.__mul__(self, other)

    def __div__(self, other):
        # Make the denominator have negative exponents in its units_dict, then
        # multiply.
        other_reciprocal = copy(other)
        other_reciprocal.units_dict = [(k, -other.units_dict[k]) for k in other.units_dict]
        return self.__mul__(self, other_reciprocal)

    def find_factor(self, new_unit):
        # Look up conversions to SI, unit by unit. If units are compatible,
        # conversion factor is the product of individual conversion factors.
        try:
            new_to_SI = 1
            print self.factor
            for unit in new_unit.units_dict:
                print definitions[unit]
                print new_unit.units_dict
                new_to_SI = new_to_SI*definitions[unit][2]**new_unit.units_dict[unit][1]

            self_to_SI = 1
            for unit in self.unit.units_dict:
                self_to_SI = self_to_SI*definitions[unit][2]**self.unit.units_dict[unit][1]

            if new_unit.units_dict == self.unit.units_dict:
                return new_to_SI / self_to_SI 
            else:
                raise IncompatibleTypesError("Types are incompatible.")

        except not IncompatibleTypesError:
            raise TypeNotFoundError("Type not found in unit dictionary!")

# Load definitions file.
definitions = yaml.load(open(os.path.join(os.path.dirname(__file__),'definitions.yml')))

# Create Amount of size 1 for each unit -- this is what lets us express units as
# e.g. 3*unitname
for unit in definitions:
    unit_dict = dict(zip(definitions[unit][0], definitions[unit][1]))
    globals()[unit] = Amount(1, Unit(unit_dict, [unit], definitions[unit][2]))

#print Newtons.unit.units_dict
