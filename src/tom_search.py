from dataclasses import dataclass, astuple
import os
import pygame as pg
from enum import Enum, auto
from .tom_math import Vec2
from . import tom_colors
from . import tom_params
from .tom_state import TomState


@dataclass(slots=True)
class TomSearch:
    part: str
    walk: list[str]
    hint: list[str]

    @classmethod
    def empty(cls):
        return cls(
            part="",
            walk=[],
            hint=[]
        )

    def run(self, mnt, screen, font, bg, pos):
        self.hint = sorted(os.listdir(mnt + '/'.join(self.walk)))
        while True:
            for event in pg.event.get():
                if event.type != pg.KEYDOWN:
                    continue
                if event.key == pg.K_BACKSPACE:
                    self.part = self.part[:-1]
                elif event.key == pg.K_RETURN:
                    self.part = [n for n in self.hint if self.part in n[:len(self.part)]][0]
                    self.walk.append(self.part)
                    path = mnt + '/'.join(self.walk)
                    if os.path.isdir(path):
                        self.part = ""
                        self.hint = [n for n in sorted(os.listdir(path))]
                    # transition event
                    else:
                        return TomState.BOARD
                # exit program
                elif event.key == pg.K_ESCAPE:
                    return TomState.EXIT
                else:
                    self.part += event.unicode
            
            # draw background
            screen.blit(bg, (0, 0))

            # draw search box (active buffer)
            text = '/'.join(self.walk + [self.part])
            width, height = font.size(text)
            screen.blit(font.render(text, antialias=True, color=tom_colors.TEXT), astuple(pos - Vec2(*font.size(text)) / 2))
            
            # draw search box (completion hints)
            fade = 255 / 2
            for i, p in enumerate(n for n in self.hint if self.part in n):
                text = '/'.join(self.walk + [p])
                width, height = font.size(text)
                srf = font.render(text, antialias=True, color=tom_colors.TEXT)
                srf.set_alpha(fade)
                screen.blit(srf, astuple(pos - Vec2(*font.size(text)) / 2 + Vec2(0, font.get_height() * (i+1))))
                fade /= 2
        
            pg.display.update()
