from dataclasses import dataclass


@dataclass(slots=True, order=True)
class Vec2:
    x: float
    y: float

    def __mul__(self, s):
        return Vec2(self.x * s, self.y * s)

    def __truediv__(self, s):
        return Vec2(self.x / s, self.y / s)

    def __add__(self, vec):
        return Vec2(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2(self.x - vec.x, self.y - vec.y)


def relto(obj, cam, h):
    return (obj - cam) * h

def absto(obj, cam, h):
    return (obj / h + cam)
