from pytron.bot import Bot, Action


class PlayerBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_cycles = 0
        self.n_forwards = 0
        self.n_current_forwards = 0

    def get_action(self, board):
        if self.n_current_forwards == self.n_forwards:
            if self.n_cycles == 1:
                self.n_cycles = 0
                self.n_forwards += 1
            else:
                self.n_cycles += 1
            self.n_current_forwards = 0
            return Action.Right
        self.n_current_forwards += 1
        return Action.Forward
