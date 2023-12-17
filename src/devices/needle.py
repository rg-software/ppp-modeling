from random import choice
from time import time


def bf_search(pattern, text, start):
    for i in range(start, len(text) - len(pattern)):
        for j in range(len(pattern)):
            if pattern[j] != text[i + j]:
                break
        else:
            return i
    return -1


def fsm_search(rules, pattern, text, start):
    state = 0
    for i in range(start, len(text)):
        c = text[i]
        state = rules[(state, c)] if (state, c) in rules else 0
        if state == len(pattern):
            return i - (state - 1)
    return -1


def rules_for_pattern(pattern):
    rules = {}
    for c in set(pattern):
        rules.update(rules_for_char(pattern, c))
    return rules


def rules_for_char(pattern, c):
    rules = {}
    for sl in range(len(pattern) + 1):
        S = pattern[:sl]
        R = ""
        for rl in range(1, len(pattern) + 1):
            Rc = pattern[:rl]
            if pattern.startswith(Rc) and (S + c).endswith(Rc) and rl > len(R):
                R = Rc
                rules[(sl, c)] = rl
    return rules


TEXTLEN = 1000000
PATTERNLEN = 6
CHARS = "abcde"
text = "".join((choice(CHARS) for _ in range(TEXTLEN)))
pattern = "".join((choice(CHARS) for _ in range(PATTERNLEN)))

rules = rules_for_pattern(pattern)

start = time()
i = 0
cnt = 0
while (i := bf_search(pattern, text, i)) != -1:
    cnt += 1
    i += 1
bftime = time() - start

start = time()
i = 0
cnt = 0
while (i := fsm_search(rules, pattern, text, i)) != -1:
    cnt += 1
    i += 1
fsmtime = time() - start

print(f"matches found: {cnt}")
print(f"fsm speedup: {(bftime/fsmtime):.03}")
