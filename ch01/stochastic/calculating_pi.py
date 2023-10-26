from random import uniform


N = 100000
Nc = 0

for _ in range(N):
    x = uniform(0, 1.0)
    y = uniform(0, 1.0)
    if x * x + y * y < 1:
        Nc += 1

print(f"Pi is {4*Nc/N}")
