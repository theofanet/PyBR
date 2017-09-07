import math


class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            self.x /= mag
            self.y /= mag
        return mag

    def mult(self, mult):
        self.x *= mult
        self.y *= mult

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length(self):
        return self.magnitude()

    def angle(self):
        return math.atan2(self.x, self.y) * 180 / math.pi
