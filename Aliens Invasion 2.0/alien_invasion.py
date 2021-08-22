import pygame
from Alien_Invasion.settings import Settings
from Alien_Invasion.ship import Ship
import Alien_Invasion.game_functions as gf
from pygame.sprite import Group
from Alien_Invasion.game_stats import GameStats
from Alien_Invasion.button import Button
from Alien_Invasion.scoreboard import Scoreboard
from Alien_Invasion.input_box import Input


def run_game():
    # Inicializa o jogo e cria um objeto para a tela
    pygame.init()
    gf.initial_sound()
    set_inst = Settings()
    screen = pygame.display.set_mode((set_inst.width, set_inst.height ))
    pygame.display.set_caption("Alien Invasion")
    # Cria o botão Play
    play_button = Button((130, 35), screen, "PLAY", (set_inst.width//2, (set_inst.height//2)-60), Font=35)
    help_button = Button((130, 35), screen, 'HELP', (set_inst.width//2, set_inst.height//2), Font=35)
    x_button = Button((20, 20), screen, 'X', (set_inst.width//2, set_inst.height//2), Font=25)
    record_button = Button((130, 35), screen, 'RECORDS', (set_inst.width//2, (set_inst.height//2) + 60), Font=35)
    reset_scores = Button((130, 35), screen, 'RESET SCORES', (set_inst.width//2, (set_inst.height//2) + 120), Font=23)
    #Cria instância para armazenar estatísticas do jogo e cria painel de pontuação
    stats = GameStats(set_inst)
    sb = Scoreboard(set_inst, screen, stats)
    stats.high_scores = gf.read_scores()
    print(stats.high_scores)
    # Cria uma espaçonave, um grupo de projéteis e um grupo de alienígenas
    ship = Ship(set_inst, screen)
    bullets = Group()
    aliens = Group()
    # Cria a frota de alienígenas
    gf.create_fleet(set_inst, screen, ship, aliens)
    # Inicia o laço principal do jogo
    screen.fill((0, 0, 70))
    pygame.display.flip()
    text = Input((130, 0, 0), 600, 350, 140, 40)
    while True:
        if not stats.game_active:
            set_inst.initial_screen(screen, stats, play_button, set_inst, ship, help_button, x_button,
                                    record_button, reset_scores)
        gf.check_events(set_inst, screen, stats, sb, play_button, ship, aliens, bullets, help_button,
                        x_button, record_button, reset_scores)
        if stats.game_active:
            if set_inst.time_before_game < 3:
                set_inst.initial_screen(screen, stats, play_button, set_inst, ship, help_button, x_button,
                                        record_button, reset_scores)
            else:
                ship.update()
                gf.update_bullets(set_inst, screen, stats, sb, ship, aliens, bullets)
                gf.update_aliens(set_inst, stats, screen, sb, ship,  aliens, bullets, text)
                gf.update_screen(set_inst, screen, stats, sb, ship, aliens, bullets)
run_game()