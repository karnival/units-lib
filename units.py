# Global dictionary of conversion factors.
factor_dict = {("metres", "metres") : 1, ("metres", "millimetres") : 1000,
               ("millimetres", "metres") : 0.001}

# Amount of some quantity -- e.g. 5*metres.
class Amount:
    def __init__(self, number, unit):
        self.number = number
        self.unit = unit

    def __add__(self, other):
        return Amount((other.to(self.unit).number + self.number), self.unit)

    def __radd__(self, other):
        return self.__add__(self, other)

    # Multiplication by unitless scalars only.
    def __mul__(self, number):
        return Amount(number, self.unit)

    def __rmul__(self, number):
        return self.__mul__(number)

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
            factor = factor_dict[self.unit, new_unit]
            return Amount(self.number*factor, new_unit)


metres = Amount(1, "metres")
millimetres = Amount(1, "millimetres")
