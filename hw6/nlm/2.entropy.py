import nlm
import torch

nlm.NLM.load('large')
h = nlm.NLM()
p = 1
for c in 't h e _ e n d _ '.split():
    print(p, h) # cumulative prob and current state (and the distribution of the next char)
    p *= h.next_prob(c) # include prob (c | ...)
    h += c # observe another character (changing NLM state internally)
