import pygame
from pygame.sprite import Sprite, Group
from time import sleep
from Alien_Invasion.alien import Alien
from random import choice
import Alien_Invasion.game_functions as gf


class Settings(Sprite):
    """Uma classe para armazenar todas as configurações da Invasão
    Alienígena."""

    def __init__(self):
        super().__init__()
        """Inicializa as configurações estáticas do jogo."""
        # Configurações da tela
        self.width = 1200
        self.height = 700
        self.bg_color = (0, 0, 70)
        self.image = pygame.image.load('images/initial_screen.png')
        self.rect = self.image.get_rect()
        self.time_before_game = 0
        self.game1_screen = pygame.image.load('images/game1_screen.png')
        self.rect_g1 = self.game1_screen.get_rect()
        self.help = pygame.image.load('images/help.png')
        self.help_image = self.help.get_rect()

        # Configurações da espaçonave
        self.ship_limit = 3

        # Configurações dos projéteis
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3

        # Configurações dos alienígenas
        self.fleet_drop_speed = 10

        # A taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1

        # A taxa com que os pontos para cada alienígena aumentam
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam no decorrer do
        jogo."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction igual a 1 representa a direita; -1 representa a esquerda
        self.fleet_direction = 1

        # Pontuação
        self.alien_points = 50

    def increase_speed(self):
        """Aumenta as configurações de velocidade."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def initial_screen(self, screen, stats, play_button, ai_settings, ship, help_button, x_button,
                       record_button, reset_scores):
        """Cria toda a interface da tela inicial"""
        self.help_image.centerx = help_button.rect.centerx
        self.help_image.centery = help_button.rect.centery + 110
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        if not stats.game_active:
            screen.blit(self.image, self.rect)
            # Desenha os botões play, help e record se o jogo estiver inativo
            play_button.draw_button(3)
            help_button.draw_button(3)
            record_button.draw_button(3)
            screen.blit(ship.image, ship.rect)
            if help_button.active:
                # Se o botão help for clicado, o botão x é chamado
                x_button.rect.x = self.help_image.right - 20
                x_button.rect.y = self.help_image.top
                x_button.msg_image_rect.x = self.help_image.right - 15
                x_button.msg_image_rect.y = self.help_image.top + 3
                screen.blit(self.help, self.help_image)
                x_button.draw_button(3)
            if record_button.active:
                # Se o botão record for clicado, o botão x e reset_scores são chamados
                reset_scores.draw_button(3)
                x_button.rect.x = self.help_image.right -38
                x_button.rect.y = self.help_image.top + 127
                x_button.msg_image_rect.x = self.help_image.right - 33
                x_button.msg_image_rect.y = self.help_image.top + 129
                x_button.draw_button(3)
                gf.button_record(screen, stats,ai_settings, record_button)
            # Cria os aliens aleatórios na tela inicial
            aliens = self.make_random_aliens(ai_settings, screen)
            pygame.display.flip()
            aliens.empty()
            sleep(0.75)
        else:
            image = pygame.image.load('images/ship.bmp')
            rect = image.get_rect()
            if ship.rect.centery > 100:
                ship.rect.centery -= self.ship_speed_factor
                screen.blit(ship.image, ship.rect)
            else:
                for i in range(3):
                    # Faz a contagem regressiva antes do jogo
                    image = pygame.image.load(f'images/game_mode1_{3-i}.png')
                    image_rect = image.get_rect()
                    screen.blit(image, image_rect)
                    pygame.display.flip()
                    sleep(1)
                    self.time_before_game += 1
            pygame.display.flip()

    def make_random_aliens(self, ai_settings, screen):
        aliens = Group()
        aliens.add(Alien(ai_settings, screen) for i in range(7))
        x = [10, 50, 80, 120, 150, 190, 230, 270, 355, 420, 498, 710, 779, 888, 950, 1030, 1120]
        y = [20, 50, 90, 170, 210, 440, 480, 530, 550, 575, 600]
        for alien in aliens.sprites():
            a = choice(x)
            b = choice(y)
            alien.rect.x = a
            alien.rect.y = b
            x.remove(a)
            y.remove(b)
        aliens.draw(screen)
        return aliens




