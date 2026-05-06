from collections import defaultdict
import random
import math
from pathlib import Path
import time

# https://wolnelektury.pl/katalog/lektury/

_FILES = [f.name for f in Path("data").glob("*.txt")]

class Markov:
    def __init__(self, text: str, n = 3):
        self.text = text
        self.n = n
        self.probs = self._build_probs(text)
    
    def _build_probs(self, text: str, alpha=0.1):
        counts = defaultdict(lambda: defaultdict(int))

        for i in range(len(text) - self.n):
            context = text[i : i + self.n - 1]
            next_char = text[i + self.n - 1]
            counts[context][next_char] += 1

        probs = {}
        all_chars = set(text)

        for context, transition in counts.items():
            total = sum(transition.values())
            probs[context] = {
                ch: (transition.get(ch, 0) + alpha) / (total + alpha * len(all_chars)) for ch, cnt in transition.items()
            }

        return probs 

            
    def generate(self, seed: str, length: int, beam_width = 3):
        candidates = [(seed, 0.0)] # text, log_of_probability

        for _ in range(length):
            new_candidates = []

            for text, score in candidates:
                context = text[-(self.n - 1):]
                if context not in self.probs:
                    continue

                for char, prob in self.probs.get(context, {}).items():
                    new_candidates.append((text + char, score + math.log(prob)))

            if not new_candidates:
                break 

            # sort by score and choose best path
            candidates = sorted(new_candidates, key=lambda x: x[1], reverse=True)[:beam_width]

        return candidates[0][0] if candidates else seed


    def perplexity(self, test_text: str):
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

    t_start = time.perf_counter()
    model = Markov(text, len(seed) - 1)
    generated = model.generate(seed, 150)

    t_stop = time.perf_counter()

    print(f"[seed: {seed}]:\n\n {generated}")
    
    print()
    print(model)
    print("took:", "{:.7f}s".format(t_stop - t_start))


if __name__ == '__main__':
    main()
