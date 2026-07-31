from io import BytesIO
import tarfile
import json
import os
import pygame as pg
from enum import Enum, auto
from search_box import SearchBox
from image_network import ImageNetwork
from camera import Camera, Vec2


with open("palette.json", "r") as file:
    palette = json.load(file)
    COLOR_BG_TRAVEL = palette["background-travel"]
    COLOR_BG_MOVE = palette["background-move"]
    COLOR_BG_SEARCH = palette["background-search"]
    COLOR_TEXT = palette["text"]
    

with open("settings.json", "r") as file:
    settings = json.load(file)
    WIDTH = settings["width"]
    HEIGHT = settings["height"]
    ROOT = settings["root"]


class State(Enum):
    TRAVEL = auto()
    MOVE = auto()
    SEARCH = auto()


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
    pos=Vec2(WIDTH/2, HEIGHT/2),
    size=Vec2(WIDTH / 2, HEIGHT / 12),
    font=pg.font.SysFont("Calibri", 24),
    partial="",
    root=ROOT,
    path=[],
    candidates=[n for n in sorted(os.listdir(ROOT))],
    color_text=COLOR_TEXT,
    result=None
)

state = State.TRAVEL
color_bg = COLOR_BG_TRAVEL
opaque = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
opaque.fill("#000000")
opaque.set_alpha(100)
blur = pg.Surface((WIDTH, HEIGHT))
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
                    images.add(search_box.result, srf, WIDTH, HEIGHT, cam)
                    search_box.result = None
                    state = State.MOVE
                    color_bg = COLOR_BG_MOVE

        if event.type == pg.MOUSEWHEEL:
            images.update(cam)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s and state != State.SEARCH:
                state = State.SEARCH
                blur = pg.transform.gaussian_blur(screen, 20)
                color_bg = COLOR_BG_SEARCH
            if event.key == pg.K_ESCAPE:
            #if event.key == pg.K_s or event.key == pg.K_ESCAPE:
                #if event.key == pg.K_s:
                #    pg.image.save(screen, "tom.png")
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

    screen.fill(color_bg)
    images.draw(screen, cam)
    if state == State.SEARCH:
        screen.blit(blur, (0, 0))
        screen.blit(opaque, (0, 0))
        search_box.draw(screen)

    pg.display.update()
