import json
import os
import pygame as pg


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
font = pg.font.SysFont("Calibri", 16)
buffer = ROOT
neighbours = [buffer + n for n in os.listdir(buffer)]

images_offline = []
images_online = []
pos = []

while True:

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == pg.K_RETURN:
                buffer = [n for n in neighbours if buffer in n][0]
                if os.path.isdir(buffer):
                    buffer += '/'
                    neighbours = [buffer + n for n in os.listdir(buffer)]
                else:
                    srf = pg.image.load(path).convert_alpha()
                    images_offline.append(srf)
                    images_online.append(pg.transform.smoothscale_by(srf, .5*WIDTH / srf.get_width()))
            else:
                buffer += event.unicode

    screen.fill(COLOR_BACKGROUND)
    for srf in images_online:
        screen.blit(srf, (0, 0))
    screen.blit(font.render(buffer, antialias=True, color=COLOR_TEXT), (0, 0))
    for i, path in enumerate(n for n in neighbours if buffer in n):
        screen.blit(font.render(path, antialias=True, color=COLOR_TEXT), (0, (i + 1) * font.get_height()))
    pg.display.update()
