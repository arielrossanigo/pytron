import random

from bot import Bot, Action


class PlayerBot(Bot):
    def get_action(self, board):
        return random.choice(list(Action))
