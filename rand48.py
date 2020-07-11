# From https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
from __future__ import division
import math

class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    def lrand(self):
        return self.next() >> 17
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n
    # Justin Mai garbage -Alan Turing
    def rand(self, Lambda):
        n = (-1) * math.log(self.drand()) / Lambda
        return n

    
'''
PROGRAM START
'''
# seed = 123123
# processes = []
# # Set the seed value in srand48()
# rng = Rand48(seed)
# rng.srand(test.n)

# for i in range(params.n):
#     arrival_time = math.floor(rng.drand())
    # if arrival_time > params.upper_bound:
    #     continue

# Testing that rand() works
upper_bound = 3000

rand = Rand48(123123)
for i in range(10):
    n = rand.rand(.001)
    if (n > upper_bound):
        i -= 1
        continue
    print(n)