from random import uniform

N = 100000
DIST = 10
DAYLEN = 5 * 2 * DIST  # 5 loops

wins = 0
for _ in range(N):
    t = uniform(0, DAYLEN)
    src = uniform(0, DIST)
    dst = uniform(0, DIST)
    busloc = t % (2 * DIST)

    bus_sbs = src <= busloc <= 2 * DIST - src
    bus_sas = busloc <= src or busloc >= 2 * DIST - src

    if src >= dst and bus_sbs or src < dst and bus_sas:
        wins += 1

print(wins / N)
