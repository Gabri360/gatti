from dataclasses import dataclass
import pygame as pg
from enum import Enum, auto
from .tom_math import Vec2, absto
from .tom_board import TomBoard
from .tom_search import TomSearch
from .tom_state import TomState
from . import tom_colors
from . import tom_params


@dataclass(slots=True)
class TomProgram:
    board: TomBoard
    search: TomSearch

    @classmethod
    def empty(cls):
        return cls(TomBoard.empty(), TomSearch.empty())

    def run(self, mnt, screen):
        state = TomState.BOARD
        while True:
            match state:

                case TomState.BOARD:
                    state = self.board.run(screen)

                case TomState.SEARCH:
                    bg = pg.transform.gaussian_blur(screen, 20)
                    layer = pg.Surface(screen.get_size())
                    layer.fill("#000000")
                    layer.set_alpha(100)
                    bg.blit(layer, (0, 0))
                    state = self.search.run(mnt, screen, pg.font.SysFont("Calibri", 24), bg, Vec2(*screen.get_size()) / 2)
                    if state == TomState.BOARD:
                        # add searched image at the relative center of the board
                        path = mnt + '/'.join(self.search.walk)
                        srf = pg.image.load(path).convert_alpha()
                        scale = 0.5 * screen.get_width() / (srf.get_width() * self.board.cam_scale)
                        pos = (Vec2(*screen.get_size()) - Vec2(*srf.get_size())  * scale) / 2
                        self.board.add(path, srf, pos, scale)
                        self.search.part = ""
                        self.search.walk.pop()

                    state = TomState.BOARD

                case TomState.EXIT:
                    break
