from dataclasses import dataclass
import pygame as pg
import os


@dataclass(slots=True)
class SearchBox:
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
                self.partial = [n for n in self.candidates if self.partial in n][0]
                if os.path.isdir(self.root + '/'.join(self.path) + self.partial):
                    self.path.append(self.partial)
                    self.partial = ""
                    self.candidates = [n for n in sorted(os.listdir(self.root + '/'.join(self.path + [self.partial])))]
                else:
                    self.result = self.root + '/'.join(self.path + [self.partial])
            else:
                self.partial += event.unicode

    def draw(self, screen):
        screen.blit(self.font.render('/'.join(self.path + [self.partial]), antialias=True, color=self.color_text), (0, 0))
        for i, p in enumerate(n for n in self.candidates if self.partial in n):
            srf = self.font.render('/'.join(self.path + [p]), antialias=True, color=self.color_text)
            srf.set_alpha(80)
            screen.blit(srf, (0, (i + 1) * self.font.get_height()))

    def update(self):
        pass
