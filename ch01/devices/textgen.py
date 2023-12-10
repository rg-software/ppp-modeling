from random import randint, choices
from collections import defaultdict
from pydoc_data.topics import topics

TOKENS = 50

input_text = " ".join(topics.values())
words_raw = input_text.split()
words = [w.lower() for w in words_raw if w.isalnum()]
freq = {}

for i in range(len(words) - 2):
    key, next_word = (words[i], words[i + 1]), words[i + 2]

    if key not in freq:
        freq[key] = defaultdict(int)

    freq[key][next_word] += 1

idx = randint(0, len(words) - 3)
next_pair = (words[idx], words[idx + 1])

for _ in range(TOKENS):
    w1, w2 = next_pair
    print(w1, end=" ")

    keys = list(freq[next_pair].keys())
    values = list(freq[next_pair].values())
    w3 = choices(keys, values)[0]

    next_pair = (w2, w3)
