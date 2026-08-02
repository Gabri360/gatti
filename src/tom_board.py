import pygame as pg
from dataclasses import dataclass, astuple

import tom_colors as tc
import tom_state as ts
import tom_math as tm


@dataclass(slots=True)
class TomBoard:
    # Variables (camera)
    cam_pos: tm.Vec2
    cam_scale: float

    # Variables (images)
    img_count: int
    img_path: list[str]
    img_pos: list[tm.Vec2]
    img_srf_on: list[pg.Surface]
    img_srf_off: list[pg.Surface]
    img_size_on: list[tm.Vec2]
    img_size_off: list[tm.Vec2]
    img_scale: list[float]
    ifoc: int

    @classmethod
    def empty(cls):
        return cls(
            cam_pos=tm.Vec2(0.0, 0.0),
            cam_scale=1.0,
            img_count=0,
            img_path=[],
            img_pos=[],
            img_srf_on=[],
            img_srf_off=[],
            img_size_on=[],
            img_size_off=[],
            img_scale=[],
            ifoc=0
        )

    def add(self, path, srf, pos, scale):
        self.img_path.append(path)
        self.img_pos.append(pos)
        self.img_srf_on.append(pg.transform.smoothscale_by(srf, scale * self.cam_scale))
        self.img_srf_off.append(srf)
        self.img_size_on.append(tm.Vec2(*srf.get_size()) * scale)
        self.img_size_off.append(tm.Vec2(*srf.get_size()))
        self.img_scale.append(scale)
        self.img_count += 1

    def run(self, screen):

        running = True
        bg_color = tc.BG_MOVE

        while running:
            for event in pg.event.get():

                # globally pan the environment if no image is left clicked or by arbitrary right click
                if event.type == pg.MOUSEMOTION and ((event.buttons[0] and self.ifoc == self.img_count) or event.buttons[2]):
                    self.cam_pos -= tm.Vec2(*event.rel) / self.cam_scale

                # globally scale the environment if no image is focused
                elif event.type == pg.MOUSEWHEEL and self.ifoc == self.img_count:

                    # the mouse cursor is used as the center of the zoom (fixed point)
                    dz = 1.0 - event.y * 0.05
                    self.cam_pos += tm.Vec2(*pg.mouse.get_pos()) * (1 - dz) / self.cam_scale
                    self.cam_scale /= dz

                    # update the scales globally
                    for i in range(self.img_count):
                        scale_total = self.cam_scale * self.img_scale[i]
                        self.img_srf_on[i] = pg.transform.smoothscale_by(self.img_srf_off[i], scale_total)

                # unfocus an image by right click
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                    self.ifoc = self.img_count
                    bg_color = tc.BG_TRAVEL

                # focus an image by left click
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                    # if the cursor isn't clicking an image set the focus out of scale
                    self.ifoc = self.img_count
                    bg_color = tc.BG_TRAVEL

                    # check if cursor (projected into the image space) is contained inside any image
                    for i in reversed(range(0, self.img_count)):
                        cur_proj = tm.absto(tm.Vec2(*event.pos), self.cam_pos, self.cam_scale)
                        if (self.img_pos[i].x < cur_proj.x < self.img_pos[i].x + self.img_size_on[i].x and
                            self.img_pos[i].y < cur_proj.y < self.img_pos[i].y + self.img_size_on[i].y):

                            # push focused image to the top layer
                            self.img_pos.append(self.img_pos.pop(i))
                            self.img_path.append(self.img_path.pop(i))
                            self.img_srf_on.append(self.img_srf_on.pop(i))
                            self.img_srf_off.append(self.img_srf_off.pop(i))
                            self.img_size_on.append(self.img_size_on.pop(i))
                            self.img_size_off.append(self.img_size_off.pop(i))
                            self.img_scale.append(self.img_scale.pop(i))

                            self.ifoc = self.img_count - 1
                            bg_color = tc.BG_MOVE
                            break

                # pan an image by the dragged distance if an image is focused and the cursor is dragging
                elif self.ifoc < self.img_count and event.type == pg.MOUSEMOTION and event.buttons[0]:
                    self.img_pos[self.ifoc] += tm.Vec2(*event.rel) / self.cam_scale

                # scale the image if an image is foucsed and the mouse-wheel is rolling
                elif self.ifoc < self.img_count and event.type == pg.MOUSEWHEEL:

                    # the mouse cursor is used as the center of the zoom (fixed point)
                    cur_proj = tm.absto(tm.Vec2(*pg.mouse.get_pos()), self.cam_pos, self.cam_scale)
                    img_pos_rel = self.img_pos[self.ifoc] - cur_proj
                    self.img_pos[self.ifoc] = tm.absto(img_pos_rel, cur_proj, 1.0 - event.y * 0.05)
                    self.img_scale[self.ifoc] /= 1.0 - event.y * 0.05
                    self.img_size_on[self.ifoc] = self.img_size_off[self.ifoc] * self.img_scale[self.ifoc]

                    # update local scale
                    scale_total = self.cam_scale * self.img_scale[i]
                    self.img_srf_on[self.ifoc] = pg.transform.smoothscale_by(self.img_srf_off[self.ifoc], scale_total)

                # delete the image if an image is focused and the X key is pressed
                elif self.ifoc < self.img_count and event.type == pg.KEYDOWN and event.key == pg.K_x:
                    self.img_path.pop(self.ifoc)
                    self.img_srf_on.pop(self.ifoc)
                    self.img_srf_off.pop(self.ifoc)
                    self.img_pos.pop(self.ifoc)
                    self.img_size_on.pop(self.ifoc)
                    self.img_size_off.pop(self.ifoc)
                    self.img_scale.pop(self.ifoc)
                    self.img_count -= 1

                # check for transition events, they are triggered by a keyboard press
                if event.type == pg.KEYDOWN:

                    # switch to searching if the S key is pressed
                    if event.key == pg.K_s:
                        return ts.TomState.SEARCH

                    # exit program if the ESC key is pressed
                    if event.key == pg.K_ESCAPE:
                        return ts.TomState.EXIT

            # draw background
            screen.fill(bg_color)

            # draw images
            for i in range(self.img_count):
                img_pos_rel = tm.relto(self.img_pos[i], self.cam_pos, self.cam_scale)
                screen.blit(self.img_srf_on[i], astuple(img_pos_rel))
        
            pg.display.update()
