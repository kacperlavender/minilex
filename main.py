from collections import defaultdict
import random
import math

def generate(start_char, length):
    result = [start_char]
    current = start_char

    for _ in range(length - 1):
        if current not in probs:
            break

        next_chars = list(probs[current].keys())
        weights = list(probs[current].values())

        current = random.choices(next_chars, weights=weights, k=1)[0]
        result.append(current)

    return ''.join(result)

def perplexity(test_text):
    log_prob = 0.0
    count = 0

    for i in range(len(test_text) - 1):
        a = test_text[i]
        b = test_text[i + 1]

        p = probs.get(a, {}).get(b, None)

        if p is None or p == 0:
            p = 1e-10
        
        log_prob += math.log(p)
        count += 1
    return math.exp(-log_prob / count)

text = open("pan_tadeusz.txt", encoding="utf-8").read()
chars = sorted(set(text))

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

counts = defaultdict(lambda: defaultdict(int))

for i in range(len(text) - 1):
    a = text[i]
    b = text[i + 1]

    counts[a][b] += 1

probs = {}

for a in counts:
    total = sum(counts[a].values())
    probs[a] = {b: count/total for b, count in counts[a].items()}

for i in range(3):
    seed = random.choice(list(probs.keys()))
    print(f"[Seed: {seed}]: {generate(seed, 50)}")
    print()

print(f"perplexity na korpusie: {perplexity(text):.2f}")
print(f"perplexity na 'Soplica ': {perplexity('Soplica '):.2f}")
print(f"perplexity na 'xyz123': {perplexity('xyz123'):.2f}")