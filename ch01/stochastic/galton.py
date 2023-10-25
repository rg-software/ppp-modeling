from random import randint

N = 100000
PEGS = 7

bins = [0 for _ in range(PEGS + 1)]

for _ in range(N):
    bin_idx = 0
    for _ in range(PEGS):
        if randint(0, 1) == 1:
            bin_idx += 1
    bins[bin_idx] += 1

print(f"bins: {bins}")
print(f"prob: {[b / N for b in bins]}")
