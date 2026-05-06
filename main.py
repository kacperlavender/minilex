from collections import defaultdict
import random
import math
from pathlib import Path

# https://wolnelektury.pl/katalog/lektury/

_FILES = [f.name for f in Path("data").glob("*.txt")]

class Markov:
    def __init__(self, text, n = 3):
        self.text = text
        self.n = n
        self.probs = self._build_probs(text)
    
    def _build_probs(self, text):
        counts = defaultdict(lambda: defaultdict(int))

        for i in range(len(text) - self.n):
            context = text[i : i + self.n - 1]
            next_char = text[i + self.n - 1]
            counts[context][next_char] += 1

        probs = {}

        for context, transition in counts.items():
            total = sum(transition.values())
            probs[context] = {ch: cnt / total for ch, cnt in transition.items()}

        return probs 

            
    def generate(self, seed, length):
        if len(seed) < self.n - 1:
            raise ValueError(f"seed musi mieć co najmniej {self.n-1} znaków")

        result = list(seed)
        context = seed[-(self.n - 1):]

        for _ in range(length - len(seed)):
            if context not in self.probs:
                break

            next_chars = list(self.probs[context].keys())
            weights = list(self.probs[context].values())
            next_char = random.choices(next_chars, weights=weights)[0]

            result.append(next_char)
            context = context[1:] + next_char

        return ''.join(result)


    def perplexity(self, test_text):
        log_prob = 0.0
        count = 0

        for i in range(len(test_text) - self.n):
            context = test_text[i:i + self.n - 1]
            next_char = test_text[i + self.n - 1]

            p = self.probs.get(context, {}).get(next_char, None)

            log_prob += math.log(p)
            count += 1
        return math.exp(-log_prob / count) if count else float('inf')

    def __repr__(self):
        total_transitions = sum(len(transitions) for transitions in self.probs.values())
        return f"Marko (n = {self.n}, states = {len(self.probs)}, transitions = {total_transitions})"


def loaddata(l: list[str]) -> str:
    text = ""

    for i in range(len(l)):
        with open(f"data/{l[i]}", encoding="utf-8") as f:
            data = f.read()
            data = data.lower()
            text += data

    return text


def main():
    text = loaddata(_FILES)

    seed = str(input("ask away: \n"))

    model = Markov(text, len(seed) - 1)

    generated = model.generate(seed, 150)

    print(f"[seed: {seed}]:\n\n {generated}")
    print(model)


if __name__ == '__main__':
    main()
