from random import randint

N = 10000


def turn_score(target):
    r = 0
    while r < target:
        die = randint(1, 6)
        if die == 1:
            return 0
        r += die
    return r


best_target = 0
best_total = 0

for target in range(1, 101):
    total = 0
    for _ in range(N):
        total += turn_score(target)

    if total > best_total:
        best_total, best_target = total, target

print(f"best target: {best_target}, best total (avg): {best_total/N}")
