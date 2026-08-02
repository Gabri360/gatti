import pygame as pg
from dataclasses import dataclass

import tom_math as tm
from tom_board import TomBoard
from tom_search import TomSearch
from tom_state import TomState


@dataclass(slots=True)
class TomProgram:
    board: TomBoard
    search: TomSearch

    @classmethod
    def empty(cls):
        return cls(TomBoard.empty(), TomSearch.empty())

    def run(self, screen):
        state = TomState.BOARD
        while True:
            match state:
                case TomState.BOARD:
                    # entering the BOARD state and waiting for termination to read transition
                    state = self.board.run(screen)

                case TomState.SEARCH:
                    # screenshot the board, blur and and darken it and use it as background
                    bg = pg.transform.gaussian_blur(screen, 20)
                    layer = pg.Surface(screen.get_size())
                    layer.fill("#000000")
                    layer.set_alpha(100)
                    bg.blit(layer, (0, 0))

                    # entering the SEARCH state and waiting for termination to read transition
                    state = self.search.run(screen, pg.font.SysFont("Calibri", 24), bg, tm.Vec2(*screen.get_size()) / 2)

                    # transition from search query to board
                    if state == TomState.BOARD:

                        # load the searched image
                        path = '/'.join(self.search.walk)
                        srf = pg.image.load(path).convert_alpha()

                        # add image to center of the board with half-screen-width scale
                        scale_rel = 0.5 * screen.get_width() / srf.get_width()
                        scale_abs = scale_rel / self.board.cam_scale
                        pos_rel = (tm.Vec2(*screen.get_size()) - tm.Vec2(*srf.get_size())  * scale_rel) / 2
                        pos_abs = tm.absto(pos_rel, self.board.cam_pos, self.board.cam_scale)
                        self.board.add(path, srf, pos_abs, scale_abs)

                        # prepare next query
                        self.search.walk.pop()

                case TomState.EXIT:
                    # exit the program
                    break
