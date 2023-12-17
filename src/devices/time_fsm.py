def accepts(rules, favstates, start, input):
    state = start
    try:
        for c in input:
            state = rules[(state, c)]
        return state in favstates
    except KeyError:
        return False


def rules_range(state_from, state_to, minchar, maxchar):
    r = range(ord(minchar), ord(maxchar) + 1)
    return {(state_from, chr(c)): state_to for c in r}


# hours
rules = {(1, "2"): 2}
rules.update(rules_range(1, 3, "0", "1"))
rules.update(rules_range(2, 4, "0", "3"))
rules.update(rules_range(3, 4, "0", "9"))

rules.update({(4, ":"): 5})

# minutes
rules.update(rules_range(5, 6, "0", "5"))
rules.update(rules_range(6, 7, "0", "9"))

rules.update({(7, ":"): 8})

# seconds
rules.update(rules_range(8, 9, "0", "5"))
rules.update(rules_range(9, 10, "0", "9"))

rules.update({(10, "."): 11})

# milliseconds
rules.update(rules_range(11, 12, "0", "9"))
rules.update(rules_range(12, 13, "0", "9"))
rules.update(rules_range(13, 14, "0", "9"))

start = 1
favs = {7, 10, 14}

print(accepts(rules, favs, start, "23:15"))  # True
print(accepts(rules, favs, start, "24:15"))  # False
print(accepts(rules, favs, start, "09:37"))  # True
print(accepts(rules, favs, start, "23:95"))  # False
print(accepts(rules, favs, start, "00:15:23"))  # True
print(accepts(rules, favs, start, "05:23:59.234"))  # True
