import importlib
import json
import random
from collections import defaultdict
from itertools import zip_longest


def state_to_tuple(state):
    return tuple((tuple(path) for path in state))


class PytronEngine:
    def __init__(self, bots, n_rows=10, n_columns=10):
        # state is a tuple of bots paths.
        # each bot path is a tuple of (row, column)
        self.bots = bots
        self.dead_bots = set()
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.init_state(bots)
        self.scores = None

    def init_state(self, bots):
        self.state = []
        self.used_positions = set()
        for _ in bots:
            while True:
                row_number = random.randint(1, self.n_rows - 1)
                col_number = random.randint(1, self.n_columns - 1)
                position = (row_number, col_number)
                if position not in self.used_positions:
                    break
            self.state.append([position])
            self.used_positions.add(position)

    def play(self):
        while not self.game_finished():
            actions = []
            current_state = state_to_tuple(self.state)
            for bot_id, bot in enumerate(self.bots):
                if bot_id in self.dead_bots:
                    action = self.state[bot_id][-1]
                else:
                    action = bot.get_action(current_state)
                    action = self.get_valid_action(action, bot_id)
                actions.append(action)

            self.apply_actions(actions)

        # scores are the number of steps the bot survive
        self.scores = [len(set(path)) for path in self.state]

    def game_finished(self):
        return len(self.bots) == len(self.dead_bots)

    def apply_actions(self, actions):
        by_position = defaultdict(list)

        for bot_id, action in enumerate(actions):
            # if someone goes outside of the board, it lose
            row, col = action
            if not 0 <= row <= self.n_rows or not 0 <= col <= self.n_columns:
                self.dead_bots.add(bot_id)

            # if someone crash some tail, it lose
            if action in self.used_positions:
                self.dead_bots.add(bot_id)

            # if 2 or more bots goes to the same place, all lose
            by_position[action].append(bot_id)

        # if 2 or more bots goes to the same place, all lose
        for action, bots in by_position.items():
            if len(bots) > 1:
                self.dead_bots = self.dead_bots.union(set(bots))

        # now it is possible to really apply the actions of no deads bots
        for bot_id, action in enumerate(actions):
            # add the head of the pytron
            self.state[bot_id].append(action)
            self.used_positions.add(action)

    def get_valid_action(self, action, bot_id):
        prev_action = self.state[bot_id][-1]
        prev_row, prev_column = prev_action

        # valid action, has manhattan distance of 1
        if action is not None and abs(action[0] - prev_row) + abs(action[1] - prev_column) == 1:
            return action

        # if action is not valid, we mantain the current direction (if it's possible)
        if len(self.state[bot_id]) == 1:
            direction = (1, 0)  # it moves down because sofi saids
        else:
            pprev_action = self.state[bot_id][-2]
            pprev_row, pprev_column = pprev_action
            direction = prev_row - pprev_row, prev_column - pprev_column

        action = prev_row + direction[0], prev_column + direction[1]
        return action


def load_bot(bot_id, bot_name):
    module = importlib.import_module(f'bots.{bot_name}.main')
    bot = module.PlayerBot(bot_id, bot_name)
    return bot


class Match:
    'Class to keep bots, engine and scores'
    def __init__(self, bots_names, size):
        self.bots_names = bots_names
        self.size = size
        self.bots = [load_bot(bot_id, bot) for bot_id, bot in enumerate(bots_names)]
        self.engine = PytronEngine(self.bots, size, size)

    def play(self):
        self.engine.play()

    def save(self, filename):
        if not self.engine.game_finished():
            raise Exception("Play the match first")

        steps = []
        for players_positions in zip_longest(*self.engine.state):
            steps.append(players_positions)

        by_bot = [(self.bots[bot_id].name, score)
                  for bot_id, score in enumerate(self.engine.scores)]
        score_board = sorted(by_bot, key=lambda x: x[1], reverse=True)

        result = {
            'speed': 500,
            'size': self.size,
            'steps': steps,  # step, players, positions
            'score_board': score_board
        }
        with open(filename, 'wt', encoding='utf-8') as f:
            json.dump(result, f)
