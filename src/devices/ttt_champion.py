from random import choices
from dataclasses import dataclass

INIT_WEIGHT = 50
POS_REWARD = 5
NEG_REWARD = -5
LEARN_RATE = 0.8
PLAYER_SYMBOL = "X"
OPP_SYMBOL = "O" if PLAYER_SYMBOL == "X" else "X"


@dataclass
class Action:
    value: int
    weight: float = 1


@dataclass
class State:
    value: list
    actions: list

    @classmethod
    def create(cls, value):
        acts = [Action(i, INIT_WEIGHT) for i, v in enumerate(value) if v == " "]
        return cls(value, acts)

    def random_action(self):
        w = [a.weight for a in self.actions]
        return choices(self.actions, w)[0]

    def key(self):
        return tuple(self.value)

    def next(self, action, symbol):
        next_value = list(self.value)
        next_value[action.value] = symbol
        return State.create(next_value)

    def full(self):
        return " " not in self.value

    def rc(self, row, col):
        return self.value[row * 3 + col]

    def victory(self, sym):
        for k in range(3):
            h = sym == self.rc(k, 0) == self.rc(k, 1) == self.rc(k, 2)
            v = sym == self.rc(0, k) == self.rc(1, k) == self.rc(2, k)
            d1 = sym == self.rc(0, 0) == self.rc(1, 1) == self.rc(2, 2)
            d2 = sym == self.rc(2, 0) == self.rc(1, 1) == self.rc(0, 2)
            if h or v or d1 or d2:
                return True
        return False

    def game_over(self):
        return self.full() or self.victory("X") or self.victory("O")


def reward(history, score):
    r = score
    for action in reversed(history):
        action.weight = max(0.001, action.weight + r)
        r *= LEARN_RATE


knowledge = {}


def play_results():
    history = []
    sym = "X"
    state = State.create([" " for _ in range(9)])

    while not state.game_over():
        if sym == OPP_SYMBOL:
            action = State.create(state.value).random_action()
        else:
            if state.key() not in knowledge:
                knowledge[state.key()] = state

            action = knowledge[state.key()].random_action()
            history.append(action)

        state = state.next(action, sym)
        sym = "X" if sym == "O" else "O"

    pl_wins = state.victory(PLAYER_SYMBOL)
    opp_wins = state.victory(OPP_SYMBOL)
    is_draw = not (pl_wins or opp_wins)

    if pl_wins:
        reward(history, POS_REWARD)
    elif opp_wins:
        reward(history, NEG_REWARD)

    return [pl_wins, opp_wins, is_draw]


for _ in range(10):
    stats = [play_results() for _ in range(10000)]
    for k in range(3):
        print(sum(s[k] for s in stats), end=" ")
    print()
