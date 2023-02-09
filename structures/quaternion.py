# quaternion.py
from operator import add, div, mul, neg, sub


class quaternion:

    def __init__(self, data):
        quaternion_length = 4
        self._data = list(data)[0:quaternion_length]
        self.index = 0

    def __add__(self, other):
        sum = map(add, self._data, other._data)
        return quaternion(sum)

    def __div__(self, other):
        if isinstance(other, quaternion):
            return self * other.conj() / other.normSqr()
        else:
            quot = [item / other for item in self]
            return quaternion(quot)

    def __getitem__(self, index):
        return self._data[index]

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.data)

    def __mul__(self, other):
        prod0 = self[0] * other[0] - self[1] * other[1] - \
            self[2] * other[2] - self[3] * other[3]
        prod1 = self[0] * other[1] + self[1] * other[0] + \
            self[2] * other[3] - self[3] * other[2]
        prod2 = self[0] * other[2] + self[2] * other[0] + \
            self[3] * other[1] - self[1] * other[3]
        prod3 = self[0] * other[3] + self[3] * other[0] + \
            self[1] * other[2] - self[2] * other[1]
        prod = [prod0, prod1, prod2, prod3]
        return quaternion(prod)

    def __neg__(self):
        opp = map(neg, self)
        return quaternion(opp)

    def __repr__(self):
        return self.str_simp()

    def __sub__(self, other):
        diff = map(sub, self._data, other._data)
        return quaternion(diff)

    def __str__(self):
        return self.str_simp()

    def __truediv__(self, other):
        return self.__div__(other)

    def conj(self):
        conj0 = self[0]
        conj1 = - self[1]
        conj2 = - self[2]
        conj3 = - self[3]
        conj = [conj0, conj1, conj2, conj3]
        return quaternion(conj)

    def copy(self):
        return quaternion(self)

    def inv(self):
        return self.conjugate()

    def next(self):
        try:
            result = self._data[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def norm(self):
        return sqrt(self.normSqr())

    def normalize(self):
        self = self / self.norm()

    def normSqr(self):
        sum = 0
        for pt in self._data:
            sum = sum + pt * pt
        return sum

    def str_simp(self):
        return tuple(self._data).__str__()

    @property
    def I(self):
        return self.conjugate()


if __name__ == "__main__":
    from sympy import symbols
    q0, q1, q2, q3 = symbols('q0 q1 q2 q3')
    q = quaternion([q0, q1, q2, q3])
    print q
    print - q
    print q + q
    print q - q
    print q * q
    print q /
