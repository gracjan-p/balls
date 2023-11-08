
from math import sqrt


class Vector:
    def __init__(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector((self.x + other.x, self.y + other.y))
        return Vector((self.x + other, self.y + other))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector((self.x - other.x, self.y - other.y))
        return Vector((self.x - other, self.y - other))

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector((self.x * other.x, self.y * other.y))
        return Vector((self.x * other, self.y * other))

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector((self.x / other.x, self.y / other.y))
        return Vector((self.x / other, self.y / other))

    def __neg__(self):
        return Vector((-self.x, -self.y))

    def __eq__(self, other):
        self.x, self.y = other.x, other.y

    def __call__(self):
        return self.x, self.y

    def neg_x(self):
        return Vector((-self.x, self.y))

    def neg_y(self):
        return Vector((self.x, -self.y))

    def distance(self, other):
        if isinstance(other, self.__class__):
            a = abs(self.x - other.x)
            b = abs(self.y - other.y)
            return sqrt(a**2 + b**2)
        return sqrt(self.x**2 + self.y**2)


if __name__ == '__main__':
    a = Vector((2,2))
    print(
        (-a)()
    )