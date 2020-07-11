from math import log, floor, ceil

class Process(object):
    def __init__(self, name, params, r):
        self.name = name
        self.arrival_time = self.activation(r.drand(), params.lam, params.upper_bound)
        self.num_burst = floor(r.drand() * 100 + 1)
        self.burst_time = ceil(r.drand())
        self.IO_burst = ceil(r.drand())


    def activation(self, r, lam, ub):
        while(1):
            test = -log(r)/lam
            if test < ub:
                return int(test)
