# From https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
from __future__ import division
import math

class Rand48(object):
    def __init__(self, seed, upperbound):
        self.n = seed
        self.upperbound = upperbound
    def seed(self, seed):
        self.n = seed
    def upperbound(self, upperbound):
        self.upperbound = upperbound
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
        while(1):
            n = (-1) * math.log(self.drand()) / Lambda
            if (n <= self.upperbound):
                break   
        return n

# Testing that rand() works
upper_bound = 3000

rand = Rand48(123123, 3000)
for i in range(10):
    n = rand.rand(.001)
    print(n)