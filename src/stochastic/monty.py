from random import choice

N = 100000

player_a = 0
player_b = 0


def choose_empty(prize, options):
    if options == [False, False]:
        return choice(options)
    return options[1] if prize[options[0]] else options[0]


for _ in range(N):
    prize = [False, False, False]
    prize[choice([0, 1, 2])] = True

    options = [0, 1, 2]
    player_choice = choice(options)
    options.remove(player_choice)
    monty_choice = choose_empty(prize, options)
    options.remove(monty_choice)

    if prize[player_choice]:
        player_a += 1
    if prize[options[0]]:
        player_b += 1

print(f"Player A: {player_a/N}")
print(f"Player B: {player_b/N}")
