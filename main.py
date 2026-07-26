import json
import os
import pygame as pg
from search_box import SearchBox
from image_network import ImageNetwork
from camera import Camera


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
pg.display.set_caption("tom")
screen = pg.display.set_mode((WIDTH, HEIGHT))
cam = Camera(x=0, y=0, z=0)
search_box = SearchBox(
    font=pg.font.SysFont("Calibri", 16),
    buffer=ROOT,
    root=ROOT,
    neighbours=[ROOT + n for n in sorted(os.listdir(ROOT))],
    color_text=COLOR_TEXT,
    result=None
)
images = ImageNetwork(
    count=0,
    srf_on=[],
    srf_off=[],
    srf_pos=[],
    srf_size_on=[],
    srf_size_off=[],
    srf_zoom=[],
    ifoc=0
)

while True:
    for event in pg.event.get():
        search_box.listen(event)
        images.listen(event, cam)
        if not images.focused:
            cam.listen(event)
        if search_box.result is not None:
            srf = pg.image.load(search_box.result).convert_alpha()
            images.load(srf, WIDTH, HEIGHT)
            search_box.result = None

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    screen.fill(COLOR_BACKGROUND)
    images.draw(screen, cam)

    search_box.draw(screen)
    pg.display.update()
