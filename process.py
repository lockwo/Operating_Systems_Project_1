from math import log, floor, ceil

class Process(object):
    def __init__(self, name, params, r):
        self.name = name
        self.arrival_time = self.activation(r, params.lam, params.upper_bound)
        self.num_burst = floor(r.drand() * 100 + 1)
        self.current_burst_num = 0
        self.burst_time = []
        self.IO_burst = []
        for i in range(self.num_burst):
            self.burst_time.append(ceil(r.drand() * 100))
            self.IO_burst.append(ceil(r.drand() * 100))
        self.status = 2 # 0 = running, 1 = ready, 2 = waiting
        self.tau = 1/params.lam


    def activation(self, r, lam, ub):
        while(1):
            test = -log(r.drand())/lam
            if test < ub:
                return int(test)
            
    def __str__(self):
        ret = self.name + ", arrival time, " + str(self.arrival_time) + ", CPU bursts, " + str(self.burst_time) + ", I/O bursts, " + str(self.IO_burst) + ", status, " + str(self.status)
        return ret
