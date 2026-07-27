import pygame as pg
from dataclasses import dataclass


@dataclass(slots=True)
class Camera:
    x: float
    y: float
    z: float

    def listen(self, event):
        if event.type == pg.MOUSEMOTION and event.buttons[0]:
            self.x -= event.rel[0]
            self.y -= event.rel[1]
