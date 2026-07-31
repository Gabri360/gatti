import os
import pygame as pg
from enum import Enum, auto
from search_box import SearchBox
from image_network import ImageNetwork
from camera import Camera, Vec2
import tom_colors
import tom_params
import tom_serialization


class State(Enum):
    TRAVEL = auto()
    MOVE = auto()
    SEARCH = auto()


pg.init()
pg.display.set_caption("tom")
screen = pg.display.set_mode((tom_params.WIDTH, tom_params.HEIGHT))

cam, images = tom_serialization.load()

search_box = SearchBox(
    pos=Vec2(tom_params.WIDTH/2, tom_params.HEIGHT/2),
    size=Vec2(tom_params.WIDTH / 2, tom_params.HEIGHT / 12),
    font=pg.font.SysFont("Calibri", 24),
    partial="",
    root=tom_params.ROOT,
    path=[],
    candidates=[n for n in sorted(os.listdir(tom_params.ROOT))],
    color_text=tom_colors.TEXT,
    result=None
)

state = State.TRAVEL
color_bg = tom_colors.BG_TRAVEL
opaque = pg.Surface((tom_params.WIDTH, tom_params.HEIGHT), pg.SRCALPHA)
opaque.fill("#000000")
opaque.set_alpha(100)
blur = pg.Surface((tom_params.WIDTH, tom_params.HEIGHT))
while True:
    for event in pg.event.get():

        match state:
            case State.TRAVEL:
                cam.listen(event)
            case State.MOVE:
                images.listen(event, cam)
            case State.SEARCH:
                search_box.listen(event)
                if search_box.result is not None:
                    srf = pg.image.load(search_box.result).convert_alpha()
                    images.add(search_box.result, srf, tom_params.WIDTH, tom_params.HEIGHT, cam)
                    search_box.result = None
                    state = State.MOVE
                    color_bg = tom_colors.BG_MOVE

        if event.type == pg.MOUSEWHEEL:
            images.update(cam)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s and state != State.SEARCH:
                state = State.SEARCH
                blur = pg.transform.gaussian_blur(screen, 20)
                color_bg = tom_colors.BG_SEARCH
            if event.key == pg.K_ESCAPE:
            #if event.key == pg.K_s or event.key == pg.K_ESCAPE:
                #if event.key == pg.K_s:
                #    pg.image.save(screen, "tom.png")

                tom_serialization.dump(cam, images)

                pg.quit()
                exit()

    screen.fill(color_bg)
    images.draw(screen, cam)
    if state == State.SEARCH:
        screen.blit(blur, (0, 0))
        screen.blit(opaque, (0, 0))
        search_box.draw(screen)

    pg.display.update()
