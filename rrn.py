import numpy as np

data = open('pan_tadeusz.txt', 'r').read()
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)

print('data has %d characters, %d unique.' % (data_size, vocab_size))

char_to_idx = { ch: i for i, ch in enumerate(chars) }
ix_to_char = { i:ch for i, ch in enumerate(chars) }

print(ix_to_char)

hidden_size = 100 # rozmiar ukrytych warstw
seq_length = 25 # kroki do rrn 
learning_rate = 1e-1

Wxh = np.random.randn(hidden_size, vocab_size)*0.01 # input to hidden
Whh = np.random.randn(hidden_size, vocab_size)*0.01 # hidden to hidden
Wxy = np.random.randn(hidden_size, vocab_size)*0.01 # output to hidden

bh = np.zeros((hidden_size, 1)) # hidden bias
by = np.zeros((vocab_size, 1)) # output bias

def lossFun(inputs, targets, hprev):
    """
    inputs,targets are both list of integers.
    hprev is Hx1 array of initial hidden state
    returns the loss, gradients on model parameters, and last hidden state
    """
    xs, hs, ys, ps = {}, {}, {}, {} 
    hs[-1] = np.copy(hprev)
    loss = 0

    # forward pass
    for t in xrange(len(inputs)):
        xs[t] = np.zeros((vocab_size, 1))
        xs[t][inputs[t]] = 1
        hs[t] = np.tanh(np.dot(Wxh, xs[t]) + np.dot(Whh, hs[t - 1]) + bh)
        ys[t] = np.dot(Why, hs[t]) + by
        ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t]))
        loss += -np.log(ps[t][targets[t], 0]) # softmax

    dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
    dbh, dby = np.zeros_like(bh), np.zeros_like(by)
    dhnext = np.zeros_like(hs[0])

    for t in reversed(xrange(len(inputs))):
        dy = np.copy(ps[t])
        dy[targets[t]] -= 1
        dWhy += np.dot(dy, hs[t].T)
        dby += dy
        dh = np.dot(Why.T, dy) + dhnext 
        dhraw = (1 - hs[t] * hs[t]) * dh 
        dbh += dhraw
        dWxh += np.dot(dhraw, xs[t].T)
        dWhh += np.dot(dhraw, hs[t-1].T)
        dhnext = np.dot(Whh.T, dhraw)
    for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
        np.clip(dparam, -5, 5, out=dparam) 
    return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs)-1]