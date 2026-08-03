import os
import pygame as pg
from dataclasses import dataclass, astuple

import tom_math as tm
import tom_colors as tc
import tom_state as ts


@dataclass(slots=True)
class TomSearch:
    part: str
    walk: list[str]
    hint: list[str]
    index: int

    @classmethod
    def empty(cls):
        return cls(part="", walk=os.path.abspath("").split('/'), hint=[], index=0)

    def genhint(self):

        LEGAL = [".jpg", ".jpeg", ".png", ".webp"]

        # absolute path is used because it hints at possible sub-directories
        path = '/'.join(self.walk)

        # only some specific names are worth exploring
        self.hint = sorted(
            name for name in os.listdir(path)

            # filter names that are incompatible with the query
            if self.part in name[:len(self.part)] and

            # filter unrecognized formats (that aren't directories)
            (any(fmt in name for fmt in LEGAL) or os.path.isdir(f"{path}/{name}"))

        )

    def run(self, screen, font, bg, pos):

        self.genhint()

        while True:
            for event in pg.event.get():

                # ignore non-keyboard input
                if event.type != pg.KEYDOWN:
                    continue

                # pop latest user-input character if the BACKSPACE key is pressed
                if event.key == pg.K_BACKSPACE:
                    if len(self.part) > 0:
                        self.part = self.part[:-1]
                    else:
                        self.walk.pop()
                        
                # roll through hints
                elif event.key == pg.K_TAB:
                    self.index = (self.index + 1) % len(self.hint)

                # process user-input if the RETURN key is pressed and a possible match exists
                elif event.key == pg.K_RETURN:

                    # this conditional is separated from the previous so that RETURN wouldn't be read as unicode
                    if len(self.hint) == 0:
                        continue

                    # fit user-input to nearest hint and extend walk
                    self.walk.append(self.hint[self.index])
                    self.part = ""

                    # transition to the BOARD if the walk can no longer be extended otherwise generate new hints
                    path = '/'.join(self.walk)
                    if not os.path.isdir(path):
                        return ts.TomState.BOARD

                # exit program if the ESC key is pressed
                elif event.key == pg.K_ESCAPE:
                    return ts.TomState.EXIT

                # append user-input if the pressed key ALPHA-NUMERICAL
                else:
                    self.part += event.unicode

                self.genhint()

            # draw background
            screen.blit(bg, (0, 0))

            # draw search box (active buffer)
            text = '/'.join(self.walk + [self.part])
            pos_box = pos - tm.Vec2(*font.size(text)) / 2
            srf = font.render(text, antialias=True, color=tc.TEXT)
            screen.blit(srf, astuple(pos_box))
            
            # draw search box (completion hints)
            fade = 255 / 2
            for i, p in enumerate(self.hint[self.index:] + self.hint[:self.index]):

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
