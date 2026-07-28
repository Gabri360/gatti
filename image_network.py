import pygame as pg
from camera import Vec2
from dataclasses import dataclass, field


@dataclass(slots=True)
class ImageNetwork:
    # image count
    count: int
    # paths
    paths: list[str]
    # online images
    srf_on: list[pg.Surface]
    # offline images
    srf_off: list[pg.Surface]
    # position images
    srf_pos: list[Vec2]
    # size online images
    srf_size_on: list[Vec2]
    # size offline images
    srf_size_off: list[Vec2]
    # zoom images
    srf_zoom: list[float]
    # focused image index
    ifoc: int

    @property
    def focused(self):
        return self.ifoc < self.count

    @classmethod
    def empty(cls):
        return cls(
            count=0,
            paths=[],
            srf_on=[],
            srf_off=[],
            srf_pos=[],
            srf_size_on=[],
            srf_size_off=[],
            srf_zoom=[],
            ifoc=0
        )

    @classmethod
    def load(cls, d, cam):
        paths = []
        srf_on = []
        srf_off = []
        srf_pos = []
        srf_size_on = []
        srf_size_off = []
        srf_zoom = []
        for img in d:
            srf = pg.image.load(img["path"]).convert_alpha()
            s = img["z"]
            paths.append(img["path"])
            srf_on.append(pg.transform.smoothscale_by(srf, s * cam.z))
            srf_off.append(srf)
            srf_pos.append(Vec2(img["x"], img["y"]))
            srf_size_on.append(Vec2(img["w"] * s, img["h"] * s))
            srf_size_off.append(Vec2(img["w"], img["h"]))
            srf_zoom.append(s)
        return cls(len(d), paths, srf_on, srf_off, srf_pos, srf_size_on, srf_size_off, srf_zoom, len(d))

    def dump(self):
        d = []
        for i in range(self.count):
            d.append({
                "path": self.paths[i],
                "x": self.srf_pos[i].x,
                "y": self.srf_pos[i].y,
                "z": self.srf_zoom[i],
                "w": self.srf_size_off[i].x,
                "h": self.srf_size_off[i].y
            })
        return d


    def listen(self, event, cam):

        if event.type == pg.MOUSEWHEEL and not self.focused:
            for i in range(self.count):
                self.srf_on[i] = pg.transform.smoothscale_by(self.srf_off[i], cam.z * self.srf_zoom[i])

        if event.type == pg.MOUSEWHEEL and self.focused:
            x, y = pg.mouse.get_pos()
            cur_proj = cam.posabs(Vec2(x, y))

            self.srf_pos[self.ifoc].x -= cur_proj.x
            self.srf_pos[self.ifoc].y -= cur_proj.y

            self.srf_zoom[self.ifoc] /= 1.0 - event.y * 0.05
            self.srf_size_on[self.ifoc].x = self.srf_size_off[self.ifoc].x * self.srf_zoom[self.ifoc]
            self.srf_size_on[self.ifoc].y = self.srf_size_off[self.ifoc].y * self.srf_zoom[self.ifoc]

            self.srf_pos[self.ifoc].x /= 1.0 - event.y * 0.05
            self.srf_pos[self.ifoc].y /= 1.0 - event.y * 0.05
            self.srf_pos[self.ifoc].x += cur_proj.x
            self.srf_pos[self.ifoc].y += cur_proj.y
            self.srf_on[self.ifoc] = pg.transform.smoothscale_by(self.srf_off[self.ifoc], cam.z * self.srf_zoom[self.ifoc])

        elif event.type == pg.MOUSEMOTION and event.buttons[0]:
            self.ifoc = self.count
            for i in reversed(range(0, self.count)):
                cur_proj = cam.posabs(Vec2(event.pos[0], event.pos[1]))
                if self.pt_in_box(cur_proj, self.srf_pos[i], self.srf_size_on[i]):
                    self.srf_pos[i].x += cam.lenabs(event.rel[0])
                    self.srf_pos[i].y += cam.lenabs(event.rel[1])
                    self.ifoc = i
                    break

    def draw(self, screen, cam):
        for i in range(self.count):
            pos = cam.posrel(self.srf_pos[i])
            screen.blit(self.srf_on[i], (pos.x, pos.y))

    def add(self, path, srf_off, win_width, win_height):
        self.paths.append(path)
        self.srf_off.append(srf_off)
        self.srf_size_off.append(Vec2(
            x=srf_off.get_width(),
            y=srf_off.get_height()
        ))
        init_scale = 0.5 * win_width / srf_off.get_width()
        self.srf_zoom.append(init_scale)
        srf_on = pg.transform.smoothscale_by(srf_off, init_scale)
        self.srf_on.append(srf_on)
        self.srf_pos.append(Vec2(
            (win_width - srf_on.get_width()) / 2,
            (win_height - srf_on.get_height()) / 2
        ))
        self.srf_size_on.append(Vec2(
            x=srf_on.get_width(),
            y=srf_on.get_height()
        ))
        self.count += 1

    @staticmethod
    def pt_in_box(pt_pos, box_pos, box_size):
        return (
            (box_pos.x < pt_pos.x < box_pos.x + box_size.x) and
            (box_pos.y < pt_pos.y < box_pos.y + box_size.y)
        )
