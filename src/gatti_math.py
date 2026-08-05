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


def relto(obj: Vec2, cam: Vec2, h: float):
    return (obj - cam) * h

def absto(obj: Vec2, cam: Vec2, h: float):
    return (obj / h + cam)

def minmax(l: Vec2, m: Vec2, u: Vec2):
    return Vec2(
        x=min(max(l.x, m.x), u.x),
        y=min(max(l.y, m.y), u.y)
    )

def in_box(nw: Vec2, p: Vec2, se: Vec2):
    return nw.x < p.x < se.x and nw.y < p.y < se.y
