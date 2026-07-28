import pygame as pg
from dataclasses import dataclass


@dataclass(slots=True)
class Vec2:
    x: float
    y: float


@dataclass(slots=True)
class Camera:
    x: float
    y: float
    z: float

    @classmethod
    def empty(cls):
        return cls(0, 0, 1)

    @classmethod
    def load(cls, d):
        return cls(x=d["x"], y=d["y"], z=d["z"])

    def dump(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    def listen(self, event):
        if event.type == pg.MOUSEMOTION and event.buttons[0]:
            self.x -= event.rel[0] / self.z
            self.y -= event.rel[1] / self.z

        if event.type == pg.MOUSEWHEEL:
            x, y = pg.mouse.get_pos()
            dz = 1.0 - event.y * 0.05
            self.x += x * ((1 - dz) / self.z)
            self.y += y * ((1 - dz) / self.z)
            self.z /= dz

    def lenrel(self, d):
        return d * self.z

    def lenabs(self, d):
        return d / self.z

    def posrel(self, posabs: Vec2):
        return Vec2(
            x=(posabs.x - self.x) * self.z,
            y=(posabs.y - self.y) * self.z
        )

    def posabs(self, posrel: Vec2):
        return Vec2(
            x=(posrel.x / self.z + self.x),
            y=(posrel.y / self.z + self.y)
        )
