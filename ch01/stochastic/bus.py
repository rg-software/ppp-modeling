from random import uniform

N = 100000
DIST = 1000
DAYLEN = 24 * 3600

succ_count = 0
for _ in range(N):
    t = uniform(0, DAYLEN)
    src = uniform(0, DIST)
    dest = uniform(0, DIST)

    buspos = t % (2 * DIST)

    if buspos <= src < dest or buspos >= src > dest:
        succ_count += 1

print(succ_count / N)

# A - C - D - B
# A - D - C - B
