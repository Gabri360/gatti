from io import BytesIO
import tarfile
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

try:
    with tarfile.open("save.tom", "r:gz") as tar:
        cam = Camera.load(json.load(tar.extractfile("camera.json")))
        images = ImageNetwork.load(json.load(tar.extractfile("network.json")), cam)

except FileNotFoundError:
    cam = Camera.empty()
    images = ImageNetwork.empty()

search_box = SearchBox(
    font=pg.font.SysFont("Calibri", 16),
    partial="",
    root=ROOT,
    path=[],
    candidates=[n for n in sorted(os.listdir(ROOT))],
    color_text=COLOR_TEXT,
    result=None
)

while True:
    for event in pg.event.get():
        search_box.listen(event)
        #images.listen(event, cam)
        if not images.focused:
            cam.listen(event)
        #
        images.listen(event, cam)
        if search_box.result is not None:
            srf = pg.image.load(search_box.result).convert_alpha()
            images.add(search_box.result, srf, WIDTH, HEIGHT)
            search_box.result = None

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                # Save state
                with tarfile.open("save.tom", "w:gz") as tar:
                    # Camera
                    data = BytesIO(json.dumps(cam.dump(), indent=4).encode("utf-8"))
                    meta = tarfile.TarInfo("camera.json")
                    meta.size = data.getbuffer().nbytes
                    tar.addfile(meta, data)
                    # Network
                    data = BytesIO(json.dumps(images.dump(), indent=4).encode("utf-8"))
                    meta = tarfile.TarInfo("network.json")
                    meta.size = data.getbuffer().nbytes
                    tar.addfile(meta, data)
                pg.quit()
                exit()

    screen.fill(COLOR_BACKGROUND)
    images.draw(screen, cam)

    search_box.draw(screen)
    pg.display.update()
