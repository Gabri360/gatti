import pygame as pg
from dataclasses import dataclass

import gatti_math as gm
import gatti_colors as gc
from gatti_board import GattiBoard
from gatti_search import GattiSearch
from gatti_state import GattiState


@dataclass(slots=True)
class GattiProgram:
    board: GattiBoard
    search: GattiSearch

    @classmethod
    def empty(cls):
        return cls(GattiBoard.empty(), GattiSearch.empty())

    def run(self, screen):
        state = GattiState.BOARD
        while True:
            match state:
                case GattiState.BOARD:

                    # entering the BOARD state and waiting for termination to read transition
                    state = self.board.run(screen)

                case GattiState.SEARCH:

                    # fast gaussian blur (3-pass) of the board
                    bg = pg.transform.box_blur(screen, 3)
                    bg = pg.transform.box_blur(bg, 5)
                    bg = pg.transform.box_blur(bg, 7)

                    # layer solid color over blur
                    layer = pg.Surface(screen.get_size())
                    layer.fill(gc.BG_SEARCH)
                    layer.set_alpha(100)
                    bg.blit(layer, (0, 0))

                    # entering the SEARCH state and waiting for termination to read transition
                    state = self.search.run(screen, pg.font.SysFont("Calibri", 24), bg, gm.Vec2(*screen.get_size()) / 2)

                    # transition from search query to board
                    if state == GattiState.BOARD:

                        # load the searched image
                        srf = pg.image.load(self.search.result).convert_alpha()

                        # add image to center of the board with half-screen-width scale
                        scale_rel = 0.5 * screen.get_width() / srf.get_width()
                        scale_abs = scale_rel / self.board.cam_scale
                        pos_rel = (gm.Vec2(*screen.get_size()) - gm.Vec2(*srf.get_size())  * scale_rel) / 2
                        pos_abs = gm.absto(pos_rel, self.board.cam_pos, self.board.cam_scale)
                        self.board.add(self.search.result, srf, pos_abs, scale_abs)

                case GattiState.EXIT:
                    # exit the program
                    break
