import os
import pygame as pg
from dataclasses import dataclass, astuple

from . import tom_math as tm
from . import tom_colors as tc
from . import tom_state as ts


@dataclass(slots=True)
class TomSearch:
    part: str
    walk: list[str]
    hint: list[str]

    @classmethod
    def empty(cls):
        return cls(part="", walk=[], hint=[])

    def run(self, mnt, screen, font, bg, pos):

        # generate hints
        self.hint = sorted(os.listdir(mnt + '/'.join(self.walk)))

        while True:
            for event in pg.event.get():

                # ignore non-keyboard input
                if event.type != pg.KEYDOWN:
                    continue

                # pop latest user-input character if the BACKSPACE key is pressed
                if event.key == pg.K_BACKSPACE:
                    self.part = self.part[:-1]

                # process user-input if the RETURN key is pressed
                elif event.key == pg.K_RETURN:

                    # fit user-input to nearest hint and extend walk
                    fit = [n for n in self.hint if self.part in n[:len(self.part)]][0]
                    self.walk.append(fit)
                    self.part = ""

                    # transition to the BOARD if the walk can no longer be extended otherwise generate new hints
                    path = mnt + '/'.join(self.walk)
                    if not os.path.isdir(path):
                        return ts.TomState.BOARD
                    else:
                        self.hint = [n for n in sorted(os.listdir(path))]

                # exit program if the ESC key is pressed
                elif event.key == pg.K_ESCAPE:
                    return ts.TomState.EXIT

                # append user-input if the pressed key ALPHA-NUMERICAL
                else:
                    self.part += event.unicode

            # draw background
            screen.blit(bg, (0, 0))

            # draw search box (active buffer)
            text = '/'.join(self.walk + [self.part])
            pos_box = pos - tm.Vec2(*font.size(text)) / 2
            srf = font.render(text, antialias=True, color=tc.TEXT)
            screen.blit(srf, astuple(pos_box))
            
            # draw search box (completion hints)
            fade = 255 / 2
            for i, p in enumerate(n for n in self.hint if self.part in n):

                # fade out rendered text
                text = '/'.join(self.walk + [p])
                srf = font.render(text, antialias=True, color=tc.TEXT)
                srf.set_alpha(fade)

                # blit text in a cascading fashion under the active buffer
                pos_box = pos - tm.Vec2(*font.size(text)) / 2
                pos_offset = tm.Vec2(0, font.get_height() * (i+1))
                screen.blit(srf, astuple(pos_box + pos_offset))

                fade /= 2
        
            pg.display.update()
