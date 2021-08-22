class GameStats(object):
    """Armazena dados estatísticos da Invasão Alienígena."""
    def __init__(self, ai_settings):
        """Inicializa os dados estatísticos."""
        # A pontuação máxima jamais deverá ser reiniciada
        with open('game_stats/high_score.text', 'rt') as file:
            self.high_score = file.readline().strip().split(';')[1]
        self.high_score = int(self.high_score)
        self.high_scores = 0
        self.level = 1
        self.ai_settings = ai_settings
        self.reset_stats()
        # Inicia a Invasão Alienígena em um estado inativo
        self.game_active = False
        self.input_active = False

    def reset_stats(self):
        """Inicializa os dados estatísticos que podem mudar durante o
        jogo."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0
        self.ai_settings.time_before_game = 0