from errors import *
from copy import deepcopy

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
        return self.__mul__(other)

    def __div__(self, other):
        # Make the denominator have negative exponents in its dimns_dict, then
        # multiply.
        other_reciprocal = deepcopy(other)
        other_reciprocal.dimns_dict = dict((k, -other.dimns_dict[k]) for k in other.dimns_dict)
        other_reciprocal.factor = 1/other_reciprocal.factor
        return self.__mul__(other_reciprocal)

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

