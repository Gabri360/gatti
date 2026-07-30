from dataclasses import dataclass
from camera import Vec2
import pygame as pg
import os


@dataclass(slots=True)
class SearchBox:
    pos: Vec2
    size: Vec2
    font: pg.font.Font
    partial: str
    root: str
    path: list[str]
    candidates: str
    color_text: str
    result: str

    def listen(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.partial = self.partial[:-1]
            elif event.key == pg.K_RETURN:
                self.partial = [n for n in self.candidates if self.partial in n[:len(self.partial)]][0]
                if os.path.isdir(self.root + '/'.join(self.path + [self.partial])):
                    self.path.append(self.partial)
                    self.partial = ""
                    self.candidates = [n for n in sorted(os.listdir(self.root + '/'.join(self.path + [self.partial])))]
                else:
                    self.result = self.root + '/'.join(self.path + [self.partial])
            else:
                self.partial += event.unicode

    def draw(self, screen):
        #pg.draw.rect(screen, self.color_text, (self.pos.x, self.pos.y, self.size.x, self.size.y), width=2)
        text = '/'.join(self.path + [self.partial])
        while self.font.size(text)[0] > self.size.x * 0.9:
            text = text[1:]
        screen.blit(self.font.render(text, antialias=True, color=self.color_text), (self.pos.x + (self.size.x - self.font.size(text)[0]) / 2, self.pos.y + (self.size.y - self.font.get_height()) / 2))
        alpha = 255 / 2
        for i, p in enumerate(n for n in self.candidates if self.partial in n):
            text = '/'.join(self.path + [p])
            srf = self.font.render(text, antialias=True, color=self.color_text)
            srf.set_alpha(alpha)
            screen.blit(srf, (self.pos.x + (self.size.x - self.font.size(text)[0]) / 2, self.pos.y + (self.size.y - self.font.get_height()) / 2 + (i + 1) * self.font.get_height()))
            alpha /= 2

    def update(self):
        pass
