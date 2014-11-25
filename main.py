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
        return self.__mul__(self, number)

    def to(self, new_unit):
        if self.unit == new_unit:
            return self
        else:
            factor = factor_dict[self.unit, new_unit]
            return Amount(self.number*factor, new_unit)


a = Amount(5, "metres")
print(a.number)
print(a.unit)
print((a + Amount(2, "metres")).number)
print((a + Amount(2, "metres")).unit)
print((a + Amount(2, "millimetres")).number)
print((a + Amount(2, "millimetres")).unit)
print((Amount(2, "millimetres") + a).number)
print((Amount(2, "millimetres") + a).unit)


metres = Amount(1, "metres")
print(3*metres)
