import pygame.font


class Button(object):
    """Uma classe que cria objetos botões para a interação do usuário"""

    def __init__(self, set, screen, msg, pos, button_color=(255, 255, 255),
                 text_color=(0, 0, 70), Font=48):
        """Inicializa os atributos do botão."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # Define as dimensões e as propriedades do botão
        self.width, self.height = set
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, Font)
        # Constrói o objeto rect do botão e o centraliza
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = pos
        # A mensagem do botão deve ser preparada apenas uma vez
        self.prep_msg(msg)
        self.active = False

    def prep_msg(self, msg):
        """Transforma msg em imagem renderizada e centraliza o texto no
        botão."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, button_rect_width):
        """Desenha um botão com a cor desejada e, em seguida, desenha a mensagem"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        pygame.draw.rect(self.screen, (170, 0, 0), self.rect, button_rect_width)

    def clicked(self, mouse_x, mouse_y):
        """Verifica se o botão foi clicado"""
        return True if self.rect.collidepoint(mouse_x, mouse_y) else False

