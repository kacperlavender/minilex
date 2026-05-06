from collections import defaultdict
import random
import math

class Markov:
    def __init__(self, text):
        self.text = text
        self.probs = self._build_probs(text)
    
    def _build_probs(self, text):
        counts = defaultdict(lambda: defaultdict(int))

        for i in range(len(text) - 1):
            a = text[i]
            b = text[i + 1]
            counts[a][b] += 1

        probs = {}

        for a, transition in counts.items():
            total = sum(transition.values())
            probs[a] = {b: cnt / total for b, cnt in transition.items()}

        return probs 

            
    def generate(self, start_char, length):
        result = [start_char]
        current = start_char

        for _ in range(length - 1):
            if current not in self.probs:
                break

            next_chars = list(self.probs[current].keys())
            weights = list(self.probs[current].values())

            current = random.choices(next_chars, weights=weights, k=1)[0]
            result.append(current)

        return ''.join(result)

    def perplexity(self, test_text):
        log_prob = 0.0
        count = 0

        for i in range(len(test_text) - 1):
            a = test_text[i]
            b = test_text[i + 1]

            p = self.probs.get(a, {}).get(b, None)

            if p is None or p == 0:
                p = 1e-10
            
            log_prob += math.log(p)
            count += 1
        return math.exp(-log_prob / count) if count else float('inf')

def main():
    with open("data/pan_tadeusz.txt", encoding="utf-8") as f:
        text = f.read()

    

    model = Markov(text)

    # seed = random.choice(list(model.probs.keys()))
    seed = 'a'
    generated = model.generate(seed, 50)

    print(f"[seed: {seed}]:\n {generated}")

    print(f"perplexity na korpusie: {model.perplexity(text):.2f}")
    print(f"perplexity na 'Soplica ': {model.perplexity('Soplica '):.2f}")
    print(f"perplexity na 'xyz123': {model.perplexity('xyz123'):.2f}")

if __name__ == '__main__':
    main()