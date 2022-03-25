import random

from bot import Bot


class PlayerBot(Bot):
    def get_action(self, board):
        return random.choice(self.possible_actions(board))
