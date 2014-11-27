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
                factor = self.unit.find_factor(new_unit.unit) 
                return Amount(self.number*factor, new_unit.unit)
        else:
            if self.unit == new_unit:
                return self
            else:
                factor = self.unit.find_factor(new_unit)
                return Amount(self.number*factor, new_unit)



class Unit(object):
    def __init__(self, definition):
        self.dimns_dict = definition[0]
        self.dimns_list = [(w + "^" + str(n) + " ") for (w,n) in self.dimns_dict.iteritems()]
        self.factor = definition[1]

    def __eq__(self, other):
        return (self.dimns_dict == other.dimns_dict and self.factor == other.factor)

    def __mul__(self, other):
        # Add together dictionary items with matching keys.
        return_dict = dict((k, self.dimns_dict[k] + other.dimns_dict[k]) for k in self.dimns_dict)
        return_factor = self.factor * other.factor
        return Unit([return_dict, return_factor])

    def __rmul__(self, other):
        return self.__mul__(self, other)

    def __div__(self, other):
        # Make the denominator have negative exponents in its dimns_dict, then
        # multiply.
        other_reciprocal = copy(other)
        other_reciprocal.dimns_dict = dict((k, -other.dimns_dict[k]) for k in other.dimns_dict)
        return self.__mul__(self, other_reciprocal)

    def find_factor(self, new_unit):
        # Look up conversions to SI, unit by unit. If units are compatible,
        # conversion factor is the product of individual conversion factors.
        try:
            if new_unit.dimns_dict == self.dimns_dict:
                return new_unit.factor / self.factor
            else:
                raise IncompatibleTypesError("Types are incompatible.")

        except not IncompatibleTypesError:
            raise TypeNotFoundError("Type not found in unit dictionary!")

# Load definitions file.
definitions = yaml.load(open(os.path.join(os.path.dirname(__file__),'definitions.yml')))

# Create Amount of size 1 for each unit -- this is what lets us express units as
# e.g. 3*unitname
for unit in definitions:
    # Expand dimension dicts: where a fundamental dimension isn't specified, set
    # it to zero.
    definition = definitions[unit]

    base_dimensions = ("metres", "kilograms", "amperes", "Kelvin", "seconds",
                       "moles", "candela")

    for dimension in base_dimensions:
        if dimension not in definition[0]:
            definition[0][dimension] = 0.0

    globals()[unit] = Amount(1, Unit(definition))

#print Newtons.unit.dimns_dict
