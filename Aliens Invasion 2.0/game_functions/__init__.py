import sys
import pygame
from Alien_Invasion.bullets import Bullet
from Alien_Invasion.alien import Alien
from time import sleep
from Alien_Invasion.button import Button
import collections
pygame.init()
pygame.mixer.init()
bullet = pygame.mixer.Sound(file='sounds/bullet.wav')
blowup = pygame.mixer.Sound(file='sounds/blowup.wav')


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, text):
    """Responde ao fato de a espaçonave ter sido atingida por um
    alienígena."""
    if stats.ships_left >= 1:
        # Decrementa ships_left
        stats.ships_left -= 1

        # Atualiza o painel de pontuações
        sb.prep_ships()

        # Esvazia a lista de alienígenas e de projéteis
        aliens.empty()
        bullets.empty()
        # Cria uma nova frota e centraliza a espaçonave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship(screen)
        # Faz uma pausa
        sleep(0.5)
    else:
        if not text.done:
            pygame.mouse.set_visible(True)
            store_score(stats, screen, text)
        text.done = False
        stats.game_active = False
        ship.center_ship(screen)


def get_number_aliens_x(ai_settings, alien_width):
    """Determina o número de alienígenas que cabem em uma linha."""
    available_space_x = ai_settings.width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Cria um alienígena e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de alienígenas."""
    # Cria um alienígena e calcula o número de alienígenas em uma linha
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = 4
    # Cria a frota de alienígenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a pressionamentos de tecla."""
    global pause
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        pause = True
        image = pygame.image.load('images/pause.png')
        rect = image.get_rect()
        rect.centerx = 300
        rect.centery = 25
        screen.blit(image, rect)
        pygame.display.flip()
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
                if event.type == pygame.QUIT:
                    sys.exit()
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara um projétil se o limite ainda não foi alcançado."""
    # Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.Sound.play(bullet)


def check_keyup_events(event, ship):
    """Responde a solturas de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, help_button,
                 x_button, record_button, reset_score):
    # Observa eventos de teclado e de mouse
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button(ai_settings, screen, stats, sb, ship, aliens, bullets, mouse_x,
                         mouse_y, play_button, help_button, x_button, record_button, reset_score)


def check_button(ai_settings, screen, stats, sb, ship,
                aliens, bullets, mouse_x, mouse_y, play_button, help_button,
                 x_button, record_button, reset_score):
    """Inicia um novo jogo quando o jogador clicar em Play."""
    play_button_clicked = play_button.clicked(mouse_x, mouse_y)
    help_button_clicked = help_button.clicked(mouse_x, mouse_y)
    x_button_clicked = x_button.clicked(mouse_x, mouse_y)
    record_button_clicked = record_button.clicked(mouse_x, mouse_y)
    reset_score_clicked = reset_score.clicked(mouse_x, mouse_y)
    if not stats.game_active:
        if play_button_clicked:
            # Reinicia as configurações do jogo
            ai_settings.initialize_dynamic_settings()

            # Oculta o cursor do mouse
            pygame.mouse.set_visible(False)

            # Reinicia os dados estatísticos do jogo
            stats.reset_stats()
            stats.game_active = True

            # Reinicia as imagens do painel de pontuação
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Esvazia a lista de alienígenas e de projéteis
            aliens.empty()
            bullets.empty()

            # Cria uma nova frota e centraliza a espaçonave
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship(screen)
        elif help_button_clicked:
            help_button.active = True
        elif x_button_clicked:
            help_button.active = False
            record_button.active = False
        elif record_button_clicked:
            record_button.active = True
        elif reset_score_clicked:
            stats.high_scores.clear()
            stats.high_scores = collections.OrderedDict()
            for i in range(1, 5):
                stats.high_scores[f'Empty{i}'] = '0'
            with open('high_score.text', 'wt') as file:
                for k, v in stats.high_scores.items():
                    file.write(f'{k};{v}\n')
            record_button.active = False


def update_screen(ai_settings, screen, stats, sb, ship, alien, bullets):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem pelo laço
    screen.fill(ai_settings.bg_color)
    # Redesenha todos os projéteis atrás da espaçonave e dos alienígenas
    if stats.game_active:
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        alien.draw(screen)
        # Desenha a informação sobre pontuação
        sb.show_score()
    # Deixa a tela mais recente visível
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza a posição dos projéteis e se livra dos projéteis
    antigos."""
    if stats.game_active:
        # Atualiza as posições dos projéteis
        bullets.update()
        # Livra-se dos projéteis que desapareceram
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        check_bullet_alien_collisions(ai_settings, screen, stats, sb,  ship, aliens,
                                      bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):
    """Responde a colisões entre projéteis e alienígenas."""
    # Remove qualquer projétil e alienígena que tenham colidido
    collisions = pygame.sprite.groupcollide(bullets, aliens, True,
                                            False)
    if collisions:
        for aliens_exploded in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens_exploded)
            sb.prep_score()
            pygame.mixer.Sound.play(blowup)
            for alien in aliens_exploded:
                alien_explode(alien, screen, aliens)
        check_high_score(stats, sb)
    elif len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        # Destrói os projéteis existentes e cria uma nova frota
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def alien_explode(alien, screen, aliens):
    x = alien.rect.x
    y = alien.rect.y
    alien.image = pygame.image.load('images/alien_explode.bmp')
    alien.rect = alien.image.get_rect()
    alien.rect.x = x
    alien.rect.y = y
    screen.blit(alien.image, alien.rect)
    pygame.display.flip()
    aliens.remove(alien)


def check_high_score(stats, sb):
    """Verifica se há uma nova pontuação máxima."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alienígena alcançou uma
    borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e muda a sua direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, sb,  ship, aliens, bullets, text):
    """
    Verifica se a frota está em uma das bordas
    e então atualiza as posições de todos os alienígenas da frota.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Verifica se houve colisões entre alienígenas e a espaçonave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, text)
    # Verifica se há algum alienígena que atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
                        bullets, text)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
                        bullets, text):
    """Verifica se algum alienígena alcançou a parte inferior da
    tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esse caso do mesmo modo que é feito quando a espaçonave é atingida
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, text)
            break


def initial_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/background.wav')
    pygame.mixer.music.play(-1)


def store_score(stats, screen, text):
    score = '{:,}'.format(int(stats.score))
    score_text = Button((200, 40), screen, score, (770, 235), (0, 0, 70), (130, 0, 0), 35)
    stats.input_active = True
    highscores = stats.high_scores
    points = list(highscores.values())
    for k, score in enumerate(points):
        if int(score) < stats.score:
            points.insert(k, stats.score)
            while not text.done:
                text.show(screen, stats, score_text)
            highscores[text.input_str] = stats.score
            highscores = sort_high_scores(highscores)
            break
    with open('game_stats/high_score.text', 'wt') as file:
        for k, v in highscores.items():
            file.write(f'{k};   {v}\n')
    stats.high_scores = highscores


def button_record(screen, stats, set_inst, record_button):
    if record_button.active:
        text=''
        buttons = []
        x = 0
        for k, v in stats.high_scores.items():
            str_i = "{:,}".format(int(v))
            text = f'{k:<10}' + f'{str_i:^10}'
            text = text.upper()
            texto = Button((230, 50), screen, text, (set_inst.width//2, (set_inst.height//2) + 192+x),
                       (0, 0, 70), (130, 0, 0),28)
            buttons.append(texto)
            x += 40
        for button in buttons:
            button.draw_button(1)


def sort_high_scores(highscores):
    from operator import itemgetter
    draft = sorted(highscores.items(), key=itemgetter(1), reverse=True)
    highscores.clear()
    highscores = collections.OrderedDict()
    for i in draft:
        highscores[f'{i[0]}'] = i[1]
    if len(highscores) > 4:
        highscores.popitem()
    return highscores


def read_scores():
    with open('game_stats/high_score.text', 'r+') as file:
        high_scores = collections.OrderedDict()
        for line in file.readlines():
            if line != '\n':
                kv = line.strip().split(';')
                high_scores[kv[0]] = (int(kv[1]))
        return high_scores
