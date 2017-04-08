import numpy as np
import random


class Player(object):

    def __init__(self, board, win_len=3, name=None, order=None):
        self.board = board
        self.free_fields = self.get_free_fields()
        self.win_len = win_len
        self.order = order
        if name is None:
            self.name = self.generate_name()

    def generate_name(self):
        name = 'Player{}{}'.format(self.order, self.__class__.__name__)
        return name

    def get_free_fields(self):
        return list(zip(*np.where(self.board == 0)))

    def attack(self, current_board=None, previous_attacks=None):
        self.board = current_board
        self.free_fields = self.get_free_fields()


class Human(Player):
    def attack(self, current_board=None, previous_attacks=None):
        super(Human, self).attack(current_board=current_board, previous_attacks=previous_attacks)
        while True:
            try:
                move = tuple(int(i) for i in input('Your turn from {}: '.format(self.free_fields)).split(','))
            except Exception as e:
                print(e)
                continue
            if move in self.free_fields:
                return move


class Bot(Player):
    def __init__(self, board, win_len=3, name=None, order=None):
        super(Bot, self).__init__(board, win_len=win_len, name=name, order=order)
        assert self.has_ai(), 'We do not have AI for board {shape.0}x{shape.1} ' \
                              'with length of winning line {win_len}'.format(shape=self.board.shape, win_len=win_len)

    def has_ai(self):
        return self.board.shape == (3, 3) and self.win_len == 3

    def attack(self, current_board=None, previous_attacks=None):
        super(Bot, self).attack(current_board, previous_attacks)
        # TODO: AI should be better :)
        move = random.choice(self.free_fields)
        return move

    def can_win_this_turn(self):
        pass

    def can_loose_next_turn(self):
        pass

class Game(object):
    PVP, PVM, MVM = range(3)
    MODES = {
        PVP: [Human, Human],
        PVM: [Human, Bot],
        MVM: [Bot, Bot],
    }

    def __init__(self, width=3, height=3, win_len=3, mode=PVM, first_attack=None):
        assert win_len <= width and win_len <= height, 'Winning line can not be larger than board dimensions'
        self.board = np.zeros((width, height), dtype=np.uint8)
        self.win_len = win_len
        self.turn_to_attack = first_attack or random.getrandbits(1)
        self.players = [player(self.board, win_len=win_len, order=self.turn_to_attack+1) for player in self.MODES[mode]]
        self.attacks = []

    def play(self):
        while True:
            player = self.players[self.turn_to_attack]
            move = player.attack(current_board=self.board, previous_attacks=self.attacks)
            self.attacks.append(move)


if __name__ == '__main__':
    first_attack = None
    while True:
        game = Game(first_attack=first_attack)
