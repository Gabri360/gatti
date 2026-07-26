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

while True:

    for event in pg.event.get():
        search_box.listen(event)
        if search_box.result is not None:
            srf = pg.image.load(search_box.result).convert_alpha()
            images_offline.append(srf)
            images_online.append(pg.transform.smoothscale_by(srf, .5*WIDTH / srf.get_width()))
            search_box.result = None
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    screen.fill(COLOR_BACKGROUND)
    for srf in images_online:
        screen.blit(srf, (0, 0))
    search_box.draw(screen)
    pg.display.update()
