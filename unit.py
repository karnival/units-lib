# Definition of a Unit, which is used as a component of the Amount object.
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

