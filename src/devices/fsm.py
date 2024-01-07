def accepts(rules, favstates, start, input):
    state = start
    try:
        for c in input:
            state = rules[(state, c)]
        return state in favstates
    except KeyError:
        return False


rules = {
    (3, "C"): 1,
    (1, "C"): 1,
    (1, "A"): 5,
    (5, "A"): 2,
    (2, "B"): 1,
    (2, "C"): 4,
}

favs = {2}
start = 3

print(accepts(rules, favs, start, "CAAB"))
print(accepts(rules, favs, start, "CAABAA"))
