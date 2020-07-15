from math import log, floor, ceil


class Process(object):
    def __init__(self, name, params, r):
        self.name = name
        self.arrival_time = int(self.activation(r, params.lam, params.upper_bound))
        self.num_burst = floor(r.drand() * 100 + 1)
        self.current_burst_num = 0
        self.blocked_IO = 0  # represents blocked untils...
        self.burst_time = []
        self.IO_burst = []
        for i in range(self.num_burst):
            self.burst_time.append(
                ceil(self.activation(r, params.lam, params.upper_bound))
            )
            self.IO_burst.append(
                ceil(self.activation(r, params.lam, params.upper_bound))
            )
        self.IO_burst.pop()
        self.status = 2  # 0 = running, 1 = ready, 2 = waiting
        self.run_time = 0
        self.sliced = 0
        self.block_time = -1
        self.tau = 1 / params.lam

    def activation(self, r, lam, ub):
        while 1:
            test = -log(r.drand()) / lam
            if test < ub:
                return test

    def __str__(self):
        ret = (
            self.name
            + ", arrival time, "
            + str(self.arrival_time)
            + ", number of bursts, "
            + str(self.num_burst)
            + ", CPU bursts, "
            + str(self.burst_time)
            + ", I/O bursts, "
            + str(self.IO_burst)
            + ", status, "
            + str(self.status)
        )
        return ret
