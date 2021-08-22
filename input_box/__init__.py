import pygame as pg
from pygame import font
import sys
pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class Rect(object):
    """Uma classe que cria retângulos no pygame."""

    def __init__(self, xc, yc, w, h):
        """Inicializa os atributos típicos de um retângulo"""
        self.rect = pg.Rect(0, 0, w, h)
        self.rect.centerx = xc
        self.rect.centery = yc
        self.color = COLOR_INACTIVE


class Input(Rect):
    """Inicializa a classe Input que herdará de Rect."""

    def __init__(self, text_color, xc, yc, w, h, Font=48):
        """Inicia os atributos usados na criação de caixas de input."""
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
        """Checa eventos de mouse na caixa de input e, caso True, recolhe a informação."""
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
        """Desenha a imagem do input renderizado."""
        screen.blit(self.image, self.image_rect)
        pg.draw.rect(screen, self.color, self.rect, 3)

    def update_rect(self):
        """Atualiza o tamanho da caixa de input se o texto entrado for muito longo."""
        width = max(200, self.image_rect.w + 10)
        self.rect.w = width

    def show(self, screen, score_text):
        """Carrega a tela de recordes e pede o input do username"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            self.input(event)
        self.update_rect()
        screen.fill((0, 0, 70))
        title = pg.image.load('images/score2.png')
        title_rect = title.get_rect()
        title_rect.centerx = 650
        title_rect.centery = 320
        screen.blit(title, title_rect)
        score_text.draw_button(1)
        self.draw(screen)
        pg.display.flip()

