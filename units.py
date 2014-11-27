import yaml
import os
from unit import *

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

