import pygame as pg
from pygame import font
import sys
pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class Rect(object):
    def __init__(self, xc, yc, w, h):
        self.rect = pg.Rect(0, 0, w, h)
        self.rect.centerx = xc
        self.rect.centery = yc
        self.color = COLOR_INACTIVE


class Input(Rect):
    def __init__(self, text_color, xc, yc, w, h, Font=48):
        super().__init__(xc, yc, w, h)
        self.active = False
        self.done = False
        self.text = ''
        self.text_color = text_color
        self.font = font.SysFont(None, Font)
        self.image = self.font.render(self.text, True, self.text_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.x, self.image_rect.y = (self.rect.x+5, self.rect.y+5)
        self.input_str = self.text

    def input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.input_str = self.text
                    self.text = ''
                    self.done = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.image = self.font.render(self.text, True, self.text_color)
                self.image_rect = self.image.get_rect()
                self.image_rect.x, self.image_rect.y = (self.rect.x + 5, self.rect.y + 5)

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
        pg.draw.rect(screen, self.color, self.rect, 3)

    def update_rect(self):
        # Resize the box if the text is too long.
        width = max(200, self.image_rect.w + 10)
        self.rect.w = width

    def show(self, screen, stats, score_text):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            self.input(event)
        self.update_rect()
        screen.fill((0, 0, 70))
        title = pg.image.load('images/score2.png')
        title_rect = title.get_rect()
        title_rect.centerx = 650
        title_rect.centery = 280
        screen.blit(title, title_rect)
        score_text.draw_button(1)
        self.draw(screen)
        pg.display.flip()

