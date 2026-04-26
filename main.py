from collections import defaultdict

text = open("pan_tadeusz.txt", encoding="utf-8").read()

# print(text[:500])
print(f"liczba znakow: {len(text)}")

chars = sorted(set(text))

print(f"unikalnych znakow: {len(chars)}")
print(chars)

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

print(stoi['a'])
print(itos[1])


counts = defaultdict(lambda: defaultdict(int))

for i in range(len(text) - 1):
    a = text[i]
    b = text[i + 1]

    counts[a][b] += 1

after_z = sorted(counts['z'].items(), key=lambda x:x[1], reverse=True)

print(after_z[:10])

probs = {}

for a in counts:
    total = sum(counts[a].values())
    probs[a] = {b: count / total for b, count in counts[a].items()}

print(sum(probs['z'].values()))
