import os
import pygame as pg
from dataclasses import dataclass, astuple

import gatti_math as gm
import gatti_colors as gc
import gatti_state as gs


@dataclass(slots=True)
class GattiSplash:

    @classmethod
    def empty(cls):
        return cls()

    def run(self, screen: pg.Surface, font: pg.font.Font, pos: gm.Vec2, size: gm.Vec2):

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    # exit splash-screen enter board
                    if event.key == pg.K_RETURN:
                        return gs.GattiState.BOARD

                    # exit program
                    elif event.key == pg.K_ESCAPE:
                        return gs.GattiState.EXIT
                
            # draw background (placeholder-color)
            screen.fill("#ff00ff")
            rect = (pos.x, pos.y, size.x, size.y)
            pg.draw.rect(screen, "#ff0000", rect)

            pg.display.update()
