import json
import os
import pygame as pg
from search_box import SearchBox


with open("palette.json", "r") as file:
    palette = json.load(file)
    COLOR_BACKGROUND = palette["background"]
    COLOR_TEXT = palette["text"]
    

with open("settings.json", "r") as file:
    settings = json.load(file)
    WIDTH = settings["width"]
    HEIGHT = settings["height"]
    ROOT = settings["root"]


pg.init()
pg.display.set_caption("Desktop")
screen = pg.display.set_mode((WIDTH, HEIGHT))
search_box = SearchBox(
    font=pg.font.SysFont("Calibri", 16),
    buffer=ROOT,
    root=ROOT,
    neighbours=[ROOT + n for n in sorted(os.listdir(ROOT))],
    color_text=COLOR_TEXT,
    result=None
)

images_offline = []
images_online = []
pos = []
width = []
height = []
scale = []

x0, y0 = 0, 0
while True:
    dx, dy = 0, 0
    dz = 0
    for event in pg.event.get():
        search_box.listen(event)
        if search_box.result is not None:
            srf = pg.image.load(search_box.result).convert_alpha()
            images_offline.append(srf)
            srf = pg.transform.smoothscale_by(srf, .5*WIDTH / srf.get_width())
            images_online.append(srf)
            pos.append(((WIDTH - srf.get_width())/2, (HEIGHT - srf.get_height())/2))
            width.append(srf.get_width())
            height.append(srf.get_height())
            scale.append(1.0)
            search_box.result = None

        if event.type == pg.MOUSEWHEEL:
            dz = 1.0 - event.y *.1

        if event.type == pg.MOUSEMOTION and event.buttons[0]:
            x0, y0 = event.pos
            dx, dy = event.rel

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    screen.fill(COLOR_BACKGROUND)

    locked = False
    for i, ((x, y), w, h, s, srf, srf_off) in enumerate(zip(pos, width, height, scale, images_online, images_offline)):
        if x < x0 < x + w and y < y0 < y + h and not locked:
            if dz != 0:
                scale[i] /= dz
                print(s)
                images_online[i] = pg.transform.smoothscale_by(srf_off, s)
            pos[i] = (x + dx, y + dy)
            locked = True
        screen.blit(srf, (x, y))

    search_box.draw(screen)
    pg.display.update()
