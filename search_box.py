from dataclasses import dataclass
import pygame as pg
import os


@dataclass(slots=True)
class SearchBox:
    font: pg.font.Font
    buffer: str
    root: str
    neighbours: str
    color_text: str
    result: str

    def listen(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.buffer = self.buffer[:-1]
            elif event.key == pg.K_RETURN:
                self.buffer = [n for n in self.neighbours if self.buffer in n][0]
                if os.path.isdir(self.buffer):
                    self.buffer += '/'
                    self.neighbours = [self.buffer + n for n in sorted(os.listdir(self.buffer))]
                else:
                    self.result = self.buffer
            else:
                self.buffer += event.unicode

    def draw(self, screen):
        screen.blit(self.font.render(self.buffer, antialias=True, color=self.color_text), (0, 0))
        for i, path in enumerate(n for n in self.neighbours if self.buffer in n):
            srf = self.font.render(path, antialias=True, color=self.color_text)
            srf.set_alpha(80)
            screen.blit(srf, (0, (i + 1) * self.font.get_height()))

    def update(self):
        pass
