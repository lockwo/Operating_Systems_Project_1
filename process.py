from math import log


class Process(object):
    def __init__(self, name, params, r):
        self.name = name
        self.arrival_time = self.activation(r.drand(), params.lam, params.upper_bound)


    def activation(self, r, lam, ub):
        while(1):
            test = log(r)/lam
            if test < ub:
                return test
